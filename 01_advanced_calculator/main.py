#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 1: حاسبة علمية متقدمة (Advanced Scientific Calculator)
نقطة الدخول الرئيسية للبرنامج (Application Bootstrap)
"""

import sys
import os
import tkinter as tk

# Ensure local modules can be imported directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.calc_engine import CalculatorEngine
from ui.calc_view import CalculatorView
from ui.theme import THEME


class AdvancedCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("حاسبة متقدمة | Advanced Calculator")
        self.geometry("800x580")
        self.minsize(700, 520)
        self.configure(bg=THEME["bg"])

        # Enable high-DPI scaling where supported
        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.engine = CalculatorEngine()
        self.view = CalculatorView(self, self.engine)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = AdvancedCalculatorApp()
    app.mainloop()
