#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 2: لعبة تخمين الرقم الذكية (Number Guessing Game)
نقطة الدخول الرئيسية (Bootstrap)
"""

import sys
import os
import tkinter as tk

# Ensure local module path resolution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from arabic_helper import enable_arabic_support
    enable_arabic_support()
except Exception:
    pass

from core.game_logic import NumberGuessingGameLogic
from ui.game_view import NumberGuessingGameView
from ui.theme import THEME


class NumberGuessingGameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لعبة تخمين الرقم الذكية | Number Guessing Game")
        self.geometry("720x640")
        self.minsize(640, 580)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.logic = NumberGuessingGameLogic()
        self.view = NumberGuessingGameView(self, self.logic)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = NumberGuessingGameApp()
    app.mainloop()
