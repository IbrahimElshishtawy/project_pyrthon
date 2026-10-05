# -*- coding: utf-8 -*-
"""
رسم الرسوم البيانية التفاعلية للوحة التحكم (Bar Chart & Donut Chart)
"""

def draw_monthly_bar_chart(canvas, month_totals, month_order):
    canvas.delete("all")
    w = canvas.winfo_width() or 460
    h = canvas.winfo_height() or 180

    max_val = max(month_totals.values()) if month_totals and max(month_totals.values()) > 0 else 1
    margin_left = 30
    margin_bottom = 25
    chart_w = w - margin_left - 20
    chart_h = h - margin_bottom - 20

    bar_width = chart_w / (len(month_order) * 1.5)

    for i, m in enumerate(month_order):
        val = month_totals.get(m, 0)
        bar_h = (val / max_val) * chart_h
        x1 = margin_left + i * (bar_width * 1.5)
        y1 = h - margin_bottom - bar_h
        x2 = x1 + bar_width
        y2 = h - margin_bottom

        canvas.create_rectangle(x1, y1, x2, y2, fill="#38BDF8", outline="")
        canvas.create_text(x1 + bar_width / 2, h - margin_bottom + 12, text=m, font=("Segoe UI", 7), fill="#94A3B8")


def draw_category_donut_chart(canvas, cat_totals):
    canvas.delete("all")
    w = canvas.winfo_width() or 340
    h = canvas.winfo_height() or 180

    cx, cy = w // 2, (h // 2) - 5
    radius = min(w, h) // 2.5
    inner = radius * 0.55

    colors = ["#38BDF8", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]
    total = sum(cat_totals.values())

    if total <= 0:
        canvas.create_text(cx, cy, text="لا توجد بيانات", fill="#94A3B8", font=("Segoe UI", 9))
        return

    start = 0
    for i, (cat, val) in enumerate(cat_totals.items()):
        ext = (val / total) * 360
        color = colors[i % len(colors)]
        canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=start, extent=ext, fill=color, outline="#1E293B", width=2)
        start += ext

    canvas.create_oval(cx - inner, cy - inner, cx + inner, cy + inner, fill="#1E293B", outline="#1E293B")
    canvas.create_text(cx, cy, text=f"${total:,.0f}", fill="#F8FAFC", font=("Segoe UI", 10, "bold"))
