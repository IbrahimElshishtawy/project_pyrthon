# -*- coding: utf-8 -*-
"""
محرك قواعد ولعبة تخمين الرقم (Game Logic & State)
"""

import json
import os
import random


class NumberGuessingGameLogic:
    DIFFICULTIES = {
        "سهل (1 - 50)": (1, 50, 10),
        "متوسط (1 - 100)": (1, 100, 7),
        "صعب (1 - 500)": (1, 500, 10)
    }

    def __init__(self, save_path=None):
        self.save_path = save_path or os.path.join(os.path.dirname(__file__), "..", "highscore.json")
        self.current_diff = "متوسط (1 - 100)"
        self.secret_number = 0
        self.max_attempts = 7
        self.attempts_left = 7
        self.attempts_taken = 0
        self.history = []
        self.is_over = False
        self.high_score = self.load_high_score()

    def load_high_score(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r", encoding="utf-8") as f:
                    return json.load(f).get("best_attempts", None)
            except Exception:
                return None
        return None

    def save_high_score(self, attempts):
        try:
            with open(self.save_path, "w", encoding="utf-8") as f:
                json.dump({"best_attempts": attempts}, f)
        except Exception:
            pass

    def start_game(self, diff_name=None):
        if diff_name:
            self.current_diff = diff_name
        low, high, max_att = self.DIFFICULTIES[self.current_diff]
        self.secret_number = random.randint(low, high)
        self.max_attempts = max_att
        self.attempts_left = max_att
        self.attempts_taken = 0
        self.history.clear()
        self.is_over = False

    def guess(self, number):
        if self.is_over:
            return {"status": "over", "msg": "اللعبة منتهية"}

        low, high, _ = self.DIFFICULTIES[self.current_diff]
        if number < low or number > high:
            return {"status": "out_of_range", "low": low, "high": high}

        self.attempts_taken += 1
        self.attempts_left -= 1
        diff = abs(number - self.secret_number)

        # Check win
        if number == self.secret_number:
            self.is_over = True
            is_new_high = False
            if self.high_score is None or self.attempts_taken < self.high_score:
                self.high_score = self.attempts_taken
                self.save_high_score(self.high_score)
                is_new_high = True

            result = {
                "status": "win",
                "secret": self.secret_number,
                "attempts": self.attempts_taken,
                "new_high": is_new_high
            }
            self.history.insert(0, f"✅ محاولة {self.attempts_taken}: {number} (إجابة صحيحة!)")
            return result

        # Check loss
        if self.attempts_left <= 0:
            self.is_over = True
            result = {
                "status": "loss",
                "secret": self.secret_number,
                "attempts": self.attempts_taken
            }
            self.history.insert(0, f"❌ محاولة {self.attempts_taken}: {number} (انتهت المحاولات)")
            return result

        # Hint logic
        direction = "أكبر ⬆️" if number < self.secret_number else "أصغر ⬇️"
        closeness = ""
        if diff <= 3:
            closeness = "قريب جداً جداً! 🔥🔥"
        elif diff <= 10:
            closeness = "قريب! 🔥"
        elif diff > (high - low) // 2:
            closeness = "بعيد جداً! ❄️❄️"
        else:
            closeness = "معتدل البعد 💨"

        self.history.insert(0, f"🔹 محاولة {self.attempts_taken}: {number} ➔ {direction} ({closeness})")

        return {
            "status": "continue",
            "direction": direction,
            "closeness": closeness,
            "diff": diff,
            "attempts_left": self.attempts_left,
            "attempts_taken": self.attempts_taken
        }
