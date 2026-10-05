#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 4: مولّد كلمات السر القوية (Secure Password Generator & Strength Meter)
يدعم:
- تخصيص طول الكلمة (من 6 إلى 64 حرفاً)
- تضمين / استبعاد الأحرف الكبيرة، الصغيرة، الأرقام، الرموز الخاصة
- خيار استبعاد الرموز المتشابهة (l, 1, I, O, 0)
- فحص قوة كلمة المرور وحساب الإنتروبيا (Entropy) ومؤشر شريطي ملون
- نسخ مباشر للحافظة (Copy to Clipboard) مع إشعار
- سجل وحافظة للكلمات التي تم توليدها خلال الجلسة
"""

import math
import random
import string
import tkinter as tk
from tkinter import messagebox, ttk


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مولّد كلمات السر القوية | Password Generator")
        self.geometry("740x620")
        self.minsize(680, 560)
        self.configure(bg="#0F172A")

        self.history = []

        self.setup_ui()
        self.generate_password()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=14)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🔐 مولّد كلمات السر وفاحص القوة",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="قم بتوليد كلمات مرور عشوائية غير قابلة للاختراق بسهولة",
            font=("Segoe UI", 10),
            bg="#1E293B",
            fg="#94A3B8"
        )
        subtitle.pack()

        # Body Container
        body = tk.Frame(self, bg="#0F172A", padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        # Output Display Card
        disp_card = tk.Frame(body, bg="#1E293B", padx=16, pady=14, bd=1, relief=tk.SOLID)
        disp_card.pack(fill=tk.X, pady=(0, 14))

        self.pwd_var = tk.StringVar(value="")
        self.pwd_entry = tk.Entry(
            disp_card,
            textvariable=self.pwd_var,
            font=("Consolas", 18, "bold"),
            bg="#0F172A",
            fg="#4ADE80",
            insertbackground="#4ADE80",
            relief=tk.FLAT,
            justify="center",
            bd=3
        )
        self.pwd_entry.pack(fill=tk.X, ipady=6, pady=(0, 10))

        # Copy & Regenerate Buttons
        btns_row = tk.Frame(disp_card, bg="#1E293B")
        btns_row.pack(fill=tk.X)

        self.copy_btn = tk.Button(
            btns_row,
            text="📋 نسخ إلى الحافظة (Copy)",
            font=("Segoe UI", 11, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.copy_to_clipboard
        )
        self.copy_btn.pack(side=tk.RIGHT, padx=(4, 0))

        self.gen_btn = tk.Button(
            btns_row,
            text="⚡ توليد كلمة جديدة",
            font=("Segoe UI", 11, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.generate_password
        )
        self.gen_btn.pack(side=tk.RIGHT, padx=(0, 4))

        self.toast_label = tk.Label(
            btns_row,
            text="",
            font=("Segoe UI", 10, "bold"),
            bg="#1E293B",
            fg="#A7F3D0"
        )
        self.toast_label.pack(side=tk.LEFT)

        # Strength Bar Card
        strength_card = tk.Frame(body, bg="#1E293B", padx=16, pady=10, bd=1, relief=tk.SOLID)
        strength_card.pack(fill=tk.X, pady=(0, 14))

        strength_top = tk.Frame(strength_card, bg="#1E293B")
        strength_top.pack(fill=tk.X, pady=(0, 6))

        self.strength_title = tk.Label(
            strength_top,
            text="مقياس قوة الكلمة:",
            font=("Segoe UI", 10, "bold"),
            bg="#1E293B",
            fg="#94A3B8"
        )
        self.strength_title.pack(side=tk.RIGHT)

        self.strength_badge = tk.Label(
            strength_top,
            text="قوية جداً (92 bits)",
            font=("Segoe UI", 10, "bold"),
            bg="#1E293B",
            fg="#4ADE80"
        )
        self.strength_badge.pack(side=tk.LEFT)

        # Visual progress bar with canvas
        self.meter_canvas = tk.Canvas(strength_card, height=12, bg="#0F172A", highlightthickness=0)
        self.meter_canvas.pack(fill=tk.X)

        # Options Settings Card
        opts_card = tk.Frame(body, bg="#1E293B", padx=16, pady=12, bd=1, relief=tk.SOLID)
        opts_card.pack(fill=tk.X, pady=(0, 14))

        # Length slider
        length_row = tk.Frame(opts_card, bg="#1E293B")
        length_row.pack(fill=tk.X, pady=(0, 10))

        self.len_label = tk.Label(
            length_row,
            text="طول الكلمة: 16 حرفاً",
            font=("Segoe UI", 11, "bold"),
            bg="#1E293B",
            fg="#F8FAFC"
        )
        self.len_label.pack(side=tk.RIGHT)

        self.length_var = tk.IntVar(value=16)
        self.length_slider = tk.Scale(
            length_row,
            from_=6,
            to=48,
            orient=tk.HORIZONTAL,
            variable=self.length_var,
            bg="#1E293B",
            fg="#38BDF8",
            activebackground="#0284C7",
            troughcolor="#0F172A",
            highlightthickness=0,
            showvalue=False,
            command=self.on_slider_change
        )
        self.length_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 14))

        # Checkboxes
        checks_grid = tk.Frame(opts_card, bg="#1E293B")
        checks_grid.pack(fill=tk.X)

        self.chk_upper = tk.BooleanVar(value=True)
        self.chk_lower = tk.BooleanVar(value=True)
        self.chk_digits = tk.BooleanVar(value=True)
        self.chk_symbols = tk.BooleanVar(value=True)
        self.chk_no_ambiguous = tk.BooleanVar(value=False)

        c1 = tk.Checkbutton(checks_grid, text="أحرف كبيرة (A-Z)", variable=self.chk_upper, font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0", selectcolor="#0F172A", activebackground="#1E293B", activeforeground="#38BDF8", command=self.generate_password)
        c2 = tk.Checkbutton(checks_grid, text="أحرف صغيرة (a-z)", variable=self.chk_lower, font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0", selectcolor="#0F172A", activebackground="#1E293B", activeforeground="#38BDF8", command=self.generate_password)
        c3 = tk.Checkbutton(checks_grid, text="أرقام (0-9)", variable=self.chk_digits, font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0", selectcolor="#0F172A", activebackground="#1E293B", activeforeground="#38BDF8", command=self.generate_password)
        c4 = tk.Checkbutton(checks_grid, text="رموز خاصة (!@#$)", variable=self.chk_symbols, font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0", selectcolor="#0F172A", activebackground="#1E293B", activeforeground="#38BDF8", command=self.generate_password)
        c5 = tk.Checkbutton(checks_grid, text="استبعاد المتشابهة (l, 1, I, O, 0)", variable=self.chk_no_ambiguous, font=("Segoe UI", 10), bg="#1E293B", fg="#E2E8F0", selectcolor="#0F172A", activebackground="#1E293B", activeforeground="#38BDF8", command=self.generate_password)

        c1.grid(row=0, column=0, sticky="w", padx=6, pady=2)
        c2.grid(row=0, column=1, sticky="w", padx=6, pady=2)
        c3.grid(row=0, column=2, sticky="w", padx=6, pady=2)
        c4.grid(row=1, column=0, sticky="w", padx=6, pady=2)
        c5.grid(row=1, column=1, columnspan=2, sticky="w", padx=6, pady=2)

        # History Vault Frame
        hist_card = tk.Frame(body, bg="#1E293B", padx=12, pady=10, bd=1, relief=tk.SOLID)
        hist_card.pack(fill=tk.BOTH, expand=True)

        hist_top = tk.Frame(hist_card, bg="#1E293B")
        hist_top.pack(fill=tk.X, pady=(0, 4))
        tk.Label(hist_top, text="📜 سجل الكلمات المولدة مؤخراً:", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)
        tk.Button(hist_top, text="مسح السجل", font=("Segoe UI", 8), bg="#334155", fg="#F87171", relief=tk.FLAT, cursor="hand2", command=self.clear_history).pack(side=tk.LEFT)

        self.hist_listbox = tk.Listbox(
            hist_card,
            bg="#0F172A",
            fg="#E2E8F0",
            font=("Consolas", 10),
            selectbackground="#0284C7",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.hist_listbox.pack(fill=tk.BOTH, expand=True)
        self.hist_listbox.bind("<Double-Button-1>", self.reuse_hist_password)

    def on_slider_change(self, val):
        self.len_label.config(text=f"طول الكلمة: {val} حرفاً")
        self.generate_password()

    def generate_password(self):
        charset = ""
        if self.chk_upper.get():
            charset += string.ascii_uppercase
        if self.chk_lower.get():
            charset += string.ascii_lowercase
        if self.chk_digits.get():
            charset += string.digits
        if self.chk_symbols.get():
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if self.chk_no_ambiguous.get():
            for amb in "l1IoO0":
                charset = charset.replace(amb, "")

        if not charset:
            self.pwd_var.set("")
            self.strength_badge.config(text="اختر نوع حرف واحد على الأقل!", fg="#EF4444")
            self.draw_meter(0, "#EF4444")
            return

        length = self.length_var.get()
        # Secure random choice
        pwd = "".join(random.SystemRandom().choice(charset) for _ in range(length))
        self.pwd_var.set(pwd)

        # Calculate Entropy
        pool_size = len(charset)
        entropy = length * math.log2(pool_size) if pool_size > 0 else 0
        self.update_strength_display(entropy)

        # Add to history
        if pwd not in self.history:
            self.history.insert(0, pwd)
            self.hist_listbox.insert(0, f"• {pwd}")
            if len(self.history) > 20:
                self.history.pop()
                self.hist_listbox.delete(tk.END)

    def update_strength_display(self, entropy):
        if entropy < 35:
            text = f"ضعيفة جدًا ({int(entropy)} bits) ⚠️"
            color = "#EF4444"
            fill_pct = 0.25
        elif entropy < 55:
            text = f"متوسطة ({int(entropy)} bits)"
            color = "#F59E0B"
            fill_pct = 0.50
        elif entropy < 75:
            text = f"قوية ({int(entropy)} bits) 👍"
            color = "#38BDF8"
            fill_pct = 0.75
        else:
            text = f"قوية للغاية / درجة عسكرية ({int(entropy)} bits) 🛡️"
            color = "#10B981"
            fill_pct = 1.0

        self.strength_badge.config(text=text, fg=color)
        self.draw_meter(fill_pct, color)

    def draw_meter(self, pct, color):
        self.meter_canvas.delete("all")
        w = self.meter_canvas.winfo_width()
        if w <= 1:
            w = 600
        h = 12
        self.meter_canvas.create_rectangle(0, 0, w, h, fill="#334155", outline="")
        self.meter_canvas.create_rectangle(0, 0, int(w * pct), h, fill=color, outline="")

    def copy_to_clipboard(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)
        self.toast_label.config(text="✅ تم النسخ بنجاح!")
        self.after(2000, lambda: self.toast_label.config(text=""))

    def reuse_hist_password(self, event):
        sel = self.hist_listbox.curselection()
        if sel:
            item = self.hist_listbox.get(sel[0]).replace("• ", "").strip()
            self.pwd_var.set(item)
            self.copy_to_clipboard()

    def clear_history(self):
        self.history.clear()
        self.hist_listbox.delete(0, tk.END)


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
