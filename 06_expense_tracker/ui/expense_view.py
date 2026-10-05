# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمتتبع المصروفات
"""

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from ui.theme import THEME
from ui.charts import draw_donut_chart


class ExpenseView(tk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=THEME["bg"])
        self.manager = manager

        self.setup_ui()
        self.refresh_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="💰 متتبع المصروفات والميزانية الشخصية",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        export_btn = tk.Button(
            header,
            text="📥 تصدير إلى CSV",
            font=(THEME["font_family"], 10),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=3,
            command=self.on_export_csv
        )
        export_btn.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Top KPI Cards
        stats_frame = tk.Frame(body, bg=THEME["bg"])
        stats_frame.pack(fill=tk.X, pady=(0, 12))

        self.card_total = self.create_stat_card(stats_frame, "إجمالي المصروفات", "0.00 ج.م", THEME["accent_cyan"])
        self.card_top_cat = self.create_stat_card(stats_frame, "أعلى تصنيف إنفاقاً", "--", THEME["gold"])
        self.card_count = self.create_stat_card(stats_frame, "عدد العمليات", "0", THEME["success"])

        # Split: Left (Form + Chart), Right (Table)
        split_frame = tk.Frame(body, bg=THEME["bg"])
        split_frame.pack(fill=tk.BOTH, expand=True)

        # Left Column
        left_col = tk.Frame(split_frame, bg=THEME["bg"], width=340)
        left_col.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        left_col.pack_propagate(False)

        # Form
        form_card = tk.Frame(left_col, bg=THEME["surface"], padx=12, pady=12, bd=1, relief=tk.SOLID)
        form_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(form_card, text="➕ إضافة مصروف جديد", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 8))

        f1 = tk.Frame(form_card, bg=THEME["surface"])
        f1.pack(fill=tk.X, pady=2)
        tk.Label(f1, text="المبلغ (ج.م):", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.amount_entry = tk.Entry(f1, font=(THEME["font_family"], 11, "bold"), bg=THEME["bg"], fg=THEME["accent_cyan"], insertbackground=THEME["accent_cyan"], relief=tk.FLAT, bd=2)
        self.amount_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        f2 = tk.Frame(form_card, bg=THEME["surface"])
        f2.pack(fill=tk.X, pady=4)
        tk.Label(f2, text="التصنيف:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.cat_var = tk.StringVar(value="طعام")
        cat_menu = ttk.Combobox(f2, textvariable=self.cat_var, values=list(self.manager.CATEGORIES.keys()), state="readonly")
        cat_menu.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        f3 = tk.Frame(form_card, bg=THEME["surface"])
        f3.pack(fill=tk.X, pady=2)
        tk.Label(f3, text="الملاحظة:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        self.note_entry = tk.Entry(f3, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["accent_cyan"], relief=tk.FLAT, bd=2)
        self.note_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        btn_add = tk.Button(
            form_card,
            text="تسجيل المصروف",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_add_expense
        )
        btn_add.pack(fill=tk.X, pady=(8, 0), ipady=4)

        # Donut Chart
        chart_card = tk.Frame(left_col, bg=THEME["surface"], padx=10, pady=10, bd=1, relief=tk.SOLID)
        chart_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(chart_card, text="📊 توزيع المصروفات حسب التصنيف", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e")

        self.chart_canvas = tk.Canvas(chart_card, bg=THEME["surface"], highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=4)

        # Right Column
        right_col = tk.Frame(split_frame, bg=THEME["bg"])
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        filter_bar = tk.Frame(right_col, bg=THEME["bg"])
        filter_bar.pack(fill=tk.X, pady=(0, 8))

        self.filter_cat_var = tk.StringVar(value="جميع التصنيفات")
        f_options = ["جميع التصنيفات"] + list(self.manager.CATEGORIES.keys())
        cat_filter = ttk.Combobox(filter_bar, textvariable=self.filter_cat_var, values=f_options, state="readonly", width=14)
        cat_filter.pack(side=tk.RIGHT)
        cat_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        tk.Label(filter_bar, text="تصفية حسب:", font=(THEME["font_family"], 9), bg=THEME["bg"], fg=THEME["text_muted"]).pack(side=tk.RIGHT, padx=4)

        del_btn = tk.Button(
            filter_bar,
            text="🗑 حذف المصروف المحدد",
            font=(THEME["font_family"], 9),
            bg=THEME["danger"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            command=self.on_delete_expense
        )
        del_btn.pack(side=tk.LEFT)

        # Table
        table_card = tk.Frame(right_col, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "date", "category", "amount", "note")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="#")
        self.tree.heading("date", text="التاريخ والوقت")
        self.tree.heading("category", text="التصنيف")
        self.tree.heading("amount", text="المبلغ (ج.م)")
        self.tree.heading("note", text="الملاحظة والبيان")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("date", width=130, anchor="center")
        self.tree.column("category", width=90, anchor="center")
        self.tree.column("amount", width=90, anchor="center")
        self.tree.column("note", width=180, anchor="w")

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def create_stat_card(self, parent, title, initial_val, color):
        card = tk.Frame(parent, bg=THEME["surface"], padx=16, pady=10, bd=1, relief=tk.SOLID)
        card.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=4)
        lbl_t = tk.Label(card, text=title, font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"])
        lbl_t.pack(anchor="e")
        lbl_v = tk.Label(card, text=initial_val, font=(THEME["font_family"], 16, "bold"), bg=THEME["surface"], fg=color)
        lbl_v.pack(anchor="e")
        return lbl_v

    def refresh_ui(self):
        self.refresh_table()
        self.refresh_stats()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        filter_cat = self.filter_cat_var.get()
        for exp in self.manager.expenses:
            if filter_cat != "جميع التصنيفات" and exp["category"] != filter_cat:
                continue
            self.tree.insert("", tk.END, values=(exp["id"], exp["date"], exp["category"], f"{exp['amount']:.2f}", exp["note"]))

    def refresh_stats(self):
        summary = self.manager.get_summary()
        self.card_total.config(text=f"{summary['total']:,.2f} ج.م")
        self.card_count.config(text=str(summary['count']))
        if summary['top_cat'] != "--":
            self.card_top_cat.config(text=f"{summary['top_cat']} ({summary['top_cat_amount']:,.0f} ج.م)")
        else:
            self.card_top_cat.config(text="--")

        draw_donut_chart(self.chart_canvas, summary['cat_totals'], self.manager.CATEGORIES, summary['total'])

    def on_add_expense(self):
        val = self.amount_entry.get().strip()
        try:
            amt = float(val)
            if amt <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("تنبيه", "يرجى إدخال مبلغ صحيح أكبر من صفر!")
            return

        cat = self.cat_var.get()
        note = self.note_entry.get().strip() or "بدون ملاحظة"
        self.manager.add_expense(amt, cat, note)

        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.refresh_ui()

    def on_delete_expense(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مصروف لحذفه من الجدول!")
            return
        exp_id = int(self.tree.item(sel[0], "values")[0])
        self.manager.delete_expense(exp_id)
        self.refresh_ui()

    def on_export_csv(self):
        if not self.manager.expenses:
            messagebox.showinfo("تنبيه", "لا توجد مصروفات لتصديرها!")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("ملف CSV", "*.csv")], initialfile=f"تقرير_المصروفات_{datetime.now().strftime('%Y%m%d')}.csv")
        if path:
            try:
                self.manager.export_csv(path)
                messagebox.showinfo("نجاح", "تم تصدير ملف CSV بنجاح!")
            except Exception as e:
                messagebox.showerror("خطأ", str(e))
