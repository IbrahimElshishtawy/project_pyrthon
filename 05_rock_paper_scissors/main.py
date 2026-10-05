#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 5: لعبة حجر ورقة مقص التفاعلية (Rock Paper Scissors Deluxe)
نقطة الدخول الرئيسية للبرنامج (Bootstrap)
"""

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from arabic_helper import enable_arabic_support
    enable_arabic_support()
except Exception:
    pass

from core.game_rules import RockPaperScissorsEngine
from ui.game_view import RockPaperScissorsView
from ui.theme import THEME


class RockPaperScissorsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لعبة حجر ورقة مقص | Rock Paper Scissors")
        self.geometry("780x660")
        self.minsize(700, 600)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.engine = RockPaperScissorsEngine()
        self.view = RockPaperScissorsView(self, self.engine)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()
