# -*- coding: utf-8 -*-
"""
واجهة المستخدم لتطبيق الدردشة الفورية
"""

from datetime import datetime
import time
import tkinter as tk
from tkinter import messagebox
from ui.theme import THEME


class ChatView(tk.Frame):
    def __init__(self, parent, network):
        super().__init__(parent, bg=THEME["bg"])
        self.network = network
        self.username = "مستخدم_" + str(int(time.time()) % 1000)
        self.current_room = "#العامة"

        # Bind callbacks
        self.network.on_msg = self.on_message_received
        self.network.on_status = self.add_system_message

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="💬 تطبيق الدردشة الفورية المتعدد (LAN Chat)",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        self.status_badge = tk.Label(
            header,
            text="⚫ غير متصل",
            font=(THEME["font_family"], 10, "bold"),
            bg="#334155",
            fg=THEME["text_muted"],
            padx=12,
            pady=4
        )
        self.status_badge.pack(side=tk.LEFT)

        # Connection Control Bar
        conn_bar = tk.Frame(self, bg=THEME["surface"], padx=16, pady=8, bd=1, relief=tk.SOLID)
        conn_bar.pack(fill=tk.X, padx=16, pady=(10, 0))

        self.btn_host = tk.Button(
            conn_bar,
            text="🏠 استضافة سيرفر محلي (Host Server)",
            font=(THEME["font_family"], 9, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.on_start_host
        )
        self.btn_host.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_connect = tk.Button(
            conn_bar,
            text="🔗 انضمام لمحادثة (Connect)",
            font=(THEME["font_family"], 9, "bold"),
            bg=THEME["success"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.on_connect
        )
        self.btn_connect.pack(side=tk.LEFT, padx=(0, 10))

        self.port_entry = tk.Entry(conn_bar, font=(THEME["font_family"], 10), bg=THEME["bg"], fg=THEME["accent_cyan"], relief=tk.FLAT, width=6)
        self.port_entry.pack(side=tk.RIGHT, padx=4)
        self.port_entry.insert(0, "65432")
        tk.Label(conn_bar, text="المنفذ:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)

        self.host_entry = tk.Entry(conn_bar, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#FFFFFF", relief=tk.FLAT, width=12)
        self.host_entry.pack(side=tk.RIGHT, padx=4)
        self.host_entry.insert(0, "127.0.0.1")
        tk.Label(conn_bar, text="العنوان:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)

        self.user_entry = tk.Entry(conn_bar, font=(THEME["font_family"], 10), bg=THEME["bg"], fg="#4ADE80", relief=tk.FLAT, width=12)
        self.user_entry.pack(side=tk.RIGHT, padx=4)
        self.user_entry.insert(0, self.username)
        tk.Label(conn_bar, text="اسمك:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT)

        # Main Workspace
        split = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        split.pack(fill=tk.BOTH, expand=True)

        # Sidebar Left
        sidebar = tk.Frame(split, bg=THEME["surface"], width=220, bd=1, relief=tk.SOLID)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="📌 غرف المحادثة:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["accent_cyan"], padx=10, pady=6).pack(anchor="w")
        self.rooms_listbox = tk.Listbox(sidebar, bg=THEME["bg"], fg="#E2E8F0", font=(THEME["font_family"], 10), height=4, relief=tk.FLAT, selectbackground=THEME["primary"])
        self.rooms_listbox.pack(fill=tk.X, padx=8, pady=(0, 10))
        for r in ["#العامة", "#التقنية_والبرمجة", "#الاستراحة"]:
            self.rooms_listbox.insert(tk.END, r)
        self.rooms_listbox.select_set(0)
        self.rooms_listbox.bind("<<ListboxSelect>>", self.on_room_changed)

        tk.Label(sidebar, text="👥 المتواجدون الآن:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["success"], padx=10, pady=4).pack(anchor="w")
        self.users_listbox = tk.Listbox(sidebar, bg=THEME["bg"], fg="#E2E8F0", font=(THEME["font_family"], 9), relief=tk.FLAT, selectbackground="#334155")
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Main Chat Box Right
        chat_box = tk.Frame(split, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        chat_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.msg_display = tk.Text(
            chat_box,
            bg=THEME["bg"],
            fg="#F8FAFC",
            font=(THEME["font_family"], 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED,
            padx=12,
            pady=10
        )
        self.msg_display.pack(fill=tk.BOTH, expand=True)

        self.msg_display.tag_config("me", foreground=THEME["my_msg"])
        self.msg_display.tag_config("other", foreground=THEME["other_msg"])
        self.msg_display.tag_config("system", foreground=THEME["text_muted"], font=(THEME["font_family"], 9, "italic"))

        # Input Row
        input_bar = tk.Frame(chat_box, bg=THEME["surface"], padx=8, pady=8)
        input_bar.pack(fill=tk.X)

        self.input_entry = tk.Entry(
            input_bar,
            font=(THEME["font_family"], 11),
            bg=THEME["bg"],
            fg="#FFFFFF",
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))
        self.input_entry.bind("<Return>", lambda e: self.on_send())

        btn_send = tk.Button(
            input_bar,
            text="إرسال 🚀",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            command=self.on_send
        )
        btn_send.pack(side=tk.RIGHT)

        self.add_system_message("مرحباً بك! قم باستضافة سيرفر محلي أو اتصل بسيرفر قائم للبدء بالمحادثة.")

    def on_room_changed(self, event):
        sel = self.rooms_listbox.curselection()
        if sel:
            self.current_room = self.rooms_listbox.get(sel[0])
            self.add_system_message(f"انتقلت إلى الغرفة {self.current_room}")

    def add_system_message(self, text):
        t = datetime.now().strftime("%H:%M")
        self.msg_display.config(state=tk.NORMAL)
        self.msg_display.insert(tk.END, f"[{t}] ⚙️ {text}\n", "system")
        self.msg_display.see(tk.END)
        self.msg_display.config(state=tk.DISABLED)

    def on_message_received(self, payload):
        p_type = payload.get("type")
        if p_type == "msg":
            u = payload.get("user")
            r = payload.get("room")
            txt = payload.get("text")
            is_me = (u == self.username)
            t = datetime.now().strftime("%H:%M")
            self.msg_display.config(state=tk.NORMAL)
            tag = "me" if is_me else "other"
            self.msg_display.insert(tk.END, f"[{t}] {u} ({r}): ", tag)
            self.msg_display.insert(tk.END, f"{txt}\n")
            self.msg_display.see(tk.END)
            self.msg_display.config(state=tk.DISABLED)
        elif p_type == "join":
            u = payload.get("user")
            if u != self.username:
                self.add_system_message(f"انضم {u} إلى المحادثة! 👋")
                self.users_listbox.insert(tk.END, f"• {u}")

    def on_start_host(self):
        try:
            port = int(self.port_entry.get().strip())
            self.network.start_host(port)
            self.btn_host.config(state=tk.DISABLED)
            self.host_entry.delete(0, tk.END)
            self.host_entry.insert(0, "127.0.0.1")
            self.on_connect()
        except Exception as e:
            messagebox.showerror("خطأ في تشغيل السيرفر", str(e))

    def on_connect(self):
        host = self.host_entry.get().strip()
        port = int(self.port_entry.get().strip())
        self.username = self.user_entry.get().strip() or "ضيف"

        try:
            self.network.connect(host, port, self.username)
            self.status_badge.config(text=f"🟢 متصل ({self.username})", bg="#065F46", fg="#A7F3D0")
            self.btn_connect.config(state=tk.DISABLED, text="متصل حالياً")
            self.users_listbox.insert(tk.END, f"• {self.username} (أنت)")
        except Exception as e:
            messagebox.showerror("خطأ في الاتصال", f"تعذر الاتصال:\n{e}")

    def on_send(self):
        txt = self.input_entry.get().strip()
        if not txt:
            return
        try:
            self.network.send_chat(self.username, self.current_room, txt)
            self.input_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showwarning("تنبيه", str(e))
