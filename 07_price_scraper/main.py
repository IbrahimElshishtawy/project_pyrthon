#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 7: متتبع وكاشط أسعار المنتجات (E-Commerce Price Tracker & Scraper)
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

from core.scraper_service import PriceScraperService
from ui.scraper_view import PriceScraperView
from ui.theme import THEME


class PriceScraperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("متتبع أسعار المنتجات | Price Scraper & Tracker")
        self.geometry("920x700")
        self.minsize(840, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.service = PriceScraperService()
        self.view = PriceScraperView(self, self.service)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = PriceScraperApp()
    app.mainloop()
