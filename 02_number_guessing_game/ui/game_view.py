# -*- coding: utf-8 -*-
"""
واجهة المستخدم للعبة تخمين الرقم
"""

import tkinter as tk
from tkinter import messagebox
from ui.theme import THEME


class NumberGuessingGameView(tk.Frame):
    def __init__(self, parent, logic):
        super().__init__(parent, bg=THEME["bg"])
        self.logic = logic

        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        # Header Card
        header = tk.Frame(self, bg=THEME["surface"], pady=14)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎯 لعبة تخمين الرقم الذكية",
            font=(THEME["font_family"], 20, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack()

        subtitle = tk.Label(
            header,
            text="خمن الرقم الذي اختاره الكمبيوتر بأقل عدد من المحاولات!",
            font=(THEME["font_family"], 11),
            bg=THEME["surface"],
            fg="#A5B4FC"
        )
        subtitle.pack(pady=(2, 0))

        # Main Workspace Container
        body = tk.Frame(self, bg=THEME["bg"], padx=20, pady=16)
        body.pack(fill=tk.BOTH, expand=True)

        # Control Bar: Difficulty & High Score
        ctrl_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        ctrl_card.pack(fill=tk.X, pady=(0, 14), ipady=8, padx=4)

        diff_lbl = tk.Label(ctrl_card, text="المستوى:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg="#FFFFFF")
        diff_lbl.pack(side=tk.RIGHT, padx=(10, 14))

        self.diff_var = tk.StringVar(value=self.logic.current_diff)
        for diff_name in self.logic.DIFFICULTIES.keys():
            rb = tk.Radiobutton(
                ctrl_card,
                text=diff_name,
                variable=self.diff_var,
                value=diff_name,
                font=(THEME["font_family"], 10),
                bg=THEME["surface"],
                fg="#E2E8F0",
                selectcolor=THEME["surface_light"],
                activebackground=THEME["surface"],
                activeforeground=THEME["accent_cyan"],
                command=self.on_diff_changed
            )
            rb.pack(side=tk.RIGHT, padx=6)

        self.high_score_lbl = tk.Label(
            ctrl_card,
            text=f"🏆 أفضل نتيجة: {self.logic.high_score or '--'}",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["surface"],
            fg=THEME["gold"]
        )
        self.high_score_lbl.pack(side=tk.LEFT, padx=14)

        # Center Status Display Card
        card = tk.Frame(body, bg=THEME["surface"], pady=16, padx=16, bd=1, relief=tk.FLAT)
        card.pack(fill=tk.X, pady=(0, 14))

        self.hint_icon = tk.Label(card, text="🤔", font=(THEME["font_family"], 36), bg=THEME["surface"])
        self.hint_icon.pack()

        self.hint_text = tk.Label(card, text="أنا اخترت رقماً، خمن كم هو!", font=(THEME["font_family"], 15, "bold"), bg=THEME["surface"], fg=THEME["text_main"])
        self.hint_text.pack(pady=4)

        self.range_text = tk.Label(card, text="النطاق: 1 إلى 100", font=(THEME["font_family"], 11), bg=THEME["surface"], fg=THEME["text_muted"])
        self.range_text.pack()

        self.attempts_badge = tk.Label(
            card,
            text="المحاولات المتبقية: 7 / 7",
            font=(THEME["font_family"], 11, "bold"),
            bg=THEME["surface_light"],
            fg="#FFFFFF",
            padx=12,
            pady=4
        )
        self.attempts_badge.pack(pady=(10, 0))

        # Input Row
        input_frame = tk.Frame(body, bg=THEME["bg"])
        input_frame.pack(fill=tk.X, pady=(0, 14))

        self.entry_guess = tk.Entry(
            input_frame,
            font=(THEME["font_family"], 18, "bold"),
            justify="center",
            width=10,
            bg=THEME["surface"],
            fg=THEME["accent_cyan"],
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT,
            bd=2
        )
        self.entry_guess.pack(side=tk.LEFT, expand=True, ipady=6, padx=(0, 8))
        self.entry_guess.bind("<Return>", lambda e: self.on_guess())

        self.btn_submit = tk.Button(
            input_frame,
            text="تأكيد التخمين (Enter)",
            font=(THEME["font_family"], 12, "bold"),
            bg=THEME["accent_blue"],
            fg="#03045E",
            activebackground="#0096C7",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            command=self.on_guess
        )
        self.btn_submit.pack(side=tk.LEFT, ipady=6, padx=(0, 8))

        self.btn_replay = tk.Button(
            input_frame,
            text="🔄 لعبة جديدة",
            font=(THEME["font_family"], 12),
            bg=THEME["surface_light"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            command=self.start_game
        )
        self.btn_replay.pack(side=tk.LEFT, ipady=6)

        # History Box
        hist_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        hist_card.pack(fill=tk.BOTH, expand=True)

        h_title = tk.Label(hist_card, text="📋 سجل محاولاتك في هذه الجولة:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_muted"], anchor="w", padx=12, pady=6)
        h_title.pack(fill=tk.X)

        self.listbox_history = tk.Listbox(
            hist_card,
            bg=THEME["bg"],
            fg="#E2E8F0",
            font=(THEME["font_family"], 11),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground=THEME["surface_light"]
        )
        self.listbox_history.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

    def on_diff_changed(self):
        self.logic.current_diff = self.diff_var.get()
        self.start_game()

    def start_game(self):
        self.logic.start_game()
        low, high, max_att = self.logic.DIFFICULTIES[self.logic.current_diff]

        self.range_text.config(text=f"النطاق المطلوب: من {low} إلى {high}")
        self.hint_icon.config(text="🤔")
        self.hint_text.config(text="أنا اخترت رقماً، خمن كم هو!", fg=THEME["text_main"])
        self.attempts_badge.config(text=f"المحاولات المتبقية: {max_att} / {max_att}", bg=THEME["surface_light"])
        self.entry_guess.config(state=tk.NORMAL)
        self.btn_submit.config(state=tk.NORMAL)
        self.entry_guess.delete(0, tk.END)
        self.listbox_history.delete(0, tk.END)
        self.entry_guess.focus()

    def on_guess(self):
        val = self.entry_guess.get().strip()
        if not val.isdigit():
            messagebox.showwarning("تنبيه", "يرجى إدخال رقم صحيح فقط!")
            return

        res = self.logic.guess(int(val))
        self.entry_guess.delete(0, tk.END)

        if res["status"] == "out_of_range":
            messagebox.showwarning("خارج النطاق", f"يرجى إدخال رقم بين {res['low']} و {res['high']}!")
            return

        # Update Listbox
        self.listbox_history.delete(0, tk.END)
        for item in self.logic.history:
            self.listbox_history.insert(tk.END, item)

        if res["status"] == "win":
            self.hint_icon.config(text="🎉")
            self.hint_text.config(text=f"مبروك! إجابة صحيحة ({res['secret']}) في {res['attempts']} محاولة!", fg=THEME["success"])
            self.attempts_badge.config(text="انتصار! 🏆", bg="#15803D")
            self.entry_guess.config(state=tk.DISABLED)
            self.btn_submit.config(state=tk.DISABLED)
            if res.get("new_high"):
                self.high_score_lbl.config(text=f"🏆 أفضل نتيجة: {res['attempts']} محاولة!")
        elif res["status"] == "loss":
            self.hint_icon.config(text="💀")
            self.hint_text.config(text=f"للأسف نفدت المحاولات! الرقم كان: {res['secret']}", fg=THEME["danger"])
            self.attempts_badge.config(text="انتهت اللعبة! ❌", bg="#B91C1C")
            self.entry_guess.config(state=tk.DISABLED)
            self.btn_submit.config(state=tk.DISABLED)
        else:
            diff = res["diff"]
            self.hint_icon.config(text="🔥" if diff <= 5 else "🧭")
            self.hint_text.config(
                text=f"الرقم الصحيح {res['direction']} - {res['closeness']}",
                fg=THEME["gold"] if diff <= 10 else "#60A5FA"
            )
            self.attempts_badge.config(
                text=f"المحاولات المتبقية: {res['attempts_left']} / {self.logic.max_attempts}",
                bg="#B45309" if res["attempts_left"] <= 2 else THEME["surface_light"]
            )
