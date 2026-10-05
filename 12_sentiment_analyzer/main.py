#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 12: محلل مشاعر النصوص والتعليقات (Sentiment Analyzer)
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

from core.sentiment_engine import SentimentEngine
from ui.sentiment_view import SentimentAnalyzerView
from ui.theme import THEME


class SentimentAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("محلل مشاعر النصوص والتعليقات | Sentiment Analyzer")
        self.geometry("920x720")
        self.minsize(840, 640)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.engine = SentimentEngine()
        self.view = SentimentAnalyzerView(self, self.engine)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = SentimentAnalyzerApp()
    app.mainloop()
