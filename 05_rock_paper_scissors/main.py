#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 5: لعبة حجر ورقة مقص التفاعلية (Rock Paper Scissors Deluxe GUI)
يدعم:
- اللعب ضد الكمبيوتر مع خوارزمية ذكية وعشوائية
- بطاقات مرئية للأشكال (🪨 حجر، 📄 ورقة، ✂️ مقص)
- حركة تشويق للنتيجة ومؤثرات ألوان
- عداد شامل للنتائج (فوز اللاعب، فوز الكمبيوتر، التعادل، نسبة الفوز %)
- تتبع سلسلة الانتصارات الحالية (Winning Streak)
- سجل لجميع الجولات السابقة مع تفاصيل الاختيارات
"""

import random
import tkinter as tk
from tkinter import messagebox


class RockPaperScissorsGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لعبة حجر ورقة مقص | Rock Paper Scissors")
        self.geometry("760x650")
        self.minsize(700, 600)
        self.configure(bg="#0B0F19")

        # Game state
        self.choices = {
            "rock": {"name_ar": "حجر", "icon": "🪨", "beats": "scissors", "color": "#EF4444"},
            "paper": {"name_ar": "ورقة", "icon": "📄", "beats": "rock", "color": "#3B82F6"},
            "scissors": {"name_ar": "مقص", "icon": "✂️", "beats": "paper", "color": "#10B981"}
        }

        self.score_player = 0
        self.score_computer = 0
        self.score_ties = 0
        self.current_streak = 0
        self.best_streak = 0
        self.rounds_played = 0
        self.is_animating = False

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#111827", pady=12)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎮 تحدي حجر • ورقة • مقص",
            font=("Segoe UI", 18, "bold"),
            bg="#111827",
            fg="#F59E0B"
        )
        title.pack()

        sub = tk.Label(
            header,
            text="اختر سلاحك وتحدى الذكاء الاصطناعي للكمبيوتر!",
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#9CA3AF"
        )
        sub.pack()

        # Scoreboard
        scoreboard = tk.Frame(self, bg="#1F2937", pady=10, padx=20)
        scoreboard.pack(fill=tk.X)

        # Player Score Card
        p_frame = tk.Frame(scoreboard, bg="#1F2937")
        p_frame.pack(side=tk.RIGHT, expand=True)
        tk.Label(p_frame, text="👤 اللاعب (أنت)", font=("Segoe UI", 10, "bold"), bg="#1F2937", fg="#60A5FA").pack()
        self.lbl_p_score = tk.Label(p_frame, text="0", font=("Segoe UI", 24, "bold"), bg="#1F2937", fg="#FFFFFF")
        self.lbl_p_score.pack()

        # Center vs & stats
        mid_frame = tk.Frame(scoreboard, bg="#1F2937")
        mid_frame.pack(side=tk.RIGHT, expand=True)
        self.lbl_streak = tk.Label(mid_frame, text="🔥 السلسلة: 0 | تعادل: 0", font=("Segoe UI", 10, "bold"), bg="#1F2937", fg="#FBBF24")
        self.lbl_streak.pack()
        self.lbl_winrate = tk.Label(mid_frame, text="نسبة الفوز: 0%", font=("Segoe UI", 9), bg="#1F2937", fg="#9CA3AF")
        self.lbl_winrate.pack()

        # Computer Score Card
        c_frame = tk.Frame(scoreboard, bg="#1F2937")
        c_frame.pack(side=tk.RIGHT, expand=True)
        tk.Label(c_frame, text="🤖 الكمبيوتر", font=("Segoe UI", 10, "bold"), bg="#1F2937", fg="#F87171").pack()
        self.lbl_c_score = tk.Label(c_frame, text="0", font=("Segoe UI", 24, "bold"), bg="#1F2937", fg="#FFFFFF")
        self.lbl_c_score.pack()

        # Arena Display (Middle)
        arena = tk.Frame(self, bg="#0B0F19", pady=20)
        arena.pack(fill=tk.X)

        arena_inner = tk.Frame(arena, bg="#111827", bd=1, relief=tk.SOLID, padx=30, pady=16)
        arena_inner.pack()

        # Player Choice Box
        self.box_player = tk.Label(
            arena_inner,
            text="❔\nأنت",
            font=("Segoe UI", 28, "bold"),
            bg="#1F2937",
            fg="#60A5FA",
            width=6,
            height=3,
            relief=tk.FLAT
        )
        self.box_player.pack(side=tk.RIGHT, padx=20)

        # VS Label
        self.lbl_arena_status = tk.Label(
            arena_inner,
            text="VS\nابدأ الجولة!",
            font=("Segoe UI", 14, "bold"),
            bg="#111827",
            fg="#F3F4F6",
            width=14
        )
        self.lbl_arena_status.pack(side=tk.RIGHT, padx=10)

        # Computer Choice Box
        self.box_computer = tk.Label(
            arena_inner,
            text="❔\nالكمبيوتر",
            font=("Segoe UI", 28, "bold"),
            bg="#1F2937",
            fg="#F87171",
            width=6,
            height=3,
            relief=tk.FLAT
        )
        self.box_computer.pack(side=tk.RIGHT, padx=20)

        # Action Buttons (User Choices)
        btn_area = tk.Frame(self, bg="#0B0F19", pady=10)
        btn_area.pack(fill=tk.X)

        tk.Label(
            btn_area,
            text="اضغط على اختيارك للعب الجولة:",
            font=("Segoe UI", 11, "bold"),
            bg="#0B0F19",
            fg="#9CA3AF"
        ).pack(pady=(0, 10))

        choices_frame = tk.Frame(btn_area, bg="#0B0F19")
        choices_frame.pack()

        # 3 Choice Buttons
        for key in ["rock", "paper", "scissors"]:
            item = self.choices[key]
            btn = tk.Button(
                choices_frame,
                text=f"{item['icon']}\n{item['name_ar']}",
                font=("Segoe UI", 14, "bold"),
                bg="#1F2937",
                fg="#FFFFFF",
                activebackground=item["color"],
                activeforeground="#FFFFFF",
                width=10,
                height=3,
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda k=key: self.play_round(k)
            )
            btn.pack(side=tk.RIGHT, padx=10)

        # History and Reset Section
        bottom_area = tk.Frame(self, bg="#0B0F19", padx=20, pady=10)
        bottom_area.pack(fill=tk.BOTH, expand=True)

        bot_header = tk.Frame(bottom_area, bg="#0B0F19")
        bot_header.pack(fill=tk.X, pady=(0, 4))

        tk.Label(bot_header, text="📜 سجل مواجهات الجولات:", font=("Segoe UI", 10, "bold"), bg="#0B0F19", fg="#9CA3AF").pack(side=tk.RIGHT)
        tk.Button(bot_header, text="🔄 تصفير النتيجة", font=("Segoe UI", 9), bg="#374151", fg="#F87171", relief=tk.FLAT, cursor="hand2", command=self.reset_game).pack(side=tk.LEFT)

        self.history_listbox = tk.Listbox(
            bottom_area,
            bg="#111827",
            fg="#E5E7EB",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground="#374151"
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

    def play_round(self, player_key):
        if self.is_animating:
            return

        self.is_animating = True
        p_item = self.choices[player_key]
        self.box_player.config(text=f"{p_item['icon']}\nأنت", bg="#1E3A8A")

        # Countdown animation
        computer_key = random.choice(["rock", "paper", "scissors"])
        c_item = self.choices[computer_key]

        countdown_steps = ["✊\n3", "✋\n2", "✌\n1"]

        def step(idx):
            if idx < len(countdown_steps):
                self.box_computer.config(text=countdown_steps[idx], bg="#374151")
                self.after(250, lambda: step(idx + 1))
            else:
                self.finalize_round(player_key, computer_key)

        step(0)

    def finalize_round(self, player_key, computer_key):
        p_item = self.choices[player_key]
        c_item = self.choices[computer_key]

        self.box_computer.config(text=f"{c_item['icon']}\nالكمبيوتر", bg="#7F1D1D")
        self.rounds_played += 1

        # Check outcome
        if player_key == computer_key:
            outcome = "tie"
            self.score_ties += 1
            self.current_streak = 0
            msg = "🤝 تعادل!\nنفس الاختيار"
            status_fg = "#FBBF24"
            log_icon = "🤝"
        elif p_item["beats"] == computer_key:
            outcome = "player"
            self.score_player += 1
            self.current_streak += 1
            if self.current_streak > self.best_streak:
                self.best_streak = self.current_streak
            msg = "🎉 فوز رائع!\nأحسنت!"
            status_fg = "#34D399"
            log_icon = "🏆"
        else:
            outcome = "computer"
            self.score_computer += 1
            self.current_streak = 0
            msg = "💥 خسارة!\nحظ أوفر"
            status_fg = "#F87171"
            log_icon = "💀"

        self.lbl_arena_status.config(text=msg, fg=status_fg)
        self.lbl_p_score.config(text=str(self.score_player))
        self.lbl_c_score.config(text=str(self.score_computer))

        win_rate = int((self.score_player / self.rounds_played) * 100) if self.rounds_played > 0 else 0
        self.lbl_streak.config(text=f"🔥 السلسلة: {self.current_streak} (أفضل: {self.best_streak}) | تعادل: {self.score_ties}")
        self.lbl_winrate.config(text=f"نسبة الفوز: {win_rate}% (إجمالي: {self.rounds_played} جولة)")

        self.history_listbox.insert(
            0,
            f"{log_icon} جولة {self.rounds_played}: أنت ({p_item['icon']} {p_item['name_ar']}) ضد الكمبيوتر ({c_item['icon']} {c_item['name_ar']}) ➔ {msg.replace(chr(10), ' ')}"
        )

        self.is_animating = False

    def reset_game(self):
        if self.rounds_played == 0:
            return
        if messagebox.askyesno("تأكيد التصفير", "هل تريد تصفير جميع النتائج والبدء من جديد؟"):
            self.score_player = 0
            self.score_computer = 0
            self.score_ties = 0
            self.current_streak = 0
            self.best_streak = 0
            self.rounds_played = 0
            self.lbl_p_score.config(text="0")
            self.lbl_c_score.config(text="0")
            self.lbl_streak.config(text="🔥 السلسلة: 0 | تعادل: 0")
            self.lbl_winrate.config(text="نسبة الفوز: 0%")
            self.box_player.config(text="❔\nأنت", bg="#1F2937")
            self.box_computer.config(text="❔\nالكمبيوتر", bg="#1F2937")
            self.lbl_arena_status.config(text="VS\nابدأ الجولة!", fg="#F3F4F6")
            self.history_listbox.delete(0, tk.END)


if __name__ == "__main__":
    app = RockPaperScissorsGame()
    app.mainloop()
