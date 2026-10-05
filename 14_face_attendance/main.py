#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 14: منظومة تسجيل الحضور بالبصمة الوجهية (Face Recognition Attendance)
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

from core.attendance_service import AttendanceService
from ui.attendance_view import AttendanceView
from ui.theme import THEME


class FaceAttendanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("نظام التعرف على الوجوه وتسجيل الحضور | Face Attendance System")
        self.geometry("1000x740")
        self.minsize(920, 660)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.service = AttendanceService()
        self.view = AttendanceView(self, self.service)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = FaceAttendanceApp()
    app.mainloop()
