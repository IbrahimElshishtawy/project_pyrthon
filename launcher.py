#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوابة تشغيل مشاريع بايثون الـ 15 (Master Projects Hub & Launcher)
تتيح تشغيل أي مشروع من المشاريع الـ 15 بنقرة زر واحدة في نافذة مستقلة مع وصف تفصيلي وتصنيف حسب المستوى:
- المستوى المبتدئ (Projects 01 - 05)
- المستوى المتوسط (Projects 06 - 10)
- المستوى المتقدم (Projects 11 - 15)
"""

import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox

from arabic_helper import ar, get_font, FONT_FAMILY, enable_arabic_support

enable_arabic_support()


class MasterLauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("منصة مشاريع بايثون الـ 15 | Python Projects Suite Launcher")
        self.geometry("1020x760")
        self.minsize(920, 680)
        self.configure(bg="#0B0F19")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        self.projects_data = [
            # Beginner
            {
                "level": "مبتدئ",
                "level_color": "#10B981",
                "folder": "01_advanced_calculator",
                "icon": "🧮",
                "title": "حاسبة علمية متقدمة",
                "title_en": "Advanced Scientific Calculator",
                "desc": "تدعم العمليات الأساسية، الأسس والجذور، الدوال المثلثية (sin/cos/tan)، وسجل تفاعلي للعمليات."
            },
            {
                "level": "مبتدئ",
                "level_color": "#10B981",
                "folder": "02_number_guessing_game",
                "icon": "🎯",
                "title": "لعبة تخمين الرقم الذكية",
                "title_en": "Number Guessing Game",
                "desc": "3 مستويات صعوبة، تلميحات ذكية (أعلى/أقل ومقياس حراري 🔥/❄️)، وحساب أفضل نتيجة (High Score)."
            },
            {
                "level": "مبتدئ",
                "level_color": "#10B981",
                "folder": "03_todo_manager",
                "icon": "📋",
                "title": "مدير المهام اليومية الذكي",
                "title_en": "To-Do List Task Manager",
                "desc": "إضافة وتعديل وحذف وفلترة المهام مع أولويات وتصنيفات، وحفظ دائم بصيغة JSON وشريط بحث."
            },
            {
                "level": "مبتدئ",
                "level_color": "#10B981",
                "folder": "04_password_generator",
                "icon": "🔐",
                "title": "مولّد كلمات السر وفاحص القوة",
                "title_en": "Password Generator & Strength Meter",
                "desc": "تخصيص الطول والمحارف، حساب إنتروبيا القوة مع شريط ألوان، نسخ مباشر، وخزنة للكلمات المولدة."
            },
            {
                "level": "مبتدئ",
                "level_color": "#10B981",
                "folder": "05_rock_paper_scissors",
                "icon": "🎮",
                "title": "لعبة حجر ورقة مقص التفاعلية",
                "title_en": "Rock Paper Scissors Deluxe",
                "desc": "لعب ضد الكمبيوتر مع رسوم تفاعلية، عد تنازلي تشويقي، تتبع سلاسل الانتصارات ونسبة الفوز."
            },

            # Intermediate
            {
                "level": "متوسط",
                "level_color": "#F59E0B",
                "folder": "06_expense_tracker",
                "icon": "💰",
                "title": "متتبع المصروفات والميزانية",
                "title_en": "Personal Expense Tracker",
                "desc": "تسجيل وفلترة المصروفات، رسم بياني دائري (Donut Chart) على Canvas، وتصدير التقارير إلى CSV."
            },
            {
                "level": "متوسط",
                "level_color": "#F59E0B",
                "folder": "07_price_scraper",
                "icon": "🏷️",
                "title": "كاشط ومتتبع أسعار المنتجات",
                "title_en": "E-Commerce Price Tracker & Scraper",
                "desc": "تتبع أسعار المتاجر في خيوط خلفية (Multi-threading)، وتنبيه فوري عند انخفاض السعر المستهدف."
            },
            {
                "level": "متوسط",
                "level_color": "#F59E0B",
                "folder": "08_telegram_bot_manager",
                "icon": "🤖",
                "title": "لوحة تحكم ومحاكي بوت تيليجرام",
                "title_en": "Telegram Bot Manager & Simulator",
                "desc": "تشغيل بوت حقيقي عبر الـ API أو محاكاة تفاعلية فورية لأوامر الطقس والتذكيرات وحكم البرمجة."
            },
            {
                "level": "متوسط",
                "level_color": "#F59E0B",
                "folder": "09_file_organizer",
                "icon": "📁",
                "title": "منظم الملفات التلقائي",
                "title_en": "Automated File Organizer",
                "desc": "فرز وتصنيف ملفات أي مجلد حسب نوعها، وضع معاينة (Dry Run) وميزة التراجع الذكي (Undo)."
            },
            {
                "level": "متوسط",
                "level_color": "#F59E0B",
                "folder": "10_url_shortener",
                "icon": "🔗",
                "title": "مختصر الروابط مع SQLite وسيرفر مدمج",
                "title_en": "URL Shortener & SQLite Server",
                "desc": "إنشاء روابط وأسماء مخصصة، خادم تحويل محلي على المنفذ 8000، وتتبع عدد النقرات لحظياً."
            },

            # Advanced
            {
                "level": "متقدم",
                "level_color": "#EF4444",
                "folder": "11_movie_recommender",
                "icon": "🎬",
                "title": "نظام توصية الأفلام السينمائي",
                "title_en": "Movie Recommendation System",
                "desc": "توصيات ذكية بالـ TF-IDF و Cosine Similarity، فلترة التصنيفات، وقائمة مفضلة ومشاهدة لاحقة."
            },
            {
                "level": "متقدم",
                "level_color": "#EF4444",
                "folder": "12_sentiment_analyzer",
                "icon": "🧠",
                "title": "محلل مشاعر النصوص (عربي / English)",
                "title_en": "Sentiment Analysis System",
                "desc": "تحليل مشاعر التعليقات الإيجابية والسلبية، عداد مقياس سرعة المشاعر، وكشف الكلمات الدلالية."
            },
            {
                "level": "متقدم",
                "level_color": "#EF4444",
                "folder": "13_chat_application",
                "icon": "💬",
                "title": "تطبيق الدردشة الفورية المتعدد (Sockets)",
                "title_en": "Real-Time Socket Chat Application",
                "desc": "خادم وعميل متكامل، غرف متعددة (#العامة، #التقنية)، قائمة المتواجدين النشطين عبر الشبكة."
            },
            {
                "level": "متقدم",
                "level_color": "#EF4444",
                "folder": "14_face_attendance",
                "icon": "🛡️",
                "title": "منظومة تسجيل الحضور بالبصمة الوجهية",
                "title_en": "Face Recognition Attendance System",
                "desc": "عدسة مسح بيومترية تفاعلية، تسجيل حضور وانصراف الموظفين، وحفظ وتصدير سجل CSV."
            },
            {
                "level": "متقدم",
                "level_color": "#EF4444",
                "folder": "15_data_dashboard",
                "icon": "📊",
                "title": "لوحة مؤشرات وتحليل البيانات التنفيذية",
                "title_en": "Executive Data Analytics Dashboard",
                "desc": "مؤشرات KPI، رسم بياني شريطي ودائري تفاعلي على Canvas، فلاتر مناطق واستيراد وتصدير CSV."
            }
        ]

        self.setup_ui()

    def setup_ui(self):
        # Header Banner
        header = tk.Frame(self, bg="#111827", pady=16, padx=24)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text=f"🚀 {ar('منصة مشاريع بايثون الاحترافية (15 مشروع متكامل بـ Tkinter GUI)')}",
            font=get_font(16, "bold"),
            bg="#111827",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        sub = tk.Label(
            header,
            text=ar("كل مشروع مستقل في مجلد خاص به مع معمارية منظمة وتصميم حديث"),
            font=get_font(10),
            bg="#111827",
            fg="#94A3B8"
        )
        sub.pack(side=tk.RIGHT, padx=(0, 14))

        # Filter Tabs Row
        tabs_frame = tk.Frame(self, bg="#0B0F19", padx=24, pady=10)
        tabs_frame.pack(fill=tk.X)

        self.current_filter = "الكل"

        self.btn_tab_all = self.create_tab_btn(tabs_frame, ar("الكل (15 مشروع)"), "الكل")
        self.btn_tab_beg = self.create_tab_btn(tabs_frame, f"🟢 {ar('مبتدئ (5 مشاريع)')}", "مبتدئ")
        self.btn_tab_int = self.create_tab_btn(tabs_frame, f"🟡 {ar('متوسط (5 مشاريع)')}", "متوسط")
        self.btn_tab_adv = self.create_tab_btn(tabs_frame, f"🔴 {ar('متقدم (5 مشاريع)')}", "متقدم")

        # Scrollable Cards Area
        container = tk.Frame(self, bg="#0B0F19", padx=20, pady=6)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, bg="#0B0F19", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg="#0B0F19")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw", width=950)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scroll support
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))

        self.render_project_cards()

    def create_tab_btn(self, parent, text, filter_val):
        btn = tk.Button(
            parent,
            text=text,
            font=get_font(10, "bold"),
            bg="#1E293B" if filter_val != "الكل" else "#0284C7",
            fg="#94A3B8" if filter_val != "الكل" else "#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4,
            command=lambda: self.set_filter(filter_val)
        )
        btn.pack(side=tk.RIGHT, padx=4)
        return btn

    def set_filter(self, filter_val):
        self.current_filter = filter_val
        # Update colors
        tabs = [
            (self.btn_tab_all, "الكل"),
            (self.btn_tab_beg, "مبتدئ"),
            (self.btn_tab_int, "متوسط"),
            (self.btn_tab_adv, "متقدم")
        ]
        for btn, val in tabs:
            if val == filter_val:
                btn.config(bg="#0284C7", fg="#FFFFFF")
            else:
                btn.config(bg="#1E293B", fg="#94A3B8")

        self.render_project_cards()

    def render_project_cards(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for idx, p in enumerate(self.projects_data):
            if self.current_filter != "الكل" and p["level"] != self.current_filter:
                continue

            # Card frame
            card = tk.Frame(self.scrollable_frame, bg="#111827", bd=1, relief=tk.SOLID, padx=16, pady=12)
            card.pack(fill=tk.X, pady=6, padx=4)

            # Left side: Launch Button
            btn_launch = tk.Button(
                card,
                text=f"⚡ {ar('تشغيل المشروع')}\nLaunch App",
                font=get_font(9, "bold"),
                bg="#0284C7",
                fg="#FFFFFF",
                activebackground="#0369A1",
                activeforeground="#FFFFFF",
                relief=tk.FLAT,
                cursor="hand2",
                padx=16,
                pady=6,
                command=lambda folder=p["folder"]: self.launch_project(folder)
            )
            btn_launch.pack(side=tk.LEFT, padx=(0, 10))

            # Right side: Title & Description
            info_frame = tk.Frame(card, bg="#111827")
            info_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

            top_row = tk.Frame(info_frame, bg="#111827")
            top_row.pack(fill=tk.X)

            # Level badge
            level_badge = tk.Label(
                top_row,
                text=ar(p["level"]),
                font=get_font(8, "bold"),
                bg="#1F2937",
                fg=p["level_color"],
                padx=8,
                pady=2
            )
            level_badge.pack(side=tk.LEFT)

            # Project Title
            title_text = f"{p['icon']} {ar(p['title'])}  •  {p['title_en']}"
            title_lbl = tk.Label(
                top_row,
                text=title_text,
                font=get_font(12, "bold"),
                bg="#111827",
                fg="#F8FAFC"
            )
            title_lbl.pack(side=tk.RIGHT)

            # Description
            desc_lbl = tk.Label(
                info_frame,
                text=ar(p["desc"]),
                font=get_font(9),
                bg="#111827",
                fg="#94A3B8",
                anchor="e",
                justify="right"
            )
            desc_lbl.pack(fill=tk.X, pady=(4, 0))

    def launch_project(self, folder_name):
        script_path = os.path.join(self.base_dir, folder_name, "main.py")
        if not os.path.exists(script_path):
            messagebox.showerror(ar("خطأ"), f"{ar('ملف المشروع غير موجود في المسار:')}\n{script_path}")
            return

        try:
            # Run independently in a new process
            subprocess.Popen([sys.executable, script_path], cwd=os.path.join(self.base_dir, folder_name))
        except Exception as e:
            messagebox.showerror("خطأ في التشغيل", f"فشل تشغيل المشروع:\n{e}")


if __name__ == "__main__":
    app = MasterLauncherApp()
    app.mainloop()
