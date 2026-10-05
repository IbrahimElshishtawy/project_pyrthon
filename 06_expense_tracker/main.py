#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 6: متتبع المصروفات الشخصية (Personal Expense Tracker)
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

from core.expense_manager import ExpenseManager
from ui.expense_view import ExpenseView
from ui.theme import THEME


class ExpenseTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("متتبع المصروفات الشخصية | Expense Tracker")
        self.geometry("900x700")
        self.minsize(820, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.manager = ExpenseManager()
        self.view = ExpenseView(self, self.manager)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
