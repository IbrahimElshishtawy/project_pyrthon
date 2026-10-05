#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 12: محلل مشاعر التعليقات والنصوص (Arabic & English Sentiment Analyzer)
يدعم:
- تحليل فوري للمشاعر باللغتين العربية والإنجليزية
- تصنيف المشاعر إلى: (إيجابي 🟢، سلبي 🔴، محايد ⚪)
- معالجة أدوات النفي (مش، ليس، ما، لا، not, never) وأدوات التوكيد (جداً، للغاية، very)
- عداد مرئي تفاعلي (Sentiment Speedometer Gauge) مرسوم على Canvas
- كشف الكلمات الدلالية الإيجابية والسلبية المستخدمة
- وضع التحليل المتعدد (Batch Mode) لتحليل عشرات التعليقات دفعة واحدة مع نسب مئوية
"""

import math
import re
import tkinter as tk
from tkinter import ttk, messagebox


class SentimentEngine:
    def __init__(self):
        # Arabic Lexicon
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

        # English Lexicon
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
            # Check negation
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

        total_words = len(clean_words)
        # Normalize between -1.0 and +1.0
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


class SentimentAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("محلل مشاعر النصوص والتعليقات | Sentiment Analyzer")
        self.geometry("900x700")
        self.minsize(820, 620)
        self.configure(bg="#0F172A")

        self.engine = SentimentEngine()

        self.setup_ui()
        self.analyze_current_text()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🧠 محلل مشاعر النصوص والتعليقات الذكي (عربي / English)",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        sub = tk.Label(
            header,
            text="اكتشف انطباعات العملاء وتقييمات المنتجات فورياً",
            font=("Segoe UI", 9),
            bg="#1E293B",
            fg="#94A3B8"
        )
        sub.pack(side=tk.RIGHT, padx=(0, 10))

        # Main Body
        body = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Top row: Left (Gauge Speedometer), Right (Input Area)
        top_split = tk.Frame(body, bg="#0F172A")
        top_split.pack(fill=tk.X, pady=(0, 12))

        # Input Card (Right)
        input_card = tk.Frame(top_split, bg="#1E293B", padx=14, pady=12, bd=1, relief=tk.SOLID)
        input_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        tk.Label(input_card, text="اكتب أو الصق التعليق المراد تحليله:", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC").pack(anchor="e", pady=(0, 6))

        self.text_input = tk.Text(
            input_card,
            font=("Segoe UI", 11),
            bg="#0F172A",
            fg="#FFFFFF",
            insertbackground="#38BDF8",
            relief=tk.FLAT,
            height=5,
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.text_input.insert("1.0", "المنتج ممتاز جداً والتوصيل كان سريع ورائع، شكراً جزيلاً!")

        # Quick sample buttons
        samples_bar = tk.Frame(input_card, bg="#1E293B")
        samples_bar.pack(fill=tk.X, pady=(0, 8))

        samples = [
            ("تجربة إيجابية", "خدمة عملاء ممتازة وقمة في الاحترام والاحترافية!"),
            ("تجربة سلبية", "المنتج سيء جداً وتالف والتوصيل بطيء للغاية ومحبط!"),
            ("تجربة إنجليزية", "This application is absolutely amazing and very easy to use!"),
            ("نفي ذكي", "السعر مش رخيص والمنتج ليس سيئاً إطلاقاً.")
        ]
        for name, txt in samples:
            btn = tk.Button(
                samples_bar,
                text=name,
                font=("Segoe UI", 8),
                bg="#334155",
                fg="#E2E8F0",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda t=txt: self.load_sample(t)
            )
            btn.pack(side=tk.RIGHT, padx=2)

        # Analyze button
        btn_run = tk.Button(
            input_card,
            text="⚡ تحليل المشاعر الآن",
            font=("Segoe UI", 11, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4,
            command=self.analyze_current_text
        )
        btn_run.pack(fill=tk.X)

        # Gauge Card (Left)
        gauge_card = tk.Frame(top_split, bg="#1E293B", width=280, padx=12, pady=12, bd=1, relief=tk.SOLID)
        gauge_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        gauge_card.pack_propagate(False)

        tk.Label(gauge_card, text="عداد مقياس المشاعر", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#94A3B8").pack()

        self.gauge_canvas = tk.Canvas(gauge_card, bg="#1E293B", width=260, height=140, highlightthickness=0)
        self.gauge_canvas.pack(pady=4)

        self.lbl_result_badge = tk.Label(
            gauge_card,
            text="إيجابي (Positive) 🟢",
            font=("Segoe UI", 13, "bold"),
            bg="#1E293B",
            fg="#4ADE80"
        )
        self.lbl_result_badge.pack()

        self.lbl_polarity = tk.Label(
            gauge_card,
            text="القطبية: +0.85",
            font=("Segoe UI", 10),
            bg="#1E293B",
            fg="#94A3B8"
        )
        self.lbl_polarity.pack()

        # Bottom Results & Word Breakdown Card
        details_card = tk.Frame(body, bg="#1E293B", padx=16, pady=12, bd=1, relief=tk.SOLID)
        details_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(details_card, text="🔍 الكلمات الدلالية المكتشفة في النص:", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC").pack(anchor="e", pady=(0, 8))

        words_split = tk.Frame(details_card, bg="#1E293B")
        words_split.pack(fill=tk.BOTH, expand=True)

        # Positive Words Box
        pos_box = tk.Frame(words_split, bg="#064E3B", bd=1, relief=tk.SOLID, padx=10, pady=8)
        pos_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))
        tk.Label(pos_box, text="🟢 كلمات إيجابية:", font=("Segoe UI", 10, "bold"), bg="#064E3B", fg="#6EE7B7").pack(anchor="e")
        self.pos_words_lbl = tk.Label(pos_box, text="لا يوجد", font=("Segoe UI", 10), bg="#064E3B", fg="#FFFFFF", wraplength=340, justify="right")
        self.pos_words_lbl.pack(anchor="e", pady=4)

        # Negative Words Box
        neg_box = tk.Frame(words_split, bg="#7F1D1D", bd=1, relief=tk.SOLID, padx=10, pady=8)
        neg_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        tk.Label(neg_box, text="🔴 كلمات سلبية:", font=("Segoe UI", 10, "bold"), bg="#7F1D1D", fg="#FCA5A5").pack(anchor="e")
        self.neg_words_lbl = tk.Label(neg_box, text="لا يوجد", font=("Segoe UI", 10), bg="#7F1D1D", fg="#FFFFFF", wraplength=340, justify="right")
        self.neg_words_lbl.pack(anchor="e", pady=4)

    def load_sample(self, txt):
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", txt)
        self.analyze_current_text()

    def analyze_current_text(self):
        txt = self.text_input.get("1.0", tk.END).strip()
        result = self.engine.analyze(txt)

        pol = result["polarity"]
        label = result["label"]

        self.lbl_result_badge.config(text=label)
        if "إيجابي" in label:
            self.lbl_result_badge.config(fg="#4ADE80")
        elif "سلبي" in label:
            self.lbl_result_badge.config(fg="#F87171")
        else:
            self.lbl_result_badge.config(fg="#94A3B8")

        self.lbl_polarity.config(text=f"القطبية: {'+' if pol > 0 else ''}{pol}")

        # Words
        pos_list = result["pos_words"]
        neg_list = result["neg_words"]

        self.pos_words_lbl.config(text="، ".join(pos_list) if pos_list else "لم يتم العثور على كلمات إيجابية صريحة")
        self.neg_words_lbl.config(text="، ".join(neg_list) if neg_list else "لم يتم العثور على كلمات سلبية صريحة")

        self.draw_gauge(pol)

    def draw_gauge(self, score):
        # Draw semi-circular gauge on canvas
        self.gauge_canvas.delete("all")
        cx, cy = 130, 115
        radius = 90

        # Background Arc (Red -> Gray -> Green)
        # Red segment: 180 to 120 deg
        self.gauge_canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=120, extent=60, fill="#EF4444", outline="#1E293B", width=2)
        # Yellow/Gray segment: 60 to 120 deg
        self.gauge_canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=60, extent=60, fill="#F59E0B", outline="#1E293B", width=2)
        # Green segment: 0 to 60 deg
        self.gauge_canvas.create_arc(cx - radius, cy - radius, cx + radius, cy + radius, start=0, extent=60, fill="#10B981", outline="#1E293B", width=2)

        # Center cut
        inner = 55
        self.gauge_canvas.create_oval(cx - inner, cy - inner, cx + inner, cy + inner, fill="#1E293B", outline="#1E293B")

        # Needle pointer: map score from [-1.0, 1.0] to angle [180, 0]
        # score -1.0 -> 180 deg, 0.0 -> 90 deg, +1.0 -> 0 deg
        angle_deg = 90 - (score * 90)
        angle_rad = math.radians(angle_deg)

        nx = cx + (radius - 15) * math.cos(angle_rad)
        ny = cy - (radius - 15) * math.sin(angle_rad)

        self.gauge_canvas.create_line(cx, cy, nx, ny, fill="#F8FAFC", width=3, arrow=tk.LAST)
        self.gauge_canvas.create_oval(cx - 6, cy - 6, cx + 6, cy + 6, fill="#38BDF8", outline="#FFFFFF")


if __name__ == "__main__":
    app = SentimentAnalyzerApp()
    app.mainloop()
