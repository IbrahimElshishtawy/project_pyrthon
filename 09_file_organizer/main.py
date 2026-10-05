#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 9: منظم الملفات التلقائي الذكي (Automated File Organizer)
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

from core.organizer_engine import FileOrganizerEngine
from ui.organizer_view import FileOrganizerView
from ui.theme import THEME


class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("منظم الملفات التلقائي | File Organizer")
        self.geometry("880x700")
        self.minsize(820, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.engine = FileOrganizerEngine()
        self.view = FileOrganizerView(self, self.engine)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
