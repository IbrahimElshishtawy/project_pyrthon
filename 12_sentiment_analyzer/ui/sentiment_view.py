# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمحلل مشاعر النصوص
"""

import tkinter as tk
from ui.theme import THEME
from ui.gauge_canvas import draw_sentiment_gauge


class SentimentAnalyzerView(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg=THEME["bg"])
        self.engine = engine

        self.setup_ui()
        self.analyze_text()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🧠 محلل مشاعر النصوص والتعليقات الذكي (عربي / English)",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        sub = tk.Label(
            header,
            text="اكتشف انطباعات العملاء وتقييمات المنتجات فورياً",
            font=(THEME["font_family"], 9),
            bg=THEME["surface"],
            fg=THEME["text_muted"]
        )
        sub.pack(side=tk.RIGHT, padx=(0, 10))

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        top_split = tk.Frame(body, bg=THEME["bg"])
        top_split.pack(fill=tk.X, pady=(0, 12))

        # Input Card (Right)
        input_card = tk.Frame(top_split, bg=THEME["surface"], padx=14, pady=12, bd=1, relief=tk.SOLID)
        input_card.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))

        tk.Label(input_card, text="اكتب أو الصق التعليق المراد تحليله:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 6))

        self.text_input = tk.Text(
            input_card,
            font=(THEME["font_family"], 11),
            bg=THEME["bg"],
            fg="#FFFFFF",
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT,
            height=5,
            wrap=tk.WORD
        )
        self.text_input.pack(fill=tk.BOTH, expand=True, pady=(0, 8))
        self.text_input.insert("1.0", "المنتج ممتاز جداً والتوصيل كان سريع ورائع، شكراً جزيلاً!")

        # Samples
        samples_bar = tk.Frame(input_card, bg=THEME["surface"])
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
                font=(THEME["font_family"], 8),
                bg=THEME["surface_light"],
                fg="#E2E8F0",
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda t=txt: self.load_sample(t)
            )
            btn.pack(side=tk.RIGHT, padx=2)

        btn_run = tk.Button(
            input_card,
            text="⚡ تحليل المشاعر الآن",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4,
            command=self.analyze_text
        )
        btn_run.pack(fill=tk.X)

        # Gauge Card (Left)
        gauge_card = tk.Frame(top_split, bg=THEME["surface"], width=280, padx=12, pady=12, bd=1, relief=tk.SOLID)
        gauge_card.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 8))
        gauge_card.pack_propagate(False)

        tk.Label(gauge_card, text="عداد مقياس المشاعر", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_muted"]).pack()

        self.gauge_canvas = tk.Canvas(gauge_card, bg=THEME["surface"], width=260, height=140, highlightthickness=0)
        self.gauge_canvas.pack(pady=4)

        self.lbl_badge = tk.Label(gauge_card, text="إيجابي (Positive) 🟢", font=(THEME["font_family"], 13, "bold"), bg=THEME["surface"], fg=THEME["success"])
        self.lbl_badge.pack()

        self.lbl_pol = tk.Label(gauge_card, text="القطبية: +0.85", font=(THEME["font_family"], 10), bg=THEME["surface"], fg=THEME["text_muted"])
        self.lbl_pol.pack()

        # Bottom Breakdown
        details_card = tk.Frame(body, bg=THEME["surface"], padx=16, pady=12, bd=1, relief=tk.SOLID)
        details_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(details_card, text="🔍 الكلمات الدلالية المكتشفة في النص:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 8))

        words_split = tk.Frame(details_card, bg=THEME["surface"])
        words_split.pack(fill=tk.BOTH, expand=True)

        # Positive Box
        pos_box = tk.Frame(words_split, bg="#064E3B", bd=1, relief=tk.SOLID, padx=10, pady=8)
        pos_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(4, 0))
        tk.Label(pos_box, text="🟢 كلمات إيجابية:", font=(THEME["font_family"], 10, "bold"), bg="#064E3B", fg="#6EE7B7").pack(anchor="e")
        self.pos_words_lbl = tk.Label(pos_box, text="لا يوجد", font=(THEME["font_family"], 10), bg="#064E3B", fg="#FFFFFF", wraplength=340, justify="right")
        self.pos_words_lbl.pack(anchor="e", pady=4)

        # Negative Box
        neg_box = tk.Frame(words_split, bg="#7F1D1D", bd=1, relief=tk.SOLID, padx=10, pady=8)
        neg_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        tk.Label(neg_box, text="🔴 كلمات سلبية:", font=(THEME["font_family"], 10, "bold"), bg="#7F1D1D", fg="#FCA5A5").pack(anchor="e")
        self.neg_words_lbl = tk.Label(neg_box, text="لا يوجد", font=(THEME["font_family"], 10), bg="#7F1D1D", fg="#FFFFFF", wraplength=340, justify="right")
        self.neg_words_lbl.pack(anchor="e", pady=4)

    def load_sample(self, txt):
        self.text_input.delete("1.0", tk.END)
        self.text_input.insert("1.0", txt)
        self.analyze_text()

    def analyze_text(self):
        txt = self.text_input.get("1.0", tk.END).strip()
        res = self.engine.analyze(txt)

        pol = res["polarity"]
        label = res["label"]

        self.lbl_badge.config(text=label)
        if "إيجابي" in label:
            self.lbl_badge.config(fg=THEME["success"])
        elif "سلبي" in label:
            self.lbl_badge.config(fg=THEME["danger"])
        else:
            self.lbl_badge.config(fg=THEME["text_muted"])

        self.lbl_pol.config(text=f"القطبية: {'+' if pol > 0 else ''}{pol}")

        pos_list = res["pos_words"]
        neg_list = res["neg_words"]
        self.pos_words_lbl.config(text="، ".join(pos_list) if pos_list else "لم يتم العثور على كلمات إيجابية صريحة")
        self.neg_words_lbl.config(text="، ".join(neg_list) if neg_list else "لم يتم العثور على كلمات سلبية صريحة")

        draw_sentiment_gauge(self.gauge_canvas, pol)
