#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 10: تطبيق اختصار الروابط الذكي مع خادم وقاعدة بيانات SQLite
يدعم:
- تخزين الروابط في قاعدة بيانات SQLite محلية (urls.db)
- إنشاء كود اختصار عشوائي أو تخصيص اسم مختصر مخصص (Custom Alias)
- خادم ويب محلي مدمج (Embedded HTTP Server على البورت 8000) للتحويل التلقائي
- تتبع عدد الزيارات والنقرات (Click Counter) لكل رابط وتحديثه لحظياً
- معاينة مرئية ونسخ سريع للرابط المختصر
- البحث، الحذف، وفتح الروابط في المتصفح بنقرة زر واحدة
"""

import http.server
import os
import random
import socketserver
import sqlite3
import string
import threading
import tkinter as tk
import webbrowser
from datetime import datetime
from tkinter import messagebox, ttk


class URLShortenerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مختصر الروابط الاحترافي | URL Shortener & Analytics")
        self.geometry("920x680")
        self.minsize(840, 600)
        self.configure(bg="#0F172A")

        self.db_path = os.path.join(os.path.dirname(__file__), "urls.db")
        self.port = 8000
        self.server_running = True

        self.init_database()
        self.start_embedded_server()

        self.setup_ui()
        self.refresh_table()

    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS urls (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_code TEXT UNIQUE NOT NULL,
                    clicks INTEGER DEFAULT 0,
                    created_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def start_embedded_server(self):
        app_ref = self

        class RedirectHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                code = self.path.lstrip("/").split("?")[0]
                if not code:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<h2>مرحباً بك في خادم اختصار الروابط المحلي!</h2>".encode("utf-8"))
                    return

                # Lookup in sqlite
                try:
                    with sqlite3.connect(app_ref.db_path) as conn:
                        cursor = conn.cursor()
                        cursor.execute("SELECT id, original_url, clicks FROM urls WHERE short_code = ?", (code,))
                        row = cursor.fetchone()
                        if row:
                            u_id, orig_url, clicks = row
                            cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE id = ?", (u_id,))
                            conn.commit()
                            app_ref.after(0, app_ref.refresh_table)

                            # 302 Redirect
                            self.send_response(302)
                            self.send_header("Location", orig_url)
                            self.end_headers()
                            return
                except Exception:
                    pass

                self.send_response(404)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write("<h3>عذراً، هذا الرابط المختصر غير موجود أو انتهت صلاحيته.</h3>".encode("utf-8"))

            def log_message(self, format, *args):
                pass  # Suppress console clutter

        def run_server():
            try:
                # Allow port reuse
                socketserver.TCPServer.allow_reuse_address = True
                with socketserver.TCPServer(("", self.port), RedirectHandler) as httpd:
                    httpd.serve_forever()
            except Exception:
                pass

        threading.Thread(target=run_server, daemon=True).start()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🔗 مختصر الروابط الذكي مع قاعدة بيانات SQLite",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        server_badge = tk.Label(
            header,
            text=f"🟢 سيرفر التحويل يعمل على: http://localhost:{self.port}",
            font=("Segoe UI", 9, "bold"),
            bg="#065F46",
            fg="#A7F3D0",
            padx=10,
            pady=4
        )
        server_badge.pack(side=tk.LEFT)

        # Body Container
        body = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Shorten Form Card
        form_card = tk.Frame(body, bg="#1E293B", padx=16, pady=12, bd=1, relief=tk.SOLID)
        form_card.pack(fill=tk.X, pady=(0, 12))

        tk.Label(form_card, text="✂️ اختصار رابط جديد:", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC").pack(anchor="e", pady=(0, 8))

        row1 = tk.Frame(form_card, bg="#1E293B")
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="الرابط الأصلي (Long URL):", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)
        self.long_url_entry = tk.Entry(row1, font=("Segoe UI", 10), bg="#0F172A", fg="#FFFFFF", insertbackground="#38BDF8", relief=tk.FLAT)
        self.long_url_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=6)
        self.long_url_entry.insert(0, "https://github.com")

        row2 = tk.Frame(form_card, bg="#1E293B")
        row2.pack(fill=tk.X, pady=4)

        btn_shorten = tk.Button(
            row2,
            text="⚡ إنشاء الرابط المختصر",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            command=self.create_short_url
        )
        btn_shorten.pack(side=tk.LEFT)

        tk.Label(row2, text="(اتركه فارغاً للتوليد التلقائي)", font=("Segoe UI", 8), bg="#1E293B", fg="#64748B").pack(side=tk.RIGHT, padx=4)

        self.alias_entry = tk.Entry(row2, font=("Segoe UI", 10), bg="#0F172A", fg="#38BDF8", insertbackground="#38BDF8", relief=tk.FLAT, width=16)
        self.alias_entry.pack(side=tk.RIGHT, padx=4)

        tk.Label(row2, text="اسم مخصص اختياري (Custom Alias):", font=("Segoe UI", 9), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT)

        # Quick Output display
        self.result_banner = tk.Frame(form_card, bg="#0F172A", padx=10, pady=6)
        self.result_banner.pack(fill=tk.X, pady=(6, 0))

        self.lbl_result = tk.Label(
            self.result_banner,
            text="الرابط المختصر سيظهر هنا بعد التوليد",
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#94A3B8"
        )
        self.lbl_result.pack(side=tk.RIGHT)

        self.btn_copy_fast = tk.Button(
            self.result_banner,
            text="📋 نسخ",
            font=("Segoe UI", 8, "bold"),
            bg="#334155",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED,
            command=self.copy_current_result
        )
        self.btn_copy_fast.pack(side=tk.LEFT)

        # Table & Actions
        table_card = tk.Frame(body, bg="#1E293B", bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        cols = ("id", "short_code", "full_short_url", "clicks", "created_at", "original_url")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="#")
        self.tree.heading("short_code", text="الكود")
        self.tree.heading("full_short_url", text="الرابط المختصر")
        self.tree.heading("clicks", text="النقرات")
        self.tree.heading("created_at", text="تاريخ الإنشاء")
        self.tree.heading("original_url", text="الرابط الأصلي المستهدف")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("short_code", width=80, anchor="center")
        self.tree.column("full_short_url", width=220, anchor="w")
        self.tree.column("clicks", width=65, anchor="center")
        self.tree.column("created_at", width=120, anchor="center")
        self.tree.column("original_url", width=340, anchor="w")

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-Button-1>", lambda e: self.open_in_browser())

        # Action Toolbar
        action_bar = tk.Frame(body, bg="#0F172A")
        action_bar.pack(fill=tk.X)

        tk.Button(
            action_bar,
            text="🌐 فتح الرابط في المتصفح",
            font=("Segoe UI", 9, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.open_in_browser
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            action_bar,
            text="📋 نسخ الرابط المحدد",
            font=("Segoe UI", 9),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.copy_selected_url
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            action_bar,
            text="🗑 حذف من قاعدة البيانات",
            font=("Segoe UI", 9),
            bg="#EF4444",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.delete_url
        ).pack(side=tk.LEFT, padx=4)

        tk.Button(
            action_bar,
            text="🔄 تحديث الجدول",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.refresh_table
        ).pack(side=tk.LEFT, padx=4)

    def generate_random_code(self, length=6):
        chars = string.ascii_letters + string.digits
        return "".join(random.choice(chars) for _ in range(length))

    def create_short_url(self):
        orig_url = self.long_url_entry.get().strip()
        alias = self.alias_entry.get().strip()

        if not orig_url:
            messagebox.showwarning("تنبيه", "يرجى إدخال الرابط المراد اختصاره!")
            return

        if not orig_url.startswith("http://") and not orig_url.startswith("https://"):
            orig_url = "https://" + orig_url

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            code = alias if alias else self.generate_random_code()

            # Check if alias exists
            cursor.execute("SELECT id FROM urls WHERE short_code = ?", (code,))
            if cursor.fetchone():
                messagebox.showerror("كود مستخدم", f"الكود المختصر '{code}' مستخدم مسبقاً، يرجى اختيار كود آخر!")
                return

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            cursor.execute(
                "INSERT INTO urls (original_url, short_code, clicks, created_at) VALUES (?, ?, ?, ?)",
                (orig_url, code, 0, now_str)
            )
            conn.commit()

        short_url = f"http://localhost:{self.port}/{code}"
        self.lbl_result.config(text=short_url, fg="#4ADE80")
        self.btn_copy_fast.config(state=tk.NORMAL)
        self.alias_entry.delete(0, tk.END)
        self.refresh_table()
        messagebox.showinfo("تم بنجاح!", f"تم إنشاء الرابط المختصر:\n{short_url}")

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, short_code, clicks, created_at, original_url FROM urls ORDER BY id DESC")
            rows = cursor.fetchall()
            for r in rows:
                u_id, code, clicks, dt, orig = r
                short_full = f"http://localhost:{self.port}/{code}"
                self.tree.insert("", tk.END, values=(u_id, code, short_full, clicks, dt, orig))

    def copy_current_result(self):
        url = self.lbl_result.cget("text")
        if url and "http" in url:
            self.clipboard_clear()
            self.clipboard_append(url)
            messagebox.showinfo("تم النسخ", "تم نسخ الرابط المختصر إلى الحافظة بنجاح!")

    def copy_selected_url(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط من الجدول!")
            return
        vals = self.tree.item(sel[0], "values")
        short_url = vals[2]
        self.clipboard_clear()
        self.clipboard_append(short_url)
        messagebox.showinfo("تم النسخ", f"تم نسخ الرابط:\n{short_url}")

    def open_in_browser(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط لفتحه!")
            return
        vals = self.tree.item(sel[0], "values")
        short_url = vals[2]
        webbrowser.open(short_url)

    def delete_url(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo("ملاحظة", "يرجى تحديد رابط لحذفه!")
            return
        vals = self.tree.item(sel[0], "values")
        u_id = int(vals[0])

        if messagebox.askyesno("تأكيد الحذف", f"هل أنت متأكد من حذف الرابط المختصر #{u_id}؟"):
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM urls WHERE id = ?", (u_id,))
                conn.commit()
            self.refresh_table()


if __name__ == "__main__":
    app = URLShortenerApp()
    app.mainloop()
