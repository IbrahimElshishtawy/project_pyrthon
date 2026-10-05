# -*- coding: utf-8 -*-
"""
محرك تحليل المشاعر للنصوص العربية والإنجليزية
"""

import re


class SentimentEngine:
    def __init__(self):
        self.ar_positive = {
            "ممتاز", "رائع", "جميل", "عظيم", "ممتازة", "رائعة", "جميلة", "مبدع", "مبهر",
            "أفضل", "حب", "سعيد", "فخور", "ناجح", "ممتع", "أعجبني", "شكرا", "تحفة",
            "سريع", "احترافي", "مميز", "مريح", "قوي", "فخم", "نظيف", "استثنائي", "بطل"
        }
        self.ar_negative = {
            "سيء", "رديء", "فظيع", "زفت", "فاشل", "بطيء", "غالي", "تالف", "معقد",
            "سيئة", "رديئة", "كارثة", "نصب", "محبط", "مقرف", "كره", "حزين", "مخيب",
            "مشكلة", "عطل", "مزعج", "غبي", "ندمان", "ضياع", "خسارة", "صعب", "معفن"
        }
        self.ar_negations = {"مش", "ليس", "ليست", "ما", "لا", "لم", "لن", "غير"}
        self.ar_intensifiers = {"جدا", "جداً", "للغاية", "كتير", "قوي", "خالص", "أوي"}

        self.en_positive = {
            "good", "great", "excellent", "awesome", "amazing", "love", "loved", "best",
            "fantastic", "superb", "happy", "fast", "reliable", "beautiful", "perfect",
            "helpful", "easy", "clean", "wonderful", "impressive", "brilliant", "smooth"
        }
        self.en_negative = {
            "bad", "terrible", "horrible", "awful", "worst", "hate", "hated", "slow",
            "broken", "expensive", "ugly", "scam", "poor", "disappointing", "waste",
            "annoying", "useless", "crash", "error", "problem", "difficult", "boring"
        }
        self.en_negations = {"not", "never", "no", "without", "hardly", "barely", "isn't", "aren't", "wasn't"}
        self.en_intensifiers = {"very", "extremely", "really", "so", "totally", "super"}

    def analyze(self, text):
        clean_words = re.findall(r'[\w\']+', text.lower())
        if not clean_words:
            return {"polarity": 0.0, "label": "محايد (Neutral)", "pos_words": [], "neg_words": []}

        score = 0.0
        pos_found = []
        neg_found = []
        negate_window = 0

        for idx, w in enumerate(clean_words):
            if w in self.ar_negations or w in self.en_negations:
                negate_window = 2
                continue

            multiplier = 1.0
            if idx > 0 and (clean_words[idx - 1] in self.ar_intensifiers or clean_words[idx - 1] in self.en_intensifiers):
                multiplier = 1.5

            if negate_window > 0:
                multiplier *= -1.0
                negate_window -= 1

            if w in self.ar_positive or w in self.en_positive:
                word_score = 1.0 * multiplier
                score += word_score
                if word_score > 0:
                    pos_found.append(w)
                else:
                    neg_found.append(f"{w} (منفي)")
            elif w in self.ar_negative or w in self.en_negative:
                word_score = -1.0 * multiplier
                score += word_score
                if word_score < 0:
                    neg_found.append(w)
                else:
                    pos_found.append(f"{w} (نفي سلبي)")

        normalized = max(-1.0, min(1.0, score / max(1, len(pos_found) + len(neg_found) or 1)))

        if normalized > 0.15:
            label = "إيجابي (Positive) 🟢"
        elif normalized < -0.15:
            label = "سلبي (Negative) 🔴"
        else:
            label = "محايد (Neutral) ⚪"

        return {
            "polarity": round(normalized, 2),
            "label": label,
            "pos_words": list(set(pos_found)),
            "neg_words": list(set(neg_found))
        }
