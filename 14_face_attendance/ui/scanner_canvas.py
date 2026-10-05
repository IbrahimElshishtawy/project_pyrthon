# -*- coding: utf-8 -*-
"""
رسم وتحديث شاشة الماسح البيومتري على Canvas
"""

def draw_biometric_hud(canvas, scan_y, width=380, height=260):
    canvas.delete("all")
    cx, cy = width // 2, height // 2

    # Face box bounds
    bx1, by1 = cx - 80, cy - 85
    bx2, by2 = cx + 80, cy + 85

    # Reticles
    clen = 20
    # Top-Left
    canvas.create_line(bx1, by1, bx1 + clen, by1, fill="#38BDF8", width=3)
    canvas.create_line(bx1, by1, bx1, by1 + clen, fill="#38BDF8", width=3)
    # Top-Right
    canvas.create_line(bx2, by1, bx2 - clen, by1, fill="#38BDF8", width=3)
    canvas.create_line(bx2, by1, bx2, by1 + clen, fill="#38BDF8", width=3)
    # Bottom-Left
    canvas.create_line(bx1, by2, bx1 + clen, by2, fill="#38BDF8", width=3)
    canvas.create_line(bx1, by2, bx1, by2 - clen, fill="#38BDF8", width=3)
    # Bottom-Right
    canvas.create_line(bx2, by2, bx2 - clen, by2, fill="#38BDF8", width=3)
    canvas.create_line(bx2, by2, bx2, by2 - clen, fill="#38BDF8", width=3)

    # Face silhouette
    canvas.create_oval(cx - 30, cy - 65, cx + 30, cy - 5, outline="#475569", width=2)
    canvas.create_arc(cx - 60, cy - 10, cx + 60, cy + 90, start=0, extent=180, outline="#475569", width=2)

    # Scan laser line
    canvas.create_line(bx1 - 10, scan_y, bx2 + 10, scan_y, fill="#38BDF8", width=2)

    # HUD info
    canvas.create_text(15, 15, text="REC ● 60FPS", font=("Consolas", 8, "bold"), fill="#EF4444", anchor="w")
    canvas.create_text(width - 15, 15, text="AI BIOMETRIC: ACTIVE", font=("Consolas", 8), fill="#10B981", anchor="e")
    canvas.create_text(cx, height - 15, text="[ تم التعرف على البصمة الوجهية بنجاح 99.4% ]", font=("Segoe UI", 9, "bold"), fill="#38BDF8")
