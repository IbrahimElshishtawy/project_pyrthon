# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمختصر الروابط وقاعدة بيانات SQLite
"""

import tkinter as tk
import webbrowser
from tkinter import messagebox, ttk
from ui.theme import THEME


class URLShortenerView(tk.Frame):
    def __init__(self, parent, db, port=8000):
        super().__init__(parent, bg=THEME["bg"])
        self.db = db
        self.port = port

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🔗 مختصر الروابط الذكي مع قاعدة بيانات SQLite",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        server_badge = tk.Label(
            header,
            text=f"🟢 سيرفر التحويل يعمل على: http://localhost:{self.port}",
            font=(THEME["font_family"], 9, "bold"),
            bg="#065F46",
            fg="#A7F3D0",
            padx=10,
            pady=4
        )
        server_badge.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Form Card
        form_card = tk.Frame(body, bg=THEME["surface"], padx=16, pady=12, bd=1, relief=tk.SOLID)
        form_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(form_card, text="✂️ اختصار رابط جديد:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 8))

        row1 = tk.Frame(form_card, bg=THEME["surface"])
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="الرابط الأصلي (Long URL):", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.long_url_entry = tk.Entry(row1, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["accent_cyan"], relief=tk.FLAT)
        self.long_url_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=6)
        self.long_url_entry.insert(0, "https://github.com")

        row2 = tk.Frame(form_card, bg=THEME["surface"])
        row2.pack(fill=tk.X, pady=4)

        btn_shorten = tk.Button(
            row2,
            text="⚡ إنشاء الرابط المختصر",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            command=self.on_shorten
        )
        btn_shorten.pack(side=tk.LEFT)

        tk.Label(row2, text="(اتركه فارغاً للتوليد التلقائي)", font=(THEME["font_family"], 8), bg=THEME["surface"], fg="#64748B").pack(side=tk.RIGHT, padx=4)

        self.alias_entry = tk.Entry(row2, font=(THEME["font_family"], 10), bg=THEME["bg"], fg=THEME["accent_cyan"], insertbackground=THEME["accent_cyan"], relief=tk.FLAT, width=16)
        self.alias_entry.pack(side=tk.RIGHT, padx=4)

        tk.Label(row2, text="اسم مخصص اختياري (Custom Alias):", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)

        # Result Banner
        self.res_banner = tk.Frame(form_card, bg=THEME["bg"], padx=10, pady=6)
        self.res_banner.pack(fill=tk.X, pady=(6, 0))

        self.lbl_res = tk.Label(self.res_banner, text="الرابط المختصر سيظهر هنا بعد التوليد", font=("Consolas", 10), bg=THEME["bg"], fg=THEME["text_muted"])
        self.lbl_res.pack(side=tk.RIGHT)

        self.btn_copy_fast = tk.Button(self.res_banner, text="📋 نسخ", font=(THEME["font_family"], 8, "bold"), bg=THEME["surface_light"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", state=tk.DISABLED, command=self.on_copy_fast)
        self.btn_copy_fast.pack(side=tk.LEFT)

        # Table
        table_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        cols = ("id", "short_code", "full_short_url", "clicks", "created_at", "original_url")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="#")
        self.tree.heading("short_code", text="الكود")
        self.tree.heading("full_short_url", text="الرابط المختصر")
        self.tree.heading("clicks", text="النقرات")
        self.tree.heading("created_at", text="تاريخ الإنشاء")
        self.tree.heading("original_url", text="الرابط الأصلي المستهدف")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("short_code", width=80, anchor="center")
        self.tree.column("full_short_url", width=220, anchor="w")
        self.tree.column("clicks", width=65, anchor="center")
        self.tree.column("created_at", width=120, anchor="center")
        self.tree.column("original_url", width=340, anchor="w")

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-Button-1>", lambda e: self.on_open_browser())

        # Action Toolbar
        action_bar = tk.Frame(body, bg=THEME["bg"])
        action_bar.pack(fill=tk.X)

        tk.Button(action_bar, text="🌐 فتح الرابط في المتصفح", font=(THEME["font_family"], 9, "bold"), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_open_browser).pack(side=tk.RIGHT, padx=4)
        tk.Button(action_bar, text="📋 نسخ الرابط المحدد", font=(THEME["font_family"], 9), bg=THEME["primary"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_copy_selected).pack(side=tk.RIGHT, padx=4)
        tk.Button(action_bar, text="🗑 حذف من قاعدة البيانات", font=(THEME["font_family"], 9), bg=THEME["danger"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_delete).pack(side=tk.LEFT, padx=4)
        tk.Button(action_bar, text="🔄 تحديث الجدول", font=(THEME["font_family"], 9), bg=THEME["surface_light"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.refresh_table).pack(side=tk.LEFT, padx=4)

    def on_shorten(self):
        orig = self.long_url_entry.get().strip()
        alias = self.alias_entry.get().strip() or None
        if not orig:
            messagebox.showwarning("تنبيه", "يرجى إدخال الرابط المراد اختصاره!")
            return

        try:
            code, _ = self.db.create_short_url(orig, alias)
            short_url = f"http://localhost:{self.port}/{code}"
            self.lbl_res.config(text=short_url, fg="#4ADE80")
            self.btn_copy_fast.config(state=tk.NORMAL)
            self.alias_entry.delete(0, tk.END)
            self.refresh_table()
            messagebox.showinfo("تم بنجاح!", f"تم إنشاء الرابط المختصر:\n{short_url}")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        rows = self.db.get_all()
        for r in rows:
            u_id, code, clicks, dt, orig = r
            short_full = f"http://localhost:{self.port}/{code}"
            self.tree.insert("", tk.END, values=(u_id, code, short_full, clicks, dt, orig))

    def on_copy_fast(self):
        url = self.lbl_res.cget("text")
        if url and "http" in url:
            self.clipboard_clear()
            self.clipboard_append(url)
            messagebox.showinfo("تم النسخ", "تم نسخ الرابط إلى الحافظة!")

    def on_copy_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط من الجدول!")
            return
        vals = self.tree.item(sel[0], "values")
        self.clipboard_clear()
        self.clipboard_append(vals[2])
        messagebox.showinfo("تم النسخ", f"تم نسخ الرابط:\n{vals[2]}")

    def on_open_browser(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط لفتحه!")
            return
        vals = self.tree.item(sel[0], "values")
        webbrowser.open(vals[2])

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط لحذفه!")
            return
        u_id = int(self.tree.item(sel[0], "values")[0])
        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الرابط #{u_id}؟"):
            self.db.delete_url(u_id)
            self.refresh_table()
