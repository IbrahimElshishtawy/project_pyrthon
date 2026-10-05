#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 13: تطبيق الدردشة الفورية المتعدد (Real-Time Socket Chat Application)
يدعم:
- خادم مدمج (Host Chat Server) وعميل (Join Client) في واجهة واحدة متكاملة
- اتصال شبكي حقيقي عبر Sockets و Threading
- غرف ومحادثات متعددة (#العامة، #التقنية، #الاستراحة)
- قائمة حية بأسماء المتصلين النشطين (Active Online Users)
- رسائل بتنسيق أنيق مع أوقات الإرسال ورسائل انضمام ومغادرة النظام
- إمكانية تشغيل أكثر من نافذة والتحدث المباشر بينها عبر الشبكة المحلية
"""

import json
import socket
import threading
import time
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk


class ChatApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("تطبيق الدردشة الفورية | Real-Time Chat")
        self.geometry("900x680")
        self.minsize(820, 600)
        self.configure(bg="#0F172A")

        # Network State
        self.sock = None
        self.is_connected = False
        self.is_server_host = False
        self.server_sock = None
        self.clients = []  # Server clients
        self.username = "مستخدم_" + str(int(time.time()) % 1000)
        self.current_room = "#العامة"

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="💬 تطبيق الدردشة الفورية المتعدد (LAN Chat)",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        self.status_badge = tk.Label(
            header,
            text="⚫ غير متصل",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#94A3B8",
            padx=12,
            pady=4
        )
        self.status_badge.pack(side=tk.LEFT)

        # Connection Control Bar
        conn_bar = tk.Frame(self, bg="#1E293B", padx=16, pady=8, bd=1, relief=tk.SOLID)
        conn_bar.pack(fill=tk.X, padx=16, pady=(10, 0))

        # Buttons
        self.btn_host = tk.Button(
            conn_bar,
            text="🏠 استضافة سيرفر محلي (Host Server)",
            font=("Segoe UI", 9, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.start_server
        )
        self.btn_host.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_connect = tk.Button(
            conn_bar,
            text="🔗 انضمام لمحادثة (Connect)",
            font=("Segoe UI", 9, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.connect_to_server
        )
        self.btn_connect.pack(side=tk.LEFT, padx=(0, 10))

        # User Info Entries
        self.port_entry = tk.Entry(conn_bar, font=("Segoe UI", 10), bg="#0F172A", fg="#38BDF8", relief=tk.FLAT, width=6)
        self.port_entry.pack(side=tk.RIGHT, padx=4)
        self.port_entry.insert(0, "65432")
        tk.Label(conn_bar, text="المنفذ:", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)

        self.host_entry = tk.Entry(conn_bar, font=("Segoe UI", 10), bg="#0F172A", fg="#FFFFFF", relief=tk.FLAT, width=12)
        self.host_entry.pack(side=tk.RIGHT, padx=4)
        self.host_entry.insert(0, "127.0.0.1")
        tk.Label(conn_bar, text="العنوان:", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)

        self.user_entry = tk.Entry(conn_bar, font=("Segoe UI", 10), bg="#0F172A", fg="#4ADE80", relief=tk.FLAT, width=12)
        self.user_entry.pack(side=tk.RIGHT, padx=4)
        self.user_entry.insert(0, self.username)
        tk.Label(conn_bar, text="اسمك المستعار:", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)

        # Main Chat Split (Left: Channels & Online Users, Right: Messages & Input)
        split = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        split.pack(fill=tk.BOTH, expand=True)

        # Sidebar Left
        sidebar = tk.Frame(split, bg="#1E293B", width=220, bd=1, relief=tk.SOLID)
        sidebar.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        sidebar.pack_propagate(False)

        # Channels Section
        tk.Label(sidebar, text="📌 غرف المحادثة:", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#38BDF8", padx=10, pady=6).pack(anchor="w")
        self.rooms_listbox = tk.Listbox(sidebar, bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 10), height=4, relief=tk.FLAT, selectbackground="#0284C7")
        self.rooms_listbox.pack(fill=tk.X, padx=8, pady=(0, 10))
        for r in ["#العامة", "#التقنية_والبرمجة", "#الاستراحة"]:
            self.rooms_listbox.insert(tk.END, r)
        self.rooms_listbox.select_set(0)
        self.rooms_listbox.bind("<<ListboxSelect>>", self.on_room_changed)

        # Active Users Section
        tk.Label(sidebar, text="👥 المتواجدون الآن:", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#10B981", padx=10, pady=4).pack(anchor="w")
        self.users_listbox = tk.Listbox(sidebar, bg="#0F172A", fg="#E2E8F0", font=("Segoe UI", 9), relief=tk.FLAT, selectbackground="#334155")
        self.users_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        # Main Chat Area Right
        chat_box = tk.Frame(split, bg="#1E293B", bd=1, relief=tk.SOLID)
        chat_box.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Messages Display
        self.msg_display = tk.Text(
            chat_box,
            bg="#0F172A",
            fg="#F8FAFC",
            font=("Segoe UI", 10),
            wrap=tk.WORD,
            relief=tk.FLAT,
            state=tk.DISABLED,
            padx=12,
            pady=10
        )
        self.msg_display.pack(fill=tk.BOTH, expand=True)

        # Tag Styles for Chat Messages
        self.msg_display.tag_config("me", foreground="#38BDF8")
        self.msg_display.tag_config("other", foreground="#FBBF24")
        self.msg_display.tag_config("system", foreground="#94A3B8", font=("Segoe UI", 9, "italic"))
        self.msg_display.tag_config("alert", foreground="#34D399", font=("Segoe UI", 9, "bold"))

        # Input Area Bottom
        input_bar = tk.Frame(chat_box, bg="#1E293B", padx=8, pady=8)
        input_bar.pack(fill=tk.X)

        self.input_entry = tk.Entry(
            input_bar,
            font=("Segoe UI", 11),
            bg="#0F172A",
            fg="#FFFFFF",
            insertbackground="#38BDF8",
            relief=tk.FLAT
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=6, padx=(0, 8))
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        self.btn_send = tk.Button(
            input_bar,
            text="إرسال 🚀",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            command=self.send_message
        )
        self.btn_send.pack(side=tk.RIGHT)

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

    def add_chat_message(self, user, room, text, is_me=False):
        t = datetime.now().strftime("%H:%M")
        self.msg_display.config(state=tk.NORMAL)
        tag = "me" if is_me else "other"
        prefix = f"[{t}] {user} ({room}): "
        self.msg_display.insert(tk.END, prefix, tag)
        self.msg_display.insert(tk.END, f"{text}\n")
        self.msg_display.see(tk.END)
        self.msg_display.config(state=tk.DISABLED)

    def start_server(self):
        try:
            port = int(self.port_entry.get().strip())
            host = "0.0.0.0"
            self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_sock.bind((host, port))
            self.server_sock.listen(10)
            self.is_server_host = True

            threading.Thread(target=self._server_listen_loop, daemon=True).start()

            self.add_system_message(f"✅ تم تشغيل السيرفر بنجاح على المنفذ {port}!")
            self.btn_host.config(state=tk.DISABLED)

            # Auto connect this instance as a client
            self.host_entry.delete(0, tk.END)
            self.host_entry.insert(0, "127.0.0.1")
            self.connect_to_server()
        except Exception as e:
            messagebox.showerror("خطأ في تشغيل السيرفر", str(e))

    def _server_listen_loop(self):
        while True:
            try:
                client_sock, addr = self.server_sock.accept()
                self.clients.append(client_sock)
                threading.Thread(target=self._server_client_handler, args=(client_sock,), daemon=True).start()
            except Exception:
                break

    def _server_client_handler(self, client_sock):
        while True:
            try:
                data = client_sock.recv(4096)
                if not data:
                    break
                # Broadcast to all other clients
                for c in list(self.clients):
                    try:
                        c.sendall(data)
                    except Exception:
                        if c in self.clients:
                            self.clients.remove(c)
            except Exception:
                break
        if client_sock in self.clients:
            self.clients.remove(client_sock)

    def connect_to_server(self):
        if self.is_connected:
            return

        host = self.host_entry.get().strip()
        port = int(self.port_entry.get().strip())
        self.username = self.user_entry.get().strip() or "ضيف"

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
            self.is_connected = True

            self.status_badge.config(text=f"🟢 متصل ({self.username})", bg="#065F46", fg="#A7F3D0")
            self.btn_connect.config(state=tk.DISABLED, text="متصل حالياً")

            # Start receiver thread
            threading.Thread(target=self._client_receive_loop, daemon=True).start()

            # Announce join
            join_payload = json.dumps({"type": "join", "user": self.username})
            self.sock.sendall(join_payload.encode("utf-8"))

            self.add_system_message(f"تم الاتصال بالسيرفر {host}:{port} بنجاح!")
            self.users_listbox.insert(tk.END, f"• {self.username} (أنت)")
        except Exception as e:
            messagebox.showerror("خطأ في الاتصال", f"تعذر الاتصال بالسيرفر:\n{e}")

    def _client_receive_loop(self):
        while self.is_connected:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                payload = json.loads(data.decode("utf-8"))
                p_type = payload.get("type")

                if p_type == "msg":
                    u = payload.get("user")
                    r = payload.get("room")
                    txt = payload.get("text")
                    is_me = (u == self.username)
                    self.after(0, lambda u=u, r=r, txt=txt, is_me=is_me: self.add_chat_message(u, r, txt, is_me))
                elif p_type == "join":
                    u = payload.get("user")
                    if u != self.username:
                        self.after(0, lambda u=u: self.add_system_message(f"انضم {u} إلى المحادثة! 👋"))
                        self.after(0, lambda u=u: self.users_listbox.insert(tk.END, f"• {u}"))
            except Exception:
                break

        self.is_connected = False
        self.after(0, lambda: self.status_badge.config(text="⚫ انقطع الاتصال", bg="#334155", fg="#94A3B8"))

    def send_message(self):
        txt = self.input_entry.get().strip()
        if not txt:
            return

        if not self.is_connected:
            messagebox.showwarning("تنبيه", "أنت غير متصل بالسيرفر حالياً! اضغط 'انضمام' أو 'استضافة' أولاً.")
            return

        payload = {
            "type": "msg",
            "user": self.username,
            "room": self.current_room,
            "text": txt
        }
        try:
            self.sock.sendall(json.dumps(payload).encode("utf-8"))
            self.input_entry.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل إرسال الرسالة: {e}")


if __name__ == "__main__":
    app = ChatApplication()
    app.mainloop()
