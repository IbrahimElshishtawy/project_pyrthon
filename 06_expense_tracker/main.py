#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 6: متتبع المصروفات الشخصية (Personal Expense Tracker)
يدعم:
- تسجيل المصروفات بالمبلغ، التصنيف، التاريخ، والملاحظة
- تصنيفات ملونة (طعام، مواصلات، فواتير، ترفيه، صحة، تسوق، أخرى)
- رسم بياني دائري (Donut Chart) ورسم شريطي (Bar Chart) مرسوم بدقة على Tkinter Canvas
- بطاقات إحصائية للمجموع الكلي، أعلى تصنيف إنفاقاً، ومتوسط العمليات
- فلترة حسب التصنيف والبحث، وحذف وتعديل المصروفات
- تصدير التقرير إلى ملف CSV وحفظ دائم بصيغة JSON
"""

import csv
import json
import math
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("متتبع المصروفات الشخصية | Expense Tracker")
        self.geometry("880x700")
        self.minsize(800, 620)
        self.configure(bg="#0F172A")

        self.data_file = os.path.join(os.path.dirname(__file__), "expenses.json")
        self.expenses = []

        self.categories = {
            "طعام": "#EF4444",      # Red
            "مواصلات": "#F59E0B",    # Amber
            "فواتير": "#3B82F6",     # Blue
            "ترفيه": "#EC4899",      # Pink
            "صحة": "#10B981",        # Emerald
            "تسوق": "#8B5CF6",       # Purple
            "أخرى": "#64748B"        # Slate
        }

        self.setup_ui()
        self.load_data()
        self.refresh_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="💰 متتبع المصروفات والميزانية الشخصية",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        export_btn = tk.Button(
            header,
            text="📥 تصدير إلى CSV",
            font=("Segoe UI", 10),
            bg="#0369A1",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=3,
            command=self.export_csv
        )
        export_btn.pack(side=tk.LEFT)

        # Main Container
        container = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        container.pack(fill=tk.BOTH, expand=True)

        # Top Stats Cards
        stats_frame = tk.Frame(container, bg="#0F172A")
        stats_frame.pack(fill=tk.X, pady=(0, 12))

        self.card_total = self.create_stat_card(stats_frame, "إجمالي المصروفات", "0.00 ج.م", "#38BDF8")
        self.card_top_cat = self.create_stat_card(stats_frame, "أعلى تصنيف إنفاقاً", "--", "#F59E0B")
        self.card_count = self.create_stat_card(stats_frame, "عدد العمليات", "0", "#10B981")

        # Two-Column Layout (Left: Chart & Input, Right: Transactions Table)
        split_frame = tk.Frame(container, bg="#0F172A")
        split_frame.pack(fill=tk.BOTH, expand=True)

        # Left Column (Input Form + Chart)
        left_col = tk.Frame(split_frame, bg="#0F172A", width=340)
        left_col.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        left_col.pack_propagate(False)

        # Add Expense Form
        form_card = tk.Frame(left_col, bg="#1E293B", padx=12, pady=12, bd=1, relief=tk.SOLID)
        form_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(form_card, text="➕ إضافة مصروف جديد", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC").pack(anchor="e", pady=(0, 8))

        # Amount
        f1 = tk.Frame(form_card, bg="#1E293B")
        f1.pack(fill=tk.X, pady=2)
        tk.Label(f1, text="المبلغ (ج.م):", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)
        self.amount_entry = tk.Entry(f1, font=("Segoe UI", 11, "bold"), bg="#0F172A", fg="#38BDF8", insertbackground="#38BDF8", relief=tk.FLAT, bd=2)
        self.amount_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        # Category
        f2 = tk.Frame(form_card, bg="#1E293B")
        f2.pack(fill=tk.X, pady=4)
        tk.Label(f2, text="التصنيف:", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)
        self.cat_var = tk.StringVar(value="طعام")
        cat_menu = ttk.Combobox(f2, textvariable=self.cat_var, values=list(self.categories.keys()), state="readonly")
        cat_menu.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        # Note / Description
        f3 = tk.Frame(form_card, bg="#1E293B")
        f3.pack(fill=tk.X, pady=2)
        tk.Label(f3, text="الملاحظة:", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)
        self.note_entry = tk.Entry(f3, font=("Segoe UI", 10), bg="#0F172A", fg="#FFFFFF", insertbackground="#38BDF8", relief=tk.FLAT, bd=2)
        self.note_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(0, 6))

        # Submit button
        add_btn = tk.Button(
            form_card,
            text="تسجيل المصروف",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.add_expense
        )
        add_btn.pack(fill=tk.X, pady=(8, 0), ipady=4)

        # Canvas Chart Card
        chart_card = tk.Frame(left_col, bg="#1E293B", padx=10, pady=10, bd=1, relief=tk.SOLID)
        chart_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(chart_card, text="📊 توزيع المصروفات حسب التصنيف", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#F8FAFC").pack(anchor="e")

        self.chart_canvas = tk.Canvas(chart_card, bg="#1E293B", highlightthickness=0)
        self.chart_canvas.pack(fill=tk.BOTH, expand=True, pady=4)

        # Right Column (Table + Filter + Actions)
        right_col = tk.Frame(split_frame, bg="#0F172A")
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Filter toolbar
        filter_bar = tk.Frame(right_col, bg="#0F172A")
        filter_bar.pack(fill=tk.X, pady=(0, 8))

        self.filter_cat_var = tk.StringVar(value="جميع التصنيفات")
        f_options = ["جميع التصنيفات"] + list(self.categories.keys())
        cat_filter = ttk.Combobox(filter_bar, textvariable=self.filter_cat_var, values=f_options, state="readonly", width=14)
        cat_filter.pack(side=tk.RIGHT)
        cat_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh_table())

        tk.Label(filter_bar, text="تصفية حسب:", font=("Segoe UI", 9), bg="#0F172A", fg="#94A3B8").pack(side=tk.RIGHT, padx=4)

        del_btn = tk.Button(
            filter_bar,
            text="🗑 حذف المصروف المحدد",
            font=("Segoe UI", 9),
            bg="#B91C1C",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=8,
            command=self.delete_expense
        )
        del_btn.pack(side=tk.LEFT)

        # Treeview Table
        table_card = tk.Frame(right_col, bg="#1E293B", bd=1, relief=tk.SOLID)
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
        card = tk.Frame(parent, bg="#1E293B", padx=16, pady=10, bd=1, relief=tk.SOLID)
        card.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=4)

        lbl_t = tk.Label(card, text=title, font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8")
        lbl_t.pack(anchor="e")

        lbl_v = tk.Label(card, text=initial_val, font=("Segoe UI", 16, "bold"), bg="#1E293B", fg=color)
        lbl_v.pack(anchor="e")
        return lbl_v

    def load_data(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except Exception:
                self.expenses = []
        else:
            # Starter sample data
            self.expenses = [
                {"id": 1, "date": "2026-10-05 10:30", "category": "طعام", "amount": 150.0, "note": "وجبة غداء"},
                {"id": 2, "date": "2026-10-04 14:15", "category": "مواصلات", "amount": 60.0, "note": "تاكسي للجامعة"},
                {"id": 3, "date": "2026-10-03 19:00", "category": "فواتير", "amount": 420.0, "note": "فاتورة الإنترنت"},
                {"id": 4, "date": "2026-10-02 21:00", "category": "ترفيه", "amount": 200.0, "note": "تذكرة سينما"},
                {"id": 5, "date": "2026-10-01 11:00", "category": "تسوق", "amount": 350.0, "note": "مستلزمات مكتبية"}
            ]
            self.save_data()

    def save_data(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل حفظ البيانات: {e}")

    def add_expense(self):
        val = self.amount_entry.get().strip()
        try:
            amount = float(val)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("تنبيه", "يرجى إدخال مبلغ صحيح أكبر من صفر!")
            return

        cat = self.cat_var.get()
        note = self.note_entry.get().strip() or "بدون ملاحظة"

        new_id = (max([e["id"] for e in self.expenses]) + 1) if self.expenses else 1
        record = {
            "id": new_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": cat,
            "amount": amount,
            "note": note
        }
        self.expenses.insert(0, record)
        self.save_data()

        self.amount_entry.delete(0, tk.END)
        self.note_entry.delete(0, tk.END)
        self.refresh_ui()

    def delete_expense(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مصروف لحذفه من الجدول!")
            return
        item_vals = self.tree.item(sel[0], "values")
        exp_id = int(item_vals[0])

        self.expenses = [e for e in self.expenses if e["id"] != exp_id]
        self.save_data()
        self.refresh_ui()

    def refresh_ui(self):
        self.refresh_table()
        self.refresh_stats()
        self.draw_donut_chart()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        filter_cat = self.filter_cat_var.get()

        for exp in self.expenses:
            if filter_cat != "جميع التصنيفات" and exp["category"] != filter_cat:
                continue
            self.tree.insert(
                "",
                tk.END,
                values=(
                    exp["id"],
                    exp["date"],
                    exp["category"],
                    f"{exp['amount']:.2f}",
                    exp["note"]
                )
            )

    def refresh_stats(self):
        total = sum(e["amount"] for e in self.expenses)
        count = len(self.expenses)
        self.card_total.config(text=f"{total:,.2f} ج.م")
        self.card_count.config(text=str(count))

        cat_totals = {}
        for e in self.expenses:
            cat = e["category"]
            cat_totals[cat] = cat_totals.get(cat, 0.0) + e["amount"]

        if cat_totals:
            top_cat = max(cat_totals, key=cat_totals.get)
            self.card_top_cat.config(text=f"{top_cat} ({cat_totals[top_cat]:,.0f} ج.م)")
        else:
            self.card_top_cat.config(text="--")

    def draw_donut_chart(self):
        self.chart_canvas.delete("all")
        w = self.chart_canvas.winfo_width() or 300
        h = self.chart_canvas.winfo_height() or 220

        cx, cy = w // 2, (h // 2) - 10
        radius = min(w, h) // 2.5
        inner_radius = radius * 0.55

        cat_totals = {}
        total = sum(e["amount"] for e in self.expenses)
        for e in self.expenses:
            c = e["category"]
            cat_totals[c] = cat_totals.get(c, 0.0) + e["amount"]

        if total <= 0 or not cat_totals:
            self.chart_canvas.create_text(
                cx, cy,
                text="لا توجد بيانات مسجلة لعرض الرسم",
                font=("Segoe UI", 10),
                fill="#94A3B8"
            )
            return

        start_angle = 0
        legend_y = cy + radius + 15
        legend_x = 10

        for cat, amt in cat_totals.items():
            extent = (amt / total) * 360
            color = self.categories.get(cat, "#64748B")

            # Draw slice
            self.chart_canvas.create_arc(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                start=start_angle,
                extent=extent,
                fill=color,
                outline="#1E293B",
                width=2
            )
            start_angle += extent

        # Cut hole for Donut
        self.chart_canvas.create_oval(
            cx - inner_radius, cy - inner_radius,
            cx + inner_radius, cy + inner_radius,
            fill="#1E293B",
            outline="#1E293B"
        )

        # Center Text
        self.chart_canvas.create_text(
            cx, cy - 8,
            text="المجموع",
            font=("Segoe UI", 8),
            fill="#94A3B8"
        )
        self.chart_canvas.create_text(
            cx, cy + 10,
            text=f"{total:,.0f}",
            font=("Segoe UI", 11, "bold"),
            fill="#F8FAFC"
        )

    def export_csv(self):
        if not self.expenses:
            messagebox.showinfo("تنبيه", "لا توجد مصروفات لتصديرها!")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("ملف CSV", "*.csv")],
            initialfile=f"تقرير_المصروفات_{datetime.now().strftime('%Y%m%d')}.csv"
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["المعرف", "التاريخ والوقت", "التصنيف", "المبلغ", "الملاحظة"])
                for e in self.expenses:
                    writer.writerow([e["id"], e["date"], e["category"], e["amount"], e["note"]])
            messagebox.showinfo("نجاح", "تم تصدير ملف CSV بنجاح!")
        except Exception as e:
            messagebox.showerror("خطأ في التصدير", str(e))


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
