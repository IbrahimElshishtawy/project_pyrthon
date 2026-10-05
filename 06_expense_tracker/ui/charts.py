# -*- coding: utf-8 -*-
"""
رسم بياني دائري (Donut Chart) على Tkinter Canvas
"""

def draw_donut_chart(canvas, cat_totals, categories_colors, total_amount):
    canvas.delete("all")
    w = canvas.winfo_width() or 300
    h = canvas.winfo_height() or 220

    cx, cy = w // 2, (h // 2) - 10
    radius = min(w, h) // 2.5
    inner_radius = radius * 0.55

    if total_amount <= 0 or not cat_totals:
        canvas.create_text(
            cx, cy,
            text="لا توجد بيانات مسجلة لعرض الرسم",
            font=("Segoe UI", 10),
            fill="#94A3B8"
        )
        return

    start_angle = 0
    for cat, amt in cat_totals.items():
        extent = (amt / total_amount) * 360
        color = categories_colors.get(cat, "#64748B")

        canvas.create_arc(
            cx - radius, cy - radius,
            cx + radius, cy + radius,
            start=start_angle,
            extent=extent,
            fill=color,
            outline="#1E293B",
            width=2
        )
        start_angle += extent

    # Cut donut hole
    canvas.create_oval(
        cx - inner_radius, cy - inner_radius,
        cx + inner_radius, cy + inner_radius,
        fill="#1E293B",
        outline="#1E293B"
    )

    canvas.create_text(
        cx, cy - 8,
        text="المجموع",
        font=("Segoe UI", 8),
        fill="#94A3B8"
    )
    canvas.create_text(
        cx, cy + 10,
        text=f"{total_amount:,.0f}",
        font=("Segoe UI", 11, "bold"),
        fill="#F8FAFC"
    )
