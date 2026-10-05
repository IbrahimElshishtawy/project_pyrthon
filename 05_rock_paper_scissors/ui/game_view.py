# -*- coding: utf-8 -*-
"""
واجهة المستخدم للعبة حجر ورقة مقص التفاعلية
"""

import tkinter as tk
from tkinter import messagebox
from ui.theme import THEME


class RockPaperScissorsView(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg=THEME["bg"])
        self.engine = engine
        self.is_animating = False

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎮 تحدي حجر • ورقة • مقص",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_gold"]
        )
        title.pack()

        sub = tk.Label(
            header,
            text="اختر سلاحك وتحدى الذكاء الاصطناعي للكمبيوتر!",
            font=(THEME["font_family"], 10),
            bg=THEME["surface"],
            fg=THEME["text_muted"]
        )
        sub.pack()

        # Scoreboard
        scoreboard = tk.Frame(self, bg=THEME["surface_card"], pady=10, padx=20)
        scoreboard.pack(fill=tk.X)

        # Player
        p_frame = tk.Frame(scoreboard, bg=THEME["surface_card"])
        p_frame.pack(side=tk.RIGHT, expand=True)
        tk.Label(p_frame, text="👤 اللاعب (أنت)", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface_card"], fg=THEME["player_blue"]).pack()
        self.lbl_p_score = tk.Label(p_frame, text="0", font=(THEME["font_family"], 24, "bold"), bg=THEME["surface_card"], fg="#FFFFFF")
        self.lbl_p_score.pack()

        # Mid
        mid = tk.Frame(scoreboard, bg=THEME["surface_card"])
        mid.pack(side=tk.RIGHT, expand=True)
        self.lbl_streak = tk.Label(mid, text="🔥 السلسلة: 0 | تعادل: 0", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface_card"], fg="#FBBF24")
        self.lbl_streak.pack()
        self.lbl_winrate = tk.Label(mid, text="نسبة الفوز: 0%", font=(THEME["font_family"], 9), bg=THEME["surface_card"], fg=THEME["text_muted"])
        self.lbl_winrate.pack()

        # Computer
        c_frame = tk.Frame(scoreboard, bg=THEME["surface_card"])
        c_frame.pack(side=tk.RIGHT, expand=True)
        tk.Label(c_frame, text="🤖 الكمبيوتر", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface_card"], fg=THEME["comp_red"]).pack()
        self.lbl_c_score = tk.Label(c_frame, text="0", font=(THEME["font_family"], 24, "bold"), bg=THEME["surface_card"], fg="#FFFFFF")
        self.lbl_c_score.pack()

        # Battle Arena
        arena = tk.Frame(self, bg=THEME["bg"], pady=20)
        arena.pack(fill=tk.X)

        arena_inner = tk.Frame(arena, bg=THEME["surface"], bd=1, relief=tk.SOLID, padx=30, pady=16)
        arena_inner.pack()

        self.box_player = tk.Label(
            arena_inner,
            text="❔\nأنت",
            font=(THEME["font_family"], 28, "bold"),
            bg=THEME["surface_card"],
            fg=THEME["player_blue"],
            width=6,
            height=3,
            relief=tk.FLAT
        )
        self.box_player.pack(side=tk.RIGHT, padx=20)

        self.lbl_status = tk.Label(
            arena_inner,
            text="VS\nابدأ الجولة!",
            font=(THEME["font_family"], 14, "bold"),
            bg=THEME["surface"],
            fg=THEME["text_main"],
            width=14
        )
        self.lbl_status.pack(side=tk.RIGHT, padx=10)

        self.box_comp = tk.Label(
            arena_inner,
            text="❔\nالكمبيوتر",
            font=(THEME["font_family"], 28, "bold"),
            bg=THEME["surface_card"],
            fg=THEME["comp_red"],
            width=6,
            height=3,
            relief=tk.FLAT
        )
        self.box_comp.pack(side=tk.RIGHT, padx=20)

        # Choice Buttons
        btn_area = tk.Frame(self, bg=THEME["bg"], pady=10)
        btn_area.pack(fill=tk.X)

        tk.Label(btn_area, text="اضغط على اختيارك للعب الجولة:", font=(THEME["font_family"], 11, "bold"), bg=THEME["bg"], fg=THEME["text_muted"]).pack(pady=(0, 10))

        choices_frame = tk.Frame(btn_area, bg=THEME["bg"])
        choices_frame.pack()

        for key in ["rock", "paper", "scissors"]:
            item = self.engine.CHOICES[key]
            btn = tk.Button(
                choices_frame,
                text=f"{item['icon']}\n{item['name_ar']}",
                font=(THEME["font_family"], 14, "bold"),
                bg=THEME["surface_card"],
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

        # Bottom History
        bot_area = tk.Frame(self, bg=THEME["bg"], padx=20, pady=10)
        bot_area.pack(fill=tk.BOTH, expand=True)

        bot_head = tk.Frame(bot_area, bg=THEME["bg"])
        bot_head.pack(fill=tk.X, pady=(0, 4))
        tk.Label(bot_head, text="📜 سجل مواجهات الجولات:", font=(THEME["font_family"], 10, "bold"), bg=THEME["bg"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)
        tk.Button(bot_head, text="🔄 تصفير النتيجة", font=(THEME["font_family"], 9), bg="#374151", fg="#F87171", relief=tk.FLAT, cursor="hand2", command=self.on_reset).pack(side=tk.LEFT)

        self.listbox_history = tk.Listbox(
            bot_area,
            bg=THEME["surface"],
            fg="#E5E7EB",
            font=(THEME["font_family"], 10),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground=THEME["surface_card"]
        )
        self.listbox_history.pack(fill=tk.BOTH, expand=True)

    def play_round(self, player_key):
        if self.is_animating:
            return

        self.is_animating = True
        p_item = self.engine.CHOICES[player_key]
        self.box_player.config(text=f"{p_item['icon']}\nأنت", bg="#1E3A8A")

        comp_key = self.engine.get_computer_choice()
        countdown = ["✊\n3", "✋\n2", "✌\n1"]

        def step(idx):
            if idx < len(countdown):
                self.box_comp.config(text=countdown[idx], bg=THEME["surface_card"])
                self.after(250, lambda: step(idx + 1))
            else:
                self.finalize_round(player_key, comp_key)

        step(0)

    def finalize_round(self, player_key, comp_key):
        c_item = self.engine.CHOICES[comp_key]
        self.box_comp.config(text=f"{c_item['icon']}\nالكمبيوتر", bg="#7F1D1D")

        res = self.engine.evaluate_round(player_key, comp_key)

        self.lbl_status.config(text=res["msg"], fg=res["status_fg"])
        self.lbl_p_score.config(text=str(res["player_score"]))
        self.lbl_c_score.config(text=str(res["computer_score"]))
        self.lbl_streak.config(text=f"🔥 السلسلة: {res['streak']} (أفضل: {res['best_streak']}) | تعادل: {res['ties']}")
        self.lbl_winrate.config(text=f"نسبة الفوز: {res['win_rate']}% (إجمالي: {res['rounds']} جولة)")

        self.listbox_history.insert(0, res["log_entry"])
        self.is_animating = False

    def on_reset(self):
        if self.engine.rounds == 0:
            return
        if messagebox.askyesno("تأكيد التصفير", "هل تريد تصفير جميع النتائج والبدء من جديد؟"):
            self.engine.reset()
            self.lbl_p_score.config(text="0")
            self.lbl_c_score.config(text="0")
            self.lbl_streak.config(text="🔥 السلسلة: 0 | تعادل: 0")
            self.lbl_winrate.config(text="نسبة الفوز: 0%")
            self.box_player.config(text="❔\nأنت", bg=THEME["surface_card"])
            self.box_comp.config(text="❔\nالكمبيوتر", bg=THEME["surface_card"])
            self.lbl_status.config(text="VS\nابدأ الجولة!", fg=THEME["text_main"])
            self.listbox_history.delete(0, tk.END)
