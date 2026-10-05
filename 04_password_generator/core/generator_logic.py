# -*- coding: utf-8 -*-
"""
محرك توليد وفحص كلمات السر الآمنة (Pure Logic)
"""

import math
import random
import string


class PasswordGeneratorLogic:
    def __init__(self):
        self.history = []

    def generate(self, length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, no_ambiguous=False):
        charset = ""
        if use_upper:
            charset += string.ascii_uppercase
        if use_lower:
            charset += string.ascii_lowercase
        if use_digits:
            charset += string.digits
        if use_symbols:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"

        if no_ambiguous:
            for ch in "l1IoO0":
                charset = charset.replace(ch, "")

        if not charset:
            return {"password": "", "entropy": 0, "rating": "لا توجد أحرف مختارة", "color": "#EF4444", "pct": 0.0}

        # Cryptographically strong RNG
        password = "".join(random.SystemRandom().choice(charset) for _ in range(length))
        entropy = length * math.log2(len(charset))

        if entropy < 35:
            rating = f"ضعيفة جداً ({int(entropy)} bits) ⚠️"
            color = "#EF4444"
            pct = 0.25
        elif entropy < 55:
            rating = f"متوسطة ({int(entropy)} bits)"
            color = "#F59E0B"
            pct = 0.50
        elif entropy < 75:
            rating = f"قوية ({int(entropy)} bits) 👍"
            color = "#38BDF8"
            pct = 0.75
        else:
            rating = f"قوية للغاية / درجة عسكرية ({int(entropy)} bits) 🛡️"
            color = "#10B981"
            pct = 1.0

        if password not in self.history:
            self.history.insert(0, password)
            if len(self.history) > 25:
                self.history.pop()

        return {
            "password": password,
            "entropy": int(entropy),
            "rating": rating,
            "color": color,
            "pct": pct
        }

    def clear_history(self):
        self.history.clear()
