#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 15: لوحة تحليلات البيانات والمبيعات (Executive Analytics Dashboard)
نقطة الدخول الرئيسية للبرنامج (Bootstrap)
معمارية مقسمة: Core (Analytics Engine) + UI (Theme, Custom Charts, Dashboard View)
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

from core.analytics_service import AnalyticsService
from ui.dashboard_view import DashboardView
from ui.theme import THEME


class DataDashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لوحة تحليلات البيانات والمبيعات | Executive Analytics Dashboard")
        self.geometry("980x750")
        self.minsize(880, 680)
        self.configure(bg=THEME["bg_dark"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.service = AnalyticsService()
        self.view = DashboardView(self, self.service)


if __name__ == "__main__":
    app = DataDashboardApp()
    app.mainloop()
