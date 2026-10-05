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
ألوان وتصميم لوحة تحكم البيانات
"""

THEME = {
    "bg": "#0F172A",
    "bg_dark": "#0F172A",
    "panel_bg": "#1E293B",
    "surface": "#1E293B",
    "surface_light": "#334155",
    "card_bg": "#334155",
    "primary": "#0284C7",
    "accent": "#38BDF8",
    "accent_cyan": "#38BDF8",
    "success": "#10B981",
    "warning": "#F59E0B",
    "gold": "#F59E0B",
    "pink": "#EC4899",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "font_family": FONT_FAMILY
}
