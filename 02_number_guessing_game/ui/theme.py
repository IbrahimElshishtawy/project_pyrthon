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
رموز وألوان تصميم لعبة تخمين الرقم
"""

THEME = {
    "bg": "#0B132B",          # Deep midnight navy
    "surface": "#1C2541",     # Elevated card
    "surface_light": "#3A506B",
    "accent_cyan": "#6FFFE9", # Glowing cyan
    "accent_blue": "#48CAE4",
    "text_main": "#F8FAFC",
    "text_muted": "#94A3B8",
    "gold": "#FCD34D",
    "success": "#4ADE80",
    "danger": "#F87171",
    "font_family": FONT_FAMILY
}
