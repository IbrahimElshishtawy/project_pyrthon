# -*- coding: utf-8 -*-
"""
رسم عداد ومقياس سرعة المشاعر (Speedometer Gauge)
"""

import math
import tkinter as tk


def draw_sentiment_gauge(canvas, score):
    canvas.delete("all")
    cx, cy = 130, 115
    radius = 90

    # Red segment (Negative): 120 to 180 deg
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=120, extent=60, fill="#EF4444", outline="#1E293B", width=2)
    # Amber segment (Neutral): 60 to 120 deg
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=60, extent=60, fill="#F59E0B", outline="#1E293B", width=2)
    # Green segment (Positive): 0 to 60 deg
    canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=0, extent=60, fill="#10B981", outline="#1E293B", width=2)

    # Cut donut center
    inner = 55
    canvas.create_oval(cx - inner, cy - inner, cx + inner, cy + inner, fill="#1E293B", outline="#1E293B")

    # Needle
    angle_deg = 90 - (score * 90)
    angle_rad = math.radians(angle_deg)

    nx = cx + (radius - 15) * math.cos(angle_rad)
    ny = cy - (radius - 15) * math.sin(angle_rad)

    canvas.create_line(cx, cy, nx, ny, fill="#F8FAFC", width=3, arrow=tk.LAST)
    canvas.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill="#38BDF8", outline="#FFFFFF")
