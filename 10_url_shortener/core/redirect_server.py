# -*- coding: utf-8 -*-
"""
خادم تحويل محلي مدمج للروابط المختصرة
"""

import http.server
import socketserver
import threading


class RedirectServer:
    def __init__(self, db, port=8000, on_click_callback=None):
        self.db = db
        self.port = port
        self.on_click = on_click_callback or (lambda: None)
        self.httpd = None

    def start(self):
        db_ref = self.db
        cb_ref = self.on_click

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                code = self.path.lstrip("/").split("?")[0]
                if not code:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<h2>مرحباً بك في سيرفر اختصار الروابط المحلي!</h2>".encode("utf-8"))
                    return

                orig = db_ref.get_url(code)
                if orig:
                    cb_ref()
                    self.send_response(302)
                    self.send_header("Location", orig)
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("<h3>عذراً، هذا الرابط غير موجود.</h3>".encode("utf-8"))

            def log_message(self, format, *args):
                pass

        def run():
            try:
                socketserver.TCPServer.allow_reuse_address = True
                with socketserver.TCPServer(("", self.port), Handler) as server:
                    self.httpd = server
                    server.serve_forever()
            except Exception:
                pass

        threading.Thread(target=run, daemon=True).start()
