# -*- coding: utf-8 -*-
"""
واجهة لوحة البيانات والتحليلات التنفيذية المتطورة (Interactive Executive Dashboard)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ui.theme import THEME
from ui.charts import draw_monthly_bar_chart, draw_category_donut_chart


class DashboardView(tk.Frame):
    def __init__(self, parent, analytics_service):
        super().__init__(parent, bg=THEME["bg_dark"])
        self.service = analytics_service
        self.pack(fill=tk.BOTH, expand=True)

        self._create_header()
        self._create_filter_toolbar()
        self._create_kpi_row()
        self._create_charts_area()
        self._create_table_area()

        self.refresh_dashboard()

    def _create_header(self):
        header = tk.Frame(self, bg=THEME["panel_bg"], height=65)
        header.pack(fill=tk.X, padx=15, pady=(15, 10))

        title_box = tk.Frame(header, bg=THEME["panel_bg"])
        title_box.pack(side=tk.RIGHT, padx=15, pady=10)

        tk.Label(
            title_box,
            text="📊 لوحة تحليلات المبيعات التنفيذية",
            font=("Segoe UI", 16, "bold"),
            fg=THEME["text_main"],
            bg=THEME["panel_bg"]
        ).pack(anchor="e")

        tk.Label(
            title_box,
            text="Business Intelligence & Executive Sales Analytics Dashboard",
            font=("Segoe UI", 9),
            fg=THEME["accent"],
            bg=THEME["panel_bg"]
        ).pack(anchor="e")

        actions_box = tk.Frame(header, bg=THEME["panel_bg"])
        actions_box.pack(side=tk.LEFT, padx=15, pady=10)

        tk.Button(
            actions_box,
            text="📥 استيراد CSV",
            font=("Segoe UI", 9, "bold"),
            bg="#334155",
            fg=THEME["text_main"],
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._handle_import
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            actions_box,
            text="📤 تصدير تقرير",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["success"],
            fg=THEME["text_main"],
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self._handle_export
        ).pack(side=tk.LEFT, padx=5)

    def _create_filter_toolbar(self):
        bar = tk.Frame(self, bg=THEME["panel_bg"])
        bar.pack(fill=tk.X, padx=15, pady=(0, 10), ipady=6)

        inner = tk.Frame(bar, bg=THEME["panel_bg"])
        inner.pack(side=tk.RIGHT, padx=15)

        tk.Label(
            inner,
            text="🔍 تصفية حسب:",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["text_main"],
            bg=THEME["panel_bg"]
        ).pack(side=tk.RIGHT, padx=(10, 5))

        # Filter Category
        tk.Label(inner, text="الفئة:", font=("Segoe UI", 9), fg=THEME["text_muted"], bg=THEME["panel_bg"]).pack(side=tk.RIGHT, padx=3)
        self.cat_var = tk.StringVar(value="جميع الفئات")
        cat_options = ["جميع الفئات"] + self.service.CATEGORIES
        self.cat_combo = ttk.Combobox(inner, textvariable=self.cat_var, values=cat_options, state="readonly", width=14)
        self.cat_combo.pack(side=tk.RIGHT, padx=(0, 15))
        self.cat_combo.bind("<<ComboboxSelected>>", lambda e: self._on_filter_changed())

        # Filter Region
        tk.Label(inner, text="المنطقة:", font=("Segoe UI", 9), fg=THEME["text_muted"], bg=THEME["panel_bg"]).pack(side=tk.RIGHT, padx=3)
        self.region_var = tk.StringVar(value="جميع المناطق")
        region_options = ["جميع المناطق"] + self.service.REGIONS
        self.region_combo = ttk.Combobox(inner, textvariable=self.region_var, values=region_options, state="readonly", width=14)
        self.region_combo.pack(side=tk.RIGHT, padx=(0, 10))
        self.region_combo.bind("<<ComboboxSelected>>", lambda e: self._on_filter_changed())

        # Reset button
        tk.Button(
            bar,
            text="🔄 إعادة تعيين",
            font=("Segoe UI", 8, "bold"),
            bg="#334155",
            fg=THEME["accent"],
            relief=tk.FLAT,
            padx=8,
            pady=3,
            cursor="hand2",
            command=self._reset_filters
        ).pack(side=tk.LEFT, padx=15)

    def _create_kpi_row(self):
        row = tk.Frame(self, bg=THEME["bg_dark"])
        row.pack(fill=tk.X, padx=15, pady=(0, 10))

        self.kpi_labels = {}
        cards = [
            ("total_revenue", "💵 إجمالي المبيعات", "$0", THEME["accent"]),
            ("orders_count", "📦 عدد العمليات", "0", THEME["success"]),
            ("aov", "📈 متوسط الطلب", "$0", THEME["warning"]),
            ("total_units", "🏷️ إجمالي الوحدات", "0", "#C084FC"),
        ]

        for i, (key, title, default_val, accent_color) in enumerate(cards):
            card = tk.Frame(row, bg=THEME["panel_bg"], relief=tk.FLAT, bd=0)
            card.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(5 if i > 0 else 0, 5 if i < 3 else 0))

            tk.Frame(card, bg=accent_color, height=3).pack(fill=tk.X)

            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 9),
                fg=THEME["text_muted"],
                bg=THEME["panel_bg"]
            ).pack(anchor="e", padx=12, pady=(8, 2))

            lbl = tk.Label(
                card,
                text=default_val,
                font=("Segoe UI", 15, "bold"),
                fg=THEME["text_main"],
                bg=THEME["panel_bg"]
            )
            lbl.pack(anchor="e", padx=12, pady=(0, 8))
            self.kpi_labels[key] = lbl

    def _create_charts_area(self):
        area = tk.Frame(self, bg=THEME["bg_dark"])
        area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 10))

        # Monthly Bar Chart Frame
        bar_box = tk.Frame(area, bg=THEME["panel_bg"])
        bar_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        bar_header = tk.Frame(bar_box, bg=THEME["panel_bg"])
        bar_header.pack(fill=tk.X, padx=10, pady=(8, 4))
        tk.Label(bar_header, text="📈 اتجاه المبيعات الشهرية", font=("Segoe UI", 10, "bold"), fg=THEME["text_main"], bg=THEME["panel_bg"]).pack(side=tk.RIGHT)

        self.bar_canvas = tk.Canvas(bar_box, bg=THEME["panel_bg"], highlightthickness=0, height=160)
        self.bar_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        self.bar_canvas.bind("<Configure>", lambda e: self._redraw_charts())

        # Category Donut Chart Frame
        donut_box = tk.Frame(area, bg=THEME["panel_bg"], width=300)
        donut_box.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        donut_box.pack_propagate(False)

        donut_header = tk.Frame(donut_box, bg=THEME["panel_bg"])
        donut_header.pack(fill=tk.X, padx=10, pady=(8, 4))
        tk.Label(donut_header, text="🍩 توزيع الفئات", font=("Segoe UI", 10, "bold"), fg=THEME["text_main"], bg=THEME["panel_bg"]).pack(side=tk.RIGHT)

        self.donut_canvas = tk.Canvas(donut_box, bg=THEME["panel_bg"], highlightthickness=0, height=160)
        self.donut_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 8))
        self.donut_canvas.bind("<Configure>", lambda e: self._redraw_charts())

    def _create_table_area(self):
        box = tk.Frame(self, bg=THEME["panel_bg"])
        box.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))

        tbl_header = tk.Frame(box, bg=THEME["panel_bg"])
        tbl_header.pack(fill=tk.X, padx=10, pady=(6, 2))
        tk.Label(tbl_header, text="📋 سجل العمليات التفصيلية", font=("Segoe UI", 10, "bold"), fg=THEME["text_main"], bg=THEME["panel_bg"]).pack(side=tk.RIGHT)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Dashboard.Treeview",
            background="#0F172A",
            foreground="#F8FAFC",
            fieldbackground="#0F172A",
            rowheight=24,
            font=("Segoe UI", 9)
        )
        style.configure(
            "Dashboard.Treeview.Heading",
            background="#334155",
            foreground="#38BDF8",
            font=("Segoe UI", 9, "bold")
        )
        style.map("Dashboard.Treeview", background=[("selected", "#1E40AF")])

        cols = ("id", "month", "region", "category", "units", "unit_price", "revenue")
        self.tree = ttk.Treeview(box, columns=cols, show="headings", style="Dashboard.Treeview", height=5)

        self.tree.heading("id", text="كود الطلب")
        self.tree.heading("month", text="الشهر")
        self.tree.heading("region", text="المنطقة")
        self.tree.heading("category", text="الفئة")
        self.tree.heading("units", text="الكمية")
        self.tree.heading("unit_price", text="سعر الوحدة")
        self.tree.heading("revenue", text="الإجمالي")

        self.tree.column("id", width=90, anchor="center")
        self.tree.column("month", width=70, anchor="center")
        self.tree.column("region", width=110, anchor="center")
        self.tree.column("category", width=110, anchor="center")
        self.tree.column("units", width=60, anchor="center")
        self.tree.column("unit_price", width=90, anchor="center")
        self.tree.column("revenue", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(box, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=(0, 6))
        self.tree.pack(fill=tk.BOTH, expand=True, padx=(0, 10), pady=(0, 6))

    def _on_filter_changed(self):
        cat = self.cat_var.get()
        reg = self.region_var.get()
        self.service.filter_data(category=cat, region=reg)
        self.refresh_dashboard()

    def _reset_filters(self):
        self.cat_var.set("جميع الفئات")
        self.region_var.set("جميع المناطق")
        self.service.filter_data()
        self.refresh_dashboard()

    def _redraw_charts(self):
        m_totals = self.service.get_monthly_totals()
        draw_monthly_bar_chart(self.bar_canvas, m_totals, self.service.MONTHS)

        cat_totals = self.service.get_category_totals()
        draw_category_donut_chart(self.donut_canvas, cat_totals)

    def refresh_dashboard(self):
        # Update KPIs
        kpis = self.service.get_kpis()
        self.kpi_labels["total_revenue"].config(text=f"${kpis['total_revenue']:,.2f}")
        self.kpi_labels["orders_count"].config(text=f"{kpis['orders_count']:,}")
        self.kpi_labels["aov"].config(text=f"${kpis['aov']:,.2f}")
        self.kpi_labels["total_units"].config(text=f"{kpis['total_units']:,}")

        # Redraw charts
        self._redraw_charts()

        # Update Table
        for row in self.tree.get_children():
            self.tree.delete(row)

        for d in self.service.filtered_data[:150]:
            self.tree.insert("", tk.END, values=(
                d["id"],
                d["month"],
                d["region"],
                d["category"],
                d["units"],
                f"${d['unit_price']:,.2f}",
                f"${d['revenue']:,.2f}"
            ))

    def _handle_import(self):
        path = filedialog.askopenfilename(
            title="اختر ملف CSV للبيانات",
            filetypes=[("ملفات CSV", "*.csv"), ("جميع الملفات", "*.*")]
        )
        if path:
            try:
                cnt = self.service.import_csv(path)
                self.refresh_dashboard()
                messagebox.showinfo("نجاح", f"تم استيراد {cnt} سجل بنجاح!")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر استيراد الملف:\n{e}")

    def _handle_export(self):
        path = filedialog.asksaveasfilename(
            title="حفظ تقرير التحليلات",
            defaultextension=".csv",
            filetypes=[("ملف CSV", "*.csv")]
        )
        if path:
            try:
                self.service.export_csv(path)
                messagebox.showinfo("نجاح", f"تم حفظ التقرير في:\n{path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"تعذر تصدير التقرير:\n{e}")
