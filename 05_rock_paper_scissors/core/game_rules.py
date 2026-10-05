# -*- coding: utf-8 -*-
"""
محرك قواعد لعبة حجر ورقة مقص
"""

import random


class RockPaperScissorsEngine:
    CHOICES = {
        "rock": {"name_ar": "حجر", "icon": "🪨", "beats": "scissors", "color": "#EF4444"},
        "paper": {"name_ar": "ورقة", "icon": "📄", "beats": "rock", "color": "#3B82F6"},
        "scissors": {"name_ar": "مقص", "icon": "✂️", "beats": "paper", "color": "#10B981"}
    }

    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds = 0
        self.streak = 0
        self.best_streak = 0
        self.history = []

    def get_computer_choice(self):
        return random.choice(["rock", "paper", "scissors"])

    def evaluate_round(self, player_key, computer_key):
        self.rounds += 1
        p_item = self.CHOICES[player_key]
        c_item = self.CHOICES[computer_key]

        if player_key == computer_key:
            outcome = "tie"
            self.ties += 1
            self.streak = 0
            msg = "🤝 تعادل!\nنفس الاختيار"
            status_fg = "#FBBF24"
            log_icon = "🤝"
        elif p_item["beats"] == computer_key:
            outcome = "player"
            self.player_score += 1
            self.streak += 1
            if self.streak > self.best_streak:
                self.best_streak = self.streak
            msg = "🎉 فوز رائع!\nأحسنت!"
            status_fg = "#34D399"
            log_icon = "🏆"
        else:
            outcome = "computer"
            self.computer_score += 1
            self.streak = 0
            msg = "💥 خسارة!\nحظ أوفر"
            status_fg = "#F87171"
            log_icon = "💀"

        log_entry = f"{log_icon} جولة {self.rounds}: أنت ({p_item['icon']} {p_item['name_ar']}) ضد الكمبيوتر ({c_item['icon']} {c_item['name_ar']}) ➔ {msg.replace(chr(10), ' ')}"
        self.history.insert(0, log_entry)

        win_rate = int((self.player_score / self.rounds) * 100) if self.rounds > 0 else 0

        return {
            "outcome": outcome,
            "msg": msg,
            "status_fg": status_fg,
            "player_score": self.player_score,
            "computer_score": self.computer_score,
            "ties": self.ties,
            "streak": self.streak,
            "best_streak": self.best_streak,
            "rounds": self.rounds,
            "win_rate": win_rate,
            "log_entry": log_entry
        }

    def reset(self):
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.rounds = 0
        self.streak = 0
        self.best_streak = 0
        self.history.clear()
