#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 3: مدير المهام اليومية الذكي (To-Do List Task Manager)
نقطة الدخول الرئيسية للبرنامج (Bootstrap)
"""

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.task_manager import TaskManager
from ui.todo_view import TodoView
from ui.theme import THEME


class TodoManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدير المهام الاحترافي | Task Manager")
        self.geometry("840x660")
        self.minsize(760, 600)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        self.manager = TaskManager()
        self.view = TodoView(self, self.manager)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = TodoManagerApp()
    app.mainloop()
