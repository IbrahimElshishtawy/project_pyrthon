#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 10: مختصر الروابط مع SQLite وخادم محلي مدمج
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

from core.database import URLDatabase
from core.redirect_server import RedirectServer
from ui.shortener_view import URLShortenerView
from ui.theme import THEME


class URLShortenerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مختصر الروابط الاحترافي | URL Shortener")
        self.geometry("940x700")
        self.minsize(860, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.db = URLDatabase()
        self.view = URLShortenerView(self, self.db, port=8000)
        self.view.pack(fill=tk.BOTH, expand=True)

        self.server = RedirectServer(self.db, port=8000, on_click_callback=lambda: self.after(0, self.view.refresh_table))
        self.server.start()


if __name__ == "__main__":
    app = URLShortenerApp()
    app.mainloop()
