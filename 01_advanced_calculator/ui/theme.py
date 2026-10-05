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
رموز وألوان وأنماط التصميم لحاسبة متقدمة
"""

THEME = {
    "bg": "#0B1120",            # Deep Luxury Slate
    "card": "#1E293B",          # Elevated Surface
    "card_border": "#334155",
    "display_bg": "#030712",    # Pitch display
    "display_text": "#F8FAFC",
    "display_sub": "#94A3B8",
    "num_btn": "#1E293B",
    "num_hover": "#334155",
    "op_btn": "#6366F1",        # Electric Indigo
    "op_hover": "#4F46E5",
    "func_btn": "#0F172A",
    "func_hover": "#1E293B",
    "action_btn": "#EF4444",    # Crimson Red
    "action_hover": "#DC2626",
    "equal_btn": "#10B981",     # Neon Emerald
    "equal_hover": "#059669",
    "text": "#FFFFFF",
    "font_family": FONT_FAMILY
}
