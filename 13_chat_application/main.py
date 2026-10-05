#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 13: تطبيق الدردشة الفورية المتعدد (Real-Time Socket Chat)
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

from core.chat_network import ChatNetwork
from ui.chat_view import ChatView
from ui.theme import THEME


class ChatApplicationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("تطبيق الدردشة الفورية | Real-Time Chat")
        self.geometry("920x700")
        self.minsize(840, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.network = ChatNetwork()
        self.view = ChatView(self, self.network)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = ChatApplicationApp()
    app.mainloop()
