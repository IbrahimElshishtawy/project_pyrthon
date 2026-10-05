#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 4: مولّد كلمات السر وفاحص القوة (Password Generator & Strength Meter)
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

from core.generator_logic import PasswordGeneratorLogic
from ui.password_view import PasswordGeneratorView
from ui.theme import THEME


class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مولّد كلمات السر القوية | Password Generator")
        self.geometry("740x640")
        self.minsize(680, 580)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.logic = PasswordGeneratorLogic()
        self.view = PasswordGeneratorView(self, self.logic)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
