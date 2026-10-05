#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 8: لوحة تحكم ومحاكي بوت تيليجرام (Telegram Bot Manager)
نقطة الدخول الرئيسية للبرنامج (Bootstrap)
"""

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.bot_service import TelegramBotService
from ui.bot_view import TelegramBotView
from ui.theme import THEME


class TelegramBotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لوحة تحكم ومحاكي بوت تيليجرام | Telegram Bot Manager")
        self.geometry("940x720")
        self.minsize(860, 640)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.service = TelegramBotService()
        self.view = TelegramBotView(self, self.service)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = TelegramBotApp()
    app.mainloop()
