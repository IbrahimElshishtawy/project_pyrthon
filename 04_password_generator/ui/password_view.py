# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمولد كلمات السر وفاحص القوة
"""

import tkinter as tk
from ui.theme import THEME


class PasswordGeneratorView(tk.Frame):
    def __init__(self, parent, logic):
        super().__init__(parent, bg=THEME["bg"])
        self.logic = logic

        self.setup_ui()
        self.generate_password()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=14)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🔐 مولّد كلمات السر وفاحص القوة",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="قم بتوليد كلمات مرور عشوائية غير قابلة للاختراق بسهولة",
            font=(THEME["font_family"], 10),
            bg=THEME["surface"],
            fg=THEME["text_muted"]
        )
        subtitle.pack()

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        # Output Card
        out_card = tk.Frame(body, bg=THEME["surface"], padx=16, pady=14, bd=1, relief=tk.SOLID)
        out_card.pack(fill=tk.X, pady=(0, 14))

        self.pwd_var = tk.StringVar(value="")
        self.pwd_entry = tk.Entry(
            out_card,
            textvariable=self.pwd_var,
            font=("Consolas", 18, "bold"),
            bg=THEME["bg"],
            fg=THEME["neon_green"],
            insertbackground=THEME["neon_green"],
            relief=tk.FLAT,
            justify="center",
            bd=3
        )
        self.pwd_entry.pack(fill=tk.X, ipady=6, pady=(0, 10))

        # Copy & Regenerate Row
        btn_row = tk.Frame(out_card, bg=THEME["surface"])
        btn_row.pack(fill=tk.X)

        btn_copy = tk.Button(
            btn_row,
            text="📋 نسخ إلى الحافظة (Copy)",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.copy_to_clipboard
        )
        btn_copy.pack(side=tk.RIGHT, padx=(4, 0))

        btn_gen = tk.Button(
            btn_row,
            text="⚡ توليد كلمة جديدة",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["success"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.generate_password
        )
        btn_gen.pack(side=tk.RIGHT, padx=(0, 4))

        self.toast_lbl = tk.Label(btn_row, text="", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg="#A7F3D0")
        self.toast_lbl.pack(side=tk.LEFT)

        # Strength Bar Card
        str_card = tk.Frame(body, bg=THEME["surface"], padx=16, pady=10, bd=1, relief=tk.SOLID)
        str_card.pack(fill=tk.X, pady=(0, 14))

        s_top = tk.Frame(str_card, bg=THEME["surface"])
        s_top.pack(fill=tk.X, pady=(0, 6))

        tk.Label(s_top, text="مقياس قوة الكلمة:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.str_badge = tk.Label(s_top, text="قوية جداً", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["neon_green"])
        self.str_badge.pack(side=tk.LEFT)

        self.meter_canvas = tk.Canvas(str_card, height=12, bg=THEME["bg"], highlightthickness=0)
        self.meter_canvas.pack(fill=tk.X)

        # Options Settings Card
        opts_card = tk.Frame(body, bg=THEME["surface"], padx=16, pady=12, bd=1, relief=tk.SOLID)
        opts_card.pack(fill=tk.X, pady=(0, 14))

        len_row = tk.Frame(opts_card, bg=THEME["surface"])
        len_row.pack(fill=tk.X, pady=(0, 10))

        self.len_lbl = tk.Label(len_row, text="طول الكلمة: 16 حرفاً", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"])
        self.len_lbl.pack(side=tk.RIGHT)

        self.len_var = tk.IntVar(value=16)
        slider = tk.Scale(
            len_row,
            from_=6,
            to=48,
            orient=tk.HORIZONTAL,
            variable=self.len_var,
            bg=THEME["surface"],
            fg=THEME["accent_cyan"],
            activebackground=THEME["primary"],
            troughcolor=THEME["bg"],
            highlightthickness=0,
            showvalue=False,
            command=self.on_slider
        )
        slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 14))

        # Checkboxes
        grid = tk.Frame(opts_card, bg=THEME["surface"])
        grid.pack(fill=tk.X)

        self.chk_upper = tk.BooleanVar(value=True)
        self.chk_lower = tk.BooleanVar(value=True)
        self.chk_digits = tk.BooleanVar(value=True)
        self.chk_symbols = tk.BooleanVar(value=True)
        self.chk_no_amb = tk.BooleanVar(value=False)

        c1 = tk.Checkbutton(grid, text="أحرف كبيرة (A-Z)", variable=self.chk_upper, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#E2E8F0", selectcolor=THEME["bg"], command=self.generate_password)
        c2 = tk.Checkbutton(grid, text="أحرف صغيرة (a-z)", variable=self.chk_lower, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#E2E8F0", selectcolor=THEME["bg"], command=self.generate_password)
        c3 = tk.Checkbutton(grid, text="أرقام (0-9)", variable=self.chk_digits, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#E2E8F0", selectcolor=THEME["bg"], command=self.generate_password)
        c4 = tk.Checkbutton(grid, text="رموز خاصة (!@#$)", variable=self.chk_symbols, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#E2E8F0", selectcolor=THEME["bg"], command=self.generate_password)
        c5 = tk.Checkbutton(grid, text="استبعاد المتشابهة (l, 1, I, O, 0)", variable=self.chk_no_amb, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#E2E8F0", selectcolor=THEME["bg"], command=self.generate_password)

        c1.grid(row=0, column=0, sticky="w", padx=6, pady=2)
        c2.grid(row=0, column=1, sticky="w", padx=6, pady=2)
        c3.grid(row=0, column=2, sticky="w", padx=6, pady=2)
        c4.grid(row=1, column=0, sticky="w", padx=6, pady=2)
        c5.grid(row=1, column=1, columnspan=2, sticky="w", padx=6, pady=2)

        # Vault Listbox
        vault_card = tk.Frame(body, bg=THEME["surface"], padx=12, pady=10, bd=1, relief=tk.SOLID)
        vault_card.pack(fill=tk.BOTH, expand=True)

        v_top = tk.Frame(vault_card, bg=THEME["surface"])
        v_top.pack(fill=tk.X, pady=(0, 4))
        tk.Label(v_top, text="📜 سجل الكلمات المولدة مؤخراً:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        tk.Button(v_top, text="مسح السجل", font=(THEME["font_family"], 8), bg="#334155", fg="#F87171", relief=tk.FLAT, cursor="hand2", command=self.on_clear_hist).pack(side=tk.LEFT)

        self.listbox_vault = tk.Listbox(
            vault_card,
            bg=THEME["bg"],
            fg="#E2E8F0",
            font=("Consolas", 10),
            selectbackground=THEME["primary"],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.listbox_vault.pack(fill=tk.BOTH, expand=True)
        self.listbox_vault.bind("<Double-Button-1>", self.on_reuse_history)

    def on_slider(self, val):
        self.len_lbl.config(text=f"طول الكلمة: {val} حرفاً")
        self.generate_password()

    def generate_password(self):
        res = self.logic.generate(
            length=self.len_var.get(),
            use_upper=self.chk_upper.get(),
            use_lower=self.chk_lower.get(),
            use_digits=self.chk_digits.get(),
            use_symbols=self.chk_symbols.get(),
            no_ambiguous=self.chk_no_amb.get()
        )
        self.pwd_var.set(res["password"])
        self.str_badge.config(text=res["rating"], fg=res["color"])
        self.draw_meter(res["pct"], res["color"])
        self.refresh_vault()

    def draw_meter(self, pct, color):
        self.meter_canvas.delete("all")
        w = self.meter_canvas.winfo_width() or 600
        h = 12
        self.meter_canvas.create_rectangle(0, 0, w, h, fill="#334155", outline="")
        self.meter_canvas.create_rectangle(0, 0, int(w * pct), h, fill=color, outline="")

    def copy_to_clipboard(self):
        pwd = self.pwd_var.get()
        if not pwd:
            return
        self.clipboard_clear()
        self.clipboard_append(pwd)
        self.toast_lbl.config(text="✅ تم النسخ بنجاح!")
        self.after(2000, lambda: self.toast_lbl.config(text=""))

    def refresh_vault(self):
        self.listbox_vault.delete(0, tk.END)
        for pwd in self.logic.history:
            self.listbox_vault.insert(tk.END, f"• {pwd}")

    def on_reuse_history(self, event):
        sel = self.listbox_vault.curselection()
        if sel:
            pwd = self.logic.history[sel[0]]
            self.pwd_var.set(pwd)
            self.copy_to_clipboard()

    def on_clear_hist(self):
        self.logic.clear_history()
        self.listbox_vault.delete(0, tk.END)
