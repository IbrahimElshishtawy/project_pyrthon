# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمتتبع وكاشط أسعار المنتجات
"""

import threading
import time
import tkinter as tk
from tkinter import messagebox, ttk
from ui.theme import THEME


class PriceScraperView(tk.Frame):
    def __init__(self, parent, service):
        super().__init__(parent, bg=THEME["bg"])
        self.service = service
        self.is_checking = False

        self.setup_ui()
        self.refresh_table()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🏷️ متتبع وكاشط أسعار المنتجات الذكي",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        self.btn_check_all = tk.Button(
            header,
            text="🔄 فحص جميع الأسعار الآن",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=4,
            command=self.check_all_threaded
        )
        self.btn_check_all.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Add Product Card
        add_card = tk.Frame(body, bg=THEME["surface"], padx=14, pady=12, bd=1, relief=tk.SOLID)
        add_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(add_card, text="➕ إضافة منتج جديد لتتبعه:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 8))

        row1 = tk.Frame(add_card, bg=THEME["surface"])
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="اسم المنتج:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.name_entry = tk.Entry(row1, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["accent_cyan"], relief=tk.FLAT)
        self.name_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=6)

        row2 = tk.Frame(add_card, bg=THEME["surface"])
        row2.pack(fill=tk.X, pady=4)
        tk.Label(row2, text="رابط المنتج (URL):", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.url_entry = tk.Entry(row2, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["accent_cyan"], relief=tk.FLAT)
        self.url_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=6)

        row3 = tk.Frame(add_card, bg=THEME["surface"])
        row3.pack(fill=tk.X, pady=2)

        add_submit = tk.Button(row3, text="إضافة للتتبع", font=(THEME["font_family"], 10, "bold"), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=16, command=self.on_add_product)
        add_submit.pack(side=tk.LEFT)

        tk.Label(row3, text="العملة:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT, padx=(10, 4))
        self.curr_var = tk.StringVar(value="ج.م (EGP)")
        curr_cb = ttk.Combobox(row3, textvariable=self.curr_var, values=["ج.م (EGP)", "$ (USD)", "ر.س (SAR)", "د.إ (AED)"], state="readonly", width=10)
        curr_cb.pack(side=tk.RIGHT)

        tk.Label(row3, text="السعر المستهدف للتنبيه:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT, padx=(14, 4))
        self.target_entry = tk.Entry(row3, font=(THEME["font_family"], 10), bg=THEME["bg"], fg=THEME["accent_cyan"], insertbackground=THEME["accent_cyan"], relief=tk.FLAT, width=12)
        self.target_entry.pack(side=tk.RIGHT)

        # Products Table
        table_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        cols = ("id", "name", "current_price", "target_price", "status", "last_checked")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="#")
        self.tree.heading("name", text="اسم المنتج")
        self.tree.heading("current_price", text="السعر الحالي")
        self.tree.heading("target_price", text="السعر المستهدف")
        self.tree.heading("status", text="حالة التنبيه")
        self.tree.heading("last_checked", text="آخر فحص")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("name", width=260, anchor="w")
        self.tree.column("current_price", width=110, anchor="center")
        self.tree.column("target_price", width=110, anchor="center")
        self.tree.column("status", width=130, anchor="center")
        self.tree.column("last_checked", width=140, anchor="center")

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Bottom Bar
        bot_bar = tk.Frame(body, bg=THEME["bg"])
        bot_bar.pack(fill=tk.X)

        self.status_lbl = tk.Label(bot_bar, text="جاهز للتتبع", font=(THEME["font_family"], 10), bg=THEME["bg"], fg=THEME["text_muted"])
        self.status_lbl.pack(side=tk.RIGHT)

        tk.Button(bot_bar, text="🗑 حذف المنتج", font=(THEME["font_family"], 9), bg=THEME["danger"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_delete).pack(side=tk.LEFT, padx=4)
        tk.Button(bot_bar, text="🔍 فحص المنتج المحدد فقط", font=(THEME["font_family"], 9), bg=THEME["surface_light"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.check_selected_threaded).pack(side=tk.LEFT, padx=4)

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.service.products:
            curr_p = p.get("current_price", 0.0)
            target_p = p.get("target_price", 0.0)

            if curr_p <= target_p:
                status_text = "🔥 نزل للسعر المستهدف!"
            else:
                diff = curr_p - target_p
                status_text = f"أعلى بـ {diff:,.0f}"

            self.tree.insert(
                "",
                tk.END,
                values=(
                    p["id"],
                    p["name"],
                    f"{curr_p:,.2f} {p.get('currency', '')}",
                    f"{target_p:,.2f} {p.get('currency', '')}",
                    status_text,
                    p.get("last_checked", "--")
                )
            )

    def on_add_product(self):
        name = self.name_entry.get().strip()
        url = self.url_entry.get().strip()
        t_str = self.target_entry.get().strip()

        if not name or not url or not t_str:
            messagebox.showwarning("تنبيه", "يرجى تعبئة كافة الحقول!")
            return

        try:
            t_val = float(t_str)
            if t_val <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("تنبيه", "يرجى إدخال سعر مستهدف صحيح!")
            return

        self.service.add_product(name, url, t_val, self.curr_var.get())
        self.name_entry.delete(0, tk.END)
        self.url_entry.delete(0, tk.END)
        self.target_entry.delete(0, tk.END)
        self.refresh_table()
        messagebox.showinfo("تم الإضافة", "تمت إضافة المنتج بنجاح!")

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد منتج لحذفه!")
            return
        p_id = int(self.tree.item(sel[0], "values")[0])
        self.service.delete_product(p_id)
        self.refresh_table()

    def check_selected_threaded(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد منتج للفحص!")
            return
        p_id = int(self.tree.item(sel[0], "values")[0])
        p = next((x for x in self.service.products if x["id"] == p_id), None)
        if not p:
            return

        def run():
            self.service.scrape_product(p)
            self.after(0, self.refresh_table)
            self.after(0, lambda: messagebox.showinfo("اكتمل الفحص", f"تم فحص سعر {p['name']}:\nالسعر الحالي: {p['current_price']} {p['currency']}"))

        threading.Thread(target=run, daemon=True).start()

    def check_all_threaded(self):
        if self.is_checking:
            return
        self.is_checking = True
        self.btn_check_all.config(state=tk.DISABLED, text="⏳ جارٍ فحص الأسعار...")
        self.status_lbl.config(text="يتم الآن جلب بيانات الأسعار وتحديث القائمة...")

        def run():
            for p in self.service.products:
                self.service.scrape_product(p)
                time.sleep(0.4)
            self.after(0, self.on_check_all_finished)

        threading.Thread(target=run, daemon=True).start()

    def on_check_all_finished(self):
        self.is_checking = False
        self.btn_check_all.config(state=tk.NORMAL, text="🔄 فحص جميع الأسعار الآن")
        self.status_lbl.config(text="✅ اكتمل فحص جميع الأسعار وتحديث السجلات.")
        self.refresh_table()

        alerts = self.service.get_price_drop_alerts()
        if alerts:
            names = "\n• ".join([f"{a['name']}: {a['current_price']} {a['currency']}" for a in alerts])
            messagebox.showinfo("🚨 تنبيه انخفاض الأسعار!", f"المنتجات التالية وصلت إلى أو نزلت عن السعر المستهدف!\n\n• {names}")
