#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 2: لعبة تخمين الرقم (Number Guessing Game GUI)
يدعم:
- توليد رقم عشوائي مع 3 مستويات صعوبة (سهل 1-50، متوسط 1-100، صعب 1-500)
- تلميحات ديناميكية (أعلى ⬆️ / أقل ⬇️) ومقياس حراري (قريب جداً 🔥 / بعيد ❄️)
- حساب عدد المحاولات، النقاط، وأفضل نتيجة (High Score) محفوظة في ملف
- سجل المحاولات السابقة بالترتيب
- واجهة Tkinter تفاعلية بألوان حديثة ومؤثرات بصرية
"""

import json
import os
import random
import tkinter as tk
from tkinter import messagebox


class NumberGuessingGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("لعبة تخمين الرقم | Number Guessing Game")
        self.geometry("700x620")
        self.minsize(620, 560)
        self.configure(bg="#0B132B")  # Deep Navy

        # State
        self.difficulty_ranges = {
            "سهل (1 - 50)": (1, 50, 10),
            "متوسط (1 - 100)": (1, 100, 7),
            "صعب (1 - 500)": (1, 500, 10)
        }
        self.current_diff = "متوسط (1 - 100)"
        self.secret_number = 0
        self.max_attempts = 7
        self.attempts_left = 7
        self.attempts_taken = 0
        self.guesses_history = []
        self.high_score = self.load_high_score()

        self.setup_ui()
        self.start_new_game()

    def load_high_score(self):
        save_file = os.path.join(os.path.dirname(__file__), "highscore.json")
        if os.path.exists(save_file):
            try:
                with open(save_file, "r", encoding="utf-8") as f:
                    return json.load(f).get("best_attempts", None)
            except Exception:
                return None
        return None

    def save_high_score(self, attempts):
        save_file = os.path.join(os.path.dirname(__file__), "highscore.json")
        try:
            with open(save_file, "w", encoding="utf-8") as f:
                json.dump({"best_attempts": attempts}, f)
        except Exception:
            pass

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1C2541", pady=14)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎯 لعبة تخمين الرقم الذكية",
            font=("Segoe UI", 20, "bold"),
            bg="#1C2541",
            fg="#6FFFE9"
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="خمن الرقم الذي اختاره الكمبيوتر بأقل عدد من المحاولات!",
            font=("Segoe UI", 11),
            bg="#1C2541",
            fg="#A5B4FC"
        )
        subtitle.pack(pady=(2, 0))

        # Main Container
        container = tk.Frame(self, bg="#0B132B", padx=20, pady=16)
        container.pack(fill=tk.BOTH, expand=True)

        # Control Panel: Difficulty & Stats Bar
        control_frame = tk.Frame(container, bg="#1C2541", bd=1, relief=tk.SOLID)
        control_frame.pack(fill=tk.X, pady=(0, 14), ipady=8, padx=4)

        # Difficulty Selector
        diff_label = tk.Label(
            control_frame,
            text="المستوى:",
            font=("Segoe UI", 11, "bold"),
            bg="#1C2541",
            fg="#FFFFFF"
        )
        diff_label.pack(side=tk.RIGHT, padx=(10, 14))

        self.diff_var = tk.StringVar(value=self.current_diff)
        for diff_name in self.difficulty_ranges.keys():
            rb = tk.Radiobutton(
                control_frame,
                text=diff_name,
                variable=self.diff_var,
                value=diff_name,
                font=("Segoe UI", 10),
                bg="#1C2541",
                fg="#E2E8F0",
                selectcolor="#3A506B",
                activebackground="#1C2541",
                activeforeground="#6FFFE9",
                command=self.on_diff_change
            )
            rb.pack(side=tk.RIGHT, padx=6)

        # High score label on left
        self.high_score_label = tk.Label(
            control_frame,
            text=f"🏆 أفضل نتيجة: {self.high_score if self.high_score else '--'}",
            font=("Segoe UI", 10, "bold"),
            bg="#1C2541",
            fg="#FCD34D"
        )
        self.high_score_label.pack(side=tk.LEFT, padx=14)

        # Center Status Card
        self.card = tk.Frame(container, bg="#1C2541", pady=16, padx=16, bd=1, relief=tk.FLAT)
        self.card.pack(fill=tk.X, pady=(0, 14))

        self.hint_icon = tk.Label(
            self.card,
            text="🤔",
            font=("Segoe UI", 36),
            bg="#1C2541"
        )
        self.hint_icon.pack()

        self.hint_text = tk.Label(
            self.card,
            text="أنا اخترت رقماً، خمن كم هو!",
            font=("Segoe UI", 15, "bold"),
            bg="#1C2541",
            fg="#F8FAFC"
        )
        self.hint_text.pack(pady=4)

        self.range_text = tk.Label(
            self.card,
            text="النطاق: 1 إلى 100",
            font=("Segoe UI", 11),
            bg="#1C2541",
            fg="#94A3B8"
        )
        self.range_text.pack()

        # Attempts Progress / Badge
        self.attempts_badge = tk.Label(
            self.card,
            text="المحاولات المتبقية: 7 / 7",
            font=("Segoe UI", 11, "bold"),
            bg="#3A506B",
            fg="#FFFFFF",
            padx=12,
            pady=4
        )
        self.attempts_badge.pack(pady=(10, 0))

        # Input Frame
        input_frame = tk.Frame(container, bg="#0B132B")
        input_frame.pack(fill=tk.X, pady=(0, 14))

        self.guess_entry = tk.Entry(
            input_frame,
            font=("Segoe UI", 18, "bold"),
            justify="center",
            width=10,
            bg="#1C2541",
            fg="#6FFFE9",
            insertbackground="#6FFFE9",
            relief=tk.FLAT,
            bd=2
        )
        self.guess_entry.pack(side=tk.LEFT, expand=True, ipady=6, padx=(0, 8))
        self.guess_entry.bind("<Return>", lambda e: self.make_guess())
        self.guess_entry.focus()

        self.guess_btn = tk.Button(
            input_frame,
            text="تأكيد التخمين (Enter)",
            font=("Segoe UI", 12, "bold"),
            bg="#48CAE4",
            fg="#03045E",
            activebackground="#0096C7",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            command=self.make_guess
        )
        self.guess_btn.pack(side=tk.LEFT, ipady=6, padx=(0, 8))

        self.restart_btn = tk.Button(
            input_frame,
            text="🔄 لعبة جديدة",
            font=("Segoe UI", 12),
            bg="#3A506B",
            fg="#FFFFFF",
            activebackground="#4A6572",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            command=self.start_new_game
        )
        self.restart_btn.pack(side=tk.LEFT, ipady=6)

        # History / Log section
        history_frame = tk.Frame(container, bg="#1C2541", bd=1, relief=tk.SOLID)
        history_frame.pack(fill=tk.BOTH, expand=True)

        history_header = tk.Label(
            history_frame,
            text="📋 سجل تخميناتك في هذه الجولة:",
            font=("Segoe UI", 11, "bold"),
            bg="#1C2541",
            fg="#94A3B8",
            anchor="w",
            padx=12,
            pady=6
        )
        history_header.pack(fill=tk.X)

        self.history_listbox = tk.Listbox(
            history_frame,
            bg="#0B132B",
            fg="#E2E8F0",
            font=("Segoe UI", 11),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground="#3A506B"
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

    def on_diff_change(self):
        self.current_diff = self.diff_var.get()
        self.start_new_game()

    def start_new_game(self):
        low, high, max_att = self.difficulty_ranges[self.current_diff]
        self.secret_number = random.randint(low, high)
        self.max_attempts = max_att
        self.attempts_left = max_att
        self.attempts_taken = 0
        self.guesses_history.clear()

        self.range_text.config(text=f"النطاق المطلوب: من {low} إلى {high}")
        self.hint_icon.config(text="🤔")
        self.hint_text.config(text="أنا اخترت رقماً، خمن كم هو!", fg="#F8FAFC")
        self.attempts_badge.config(
            text=f"المحاولات المتبقية: {self.attempts_left} / {self.max_attempts}",
            bg="#3A506B"
        )
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state=tk.NORMAL)
        self.guess_btn.config(state=tk.NORMAL)
        self.history_listbox.delete(0, tk.END)
        self.guess_entry.focus()

    def make_guess(self):
        val = self.guess_entry.get().strip()
        if not val.isdigit():
            messagebox.showwarning("تنبيه", "يرجى إدخال رقم صحيح فقط!")
            return

        guess = int(val)
        low, high, _ = self.difficulty_ranges[self.current_diff]

        if guess < low or guess > high:
            messagebox.showwarning("خارج النطاق", f"يرجى إدخال رقم بين {low} و {high}!")
            return

        self.attempts_taken += 1
        self.attempts_left -= 1
        self.guess_entry.delete(0, tk.END)

        diff = abs(guess - self.secret_number)

        # Check Win
        if guess == self.secret_number:
            self.hint_icon.config(text="🎉")
            self.hint_text.config(
                text=f"مبروك! إجابة صحيحة ({self.secret_number}) في {self.attempts_taken} محاولة!",
                fg="#4ADE80"
            )
            self.attempts_badge.config(text="انتصار! 🏆", bg="#15803D")
            self.guess_entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)

            # Check High Score
            if self.high_score is None or self.attempts_taken < self.high_score:
                self.high_score = self.attempts_taken
                self.save_high_score(self.high_score)
                self.high_score_label.config(text=f"🏆 أفضل نتيجة: {self.high_score} محاولة!")

            self.history_listbox.insert(0, f"✅ محاولة {self.attempts_taken}: {guess} (إجابة صحيحة!)")
            return

        # Check Loss
        if self.attempts_left <= 0:
            self.hint_icon.config(text="💀")
            self.hint_text.config(
                text=f"للأسف نفدت المحاولات! الرقم كان: {self.secret_number}",
                fg="#F87171"
            )
            self.attempts_badge.config(text="انتهت اللعبة! ❌", bg="#B91C1C")
            self.guess_entry.config(state=tk.DISABLED)
            self.guess_btn.config(state=tk.DISABLED)
            self.history_listbox.insert(0, f"❌ محاولة {self.attempts_taken}: {guess} (انتهت المحاولات)")
            return

        # Hint logic
        direction = "أكبر ⬆️ (جرب رقماً أكبر)" if guess < self.secret_number else "أصغر ⬇️ (جرب رقماً أصغر)"
        closeness = ""
        if diff <= 3:
            closeness = "قريب جداً جداً! 🔥🔥"
        elif diff <= 10:
            closeness = "قريب! 🔥"
        elif diff > (high - low) // 2:
            closeness = "بعيد جداً! ❄️❄️"
        else:
            closeness = "معتدل البعد 💨"

        self.hint_icon.config(text="🔥" if diff <= 5 else "🧭")
        self.hint_text.config(
            text=f"الرقم الصحيح {direction} - {closeness}",
            fg="#FCD34D" if diff <= 10 else "#60A5FA"
        )
        self.attempts_badge.config(
            text=f"المحاولات المتبقية: {self.attempts_left} / {self.max_attempts}",
            bg="#B45309" if self.attempts_left <= 2 else "#3A506B"
        )

        self.history_listbox.insert(
            0,
            f"🔹 محاولة {self.attempts_taken}: {guess} ➔ {direction} ({closeness})"
        )


if __name__ == "__main__":
    app = NumberGuessingGame()
    app.mainloop()
