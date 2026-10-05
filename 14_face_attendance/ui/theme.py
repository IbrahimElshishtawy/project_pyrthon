import sys
import os

_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _root not in sys.path:
    sys.path.insert(0, _root)

try:
    from arabic_helper import FONT_FAMILY, ar, get_font
except Exception:
    FONT_FAMILY = "Noto Sans Arabic" if sys.platform.startswith("linux") else "Segoe UI"
    def ar(x): return x
    def get_font(s=10, w="normal"): return (FONT_FAMILY, s, w) if w == "bold" else (FONT_FAMILY, s)

# -*- coding: utf-8 -*-
"""
ألوان وتصميم منظومة تسجيل الحضور
"""

THEME = {
    "bg": "#0B0F19",
    "surface": "#111827",
    "surface_card": "#1F2937",
    "surface_light": "#374151",
    "accent_cyan": "#38BDF8",
    "primary": "#0284C7",
    "success": "#10B981",
    "danger": "#EF4444",
    "gold": "#F59E0B",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "font_family": FONT_FAMILY
}
