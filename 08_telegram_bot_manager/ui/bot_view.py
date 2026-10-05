# -*- coding: utf-8 -*-
"""
واجهة المستخدم للوحة تحكم ومحاكي بوت تيليجرام
"""

from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from ui.theme import THEME


class TelegramBotView(tk.Frame):
    def __init__(self, parent, bot_service):
        super().__init__(parent, bg=THEME["bg"])
        self.bot_service = bot_service

        # Bind event logger
        self.bot_service.on_event = self.log_event

        self.setup_ui()
        self.log_event("النظام", "تم تهيئة لوحة التحكم بنجاح! يمكنك استخدام المحاكي الفوري أو تشغيل البوت الحقيقي.")

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🤖 لوحة تحكم ومحاكي بوت تيليجرام",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["telegram_blue"]
        )
        title.pack(side=tk.RIGHT)

        self.bot_badge = tk.Label(
            header,
            text="⚫ البوت متوقف",
            font=(THEME["font_family"], 10, "bold"),
            bg="#2B5278",
            fg="#FFFFFF",
            padx=12,
            pady=4
        )
        self.bot_badge.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Config Card
        config_card = tk.Frame(body, bg=THEME["surface"], padx=14, pady=10, bd=1, relief=tk.SOLID)
        config_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(config_card, text="توكن البوت (Bot Token):", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(side=tk.RIGHT, padx=(6, 0))

        self.token_entry = tk.Entry(
            config_card,
            font=("Consolas", 10),
            bg=THEME["bg"],
            fg=THEME["telegram_blue"],
            insertbackground=THEME["telegram_blue"],
            relief=tk.FLAT,
            show="•"
        )
        self.token_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=8, ipady=3)

        self.btn_toggle = tk.Button(
            config_card,
            text="▶ تشغيل البوت الحقيقي",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["success"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            command=self.on_toggle_bot
        )
        self.btn_toggle.pack(side=tk.LEFT)

        # Columns
        cols_frame = tk.Frame(body, bg=THEME["bg"])
        cols_frame.pack(fill=tk.BOTH, expand=True)

        # Left Column: Live Event Log
        left_frame = tk.Frame(cols_frame, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        log_head = tk.Frame(left_frame, bg=THEME["surface"], padx=10, pady=8)
        log_head.pack(fill=tk.X)
        tk.Label(log_head, text="📜 سجل الأحداث والرسائل الحية (Live Console)", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["telegram_blue"]).pack(side=tk.LEFT)
        tk.Button(log_head, text="مسح", font=(THEME["font_family"], 8), bg="#2B5278", fg="#FFFFFF", relief=tk.FLAT, command=self.clear_log).pack(side=tk.RIGHT)

        self.log_text = tk.Text(
            left_frame,
            bg=THEME["bg"],
            fg="#E4ECF2",
            font=("Consolas", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=8,
            pady=8
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Right Column: Simulator & Broadcast
        right_frame = tk.Frame(cols_frame, bg=THEME["bg"], width=380)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(8, 0))
        right_frame.pack_propagate(False)

        # Simulator Box
        sim_card = tk.Frame(right_frame, bg=THEME["surface"], padx=14, pady=12, bd=1, relief=tk.SOLID)
        sim_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(sim_card, text="📱 محاكي رسائل المستخدم (Test Chat)", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["telegram_blue"]).pack(anchor="e", pady=(0, 4))
        tk.Label(sim_card, text="أرسل أمراً للبوت لتجربة ردوده مباشرة:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(anchor="e", pady=(0, 6))

        self.sim_entry = tk.Entry(sim_card, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["telegram_blue"], relief=tk.FLAT)
        self.sim_entry.pack(fill=tk.X, ipady=4, pady=(0, 6))
        self.sim_entry.bind("<Return>", lambda e: self.send_sim_command())

        quick_cmds = tk.Frame(sim_card, bg=THEME["surface"])
        quick_cmds.pack(fill=tk.X, pady=(0, 8))

        for cmd in ["/start", "/weather Cairo", "/quote", "/remind 5 القهوة", "/help"]:
            b = tk.Button(
                quick_cmds,
                text=cmd,
                font=(THEME["font_family"], 8),
                bg=THEME["surface_light"],
                fg=THEME["telegram_blue"],
                relief=tk.FLAT,
                cursor="hand2",
                command=lambda c=cmd: self.run_quick_cmd(c)
            )
            b.pack(side=tk.RIGHT, padx=2, pady=2)

        send_sim_btn = tk.Button(
            sim_card,
            text="💬 إرسال الرسالة إلى البوت",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["telegram_blue"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.send_sim_command
        )
        send_sim_btn.pack(fill=tk.X, ipady=3)

        # Broadcast Box
        broad_card = tk.Frame(right_frame, bg=THEME["surface"], padx=14, pady=12, bd=1, relief=tk.SOLID)
        broad_card.pack(fill=tk.BOTH, expand=True)

        tk.Label(broad_card, text="📢 إرسال رسالة بث (Broadcast)", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 4))
        tk.Label(broad_card, text="إرسال إشعار للمشتركين:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(anchor="e", pady=(0, 6))

        self.broad_text = tk.Text(broad_card, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", insertbackground=THEME["telegram_blue"], relief=tk.FLAT, height=6, wrap=tk.WORD)
        self.broad_text.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        send_broad_btn = tk.Button(
            broad_card,
            text="🚀 إرسال البث للجميع",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["gold"],
            fg="#000000",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.on_send_broadcast
        )
        send_broad_btn.pack(fill=tk.X, ipady=4)

    def log_event(self, source, message):
        t = datetime.now().strftime("%H:%M:%S")
        line = f"[{t}] [{source}]: {message}\n"
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete("1.0", tk.END)

    def run_quick_cmd(self, cmd):
        self.sim_entry.delete(0, tk.END)
        self.sim_entry.insert(0, cmd)
        self.send_sim_command()

    def send_sim_command(self):
        txt = self.sim_entry.get().strip()
        if not txt:
            return
        self.sim_entry.delete(0, tk.END)
        self.log_event("👤 المستخدم (المحاكي)", txt)
        reply = self.bot_service.process_command(txt, "المستخدم")
        self.log_event("🤖 البوت", reply)

    def on_send_broadcast(self):
        msg = self.broad_text.get("1.0", tk.END).strip()
        if not msg:
            messagebox.showwarning("تنبيه", "يرجى كتابة نص الرسالة للبث!")
            return
        self.log_event("📢 بث عام", f"إرسال: \"{msg}\"")
        self.broad_text.delete("1.0", tk.END)
        messagebox.showinfo("نجاح", "تم إرسال رسالة البث بنجاح!")

    def on_toggle_bot(self):
        if not self.bot_service.is_running:
            token = self.token_entry.get().strip()
            if not token:
                if messagebox.askyesno("توكن البوت مفقود", "لم تقم بإدخال توكن حقيقي.\nهل تريد تشغيل وضع المحاكي التفاعلي الفوري؟"):
                    self.bot_service.is_running = True
                    self.btn_toggle.config(text="⏹ إيقاف المحاكي", bg=THEME["danger"])
                    self.bot_badge.config(text="🟢 المحاكي يعمل بنشاط", bg=THEME["success"])
                    self.log_event("النظام", "البوت يعمل الآن في وضع المحاكي التفاعلي!")
                return

            self.btn_toggle.config(text="⏹ إيقاف البوت", bg=THEME["danger"])
            self.bot_badge.config(text="🟢 البوت الحقيقي متصل", bg=THEME["success"])
            self.log_event("النظام", "جارٍ الاتصال بسيرفرات Telegram Bot API...")
            self.bot_service.start_real_bot(token)
        else:
            self.bot_service.stop_bot()
            self.btn_toggle.config(text="▶ تشغيل البوت", bg=THEME["success"])
            self.bot_badge.config(text="⚫ البوت متوقف", bg="#2B5278")
            self.log_event("النظام", "تم إيقاف عمل البوت.")
