# -*- coding: utf-8 -*-
"""
محرك وبروتوكول شبكة الدردشة الفورية (TCP Sockets & Threading)
"""

import json
import socket
import threading


class ChatNetwork:
    def __init__(self, on_msg_callback=None, on_status_callback=None):
        self.on_msg = on_msg_callback or (lambda payload: None)
        self.on_status = on_status_callback or (lambda text: None)

        self.client_sock = None
        self.server_sock = None
        self.is_connected = False
        self.is_hosting = False
        self.clients = []

    def start_host(self, port=65432):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_sock.bind(("0.0.0.0", port))
        self.server_sock.listen(10)
        self.is_hosting = True

        threading.Thread(target=self._server_listen_loop, daemon=True).start()
        self.on_status(f"✅ تم تشغيل السيرفر بنجاح على المنفذ {port}!")

    def _server_listen_loop(self):
        while self.is_hosting:
            try:
                c_sock, _ = self.server_sock.accept()
                self.clients.append(c_sock)
                threading.Thread(target=self._client_relay_loop, args=(c_sock,), daemon=True).start()
            except Exception:
                break

    def _client_relay_loop(self, sock):
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                for c in list(self.clients):
                    try:
                        c.sendall(data)
                    except Exception:
                        if c in self.clients:
                            self.clients.remove(c)
            except Exception:
                break
        if sock in self.clients:
            self.clients.remove(sock)

    def connect(self, host, port, username):
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock.connect((host, port))
        self.is_connected = True

        threading.Thread(target=self._client_receive_loop, daemon=True).start()

        join_payload = json.dumps({"type": "join", "user": username})
        self.client_sock.sendall(join_payload.encode("utf-8"))
        self.on_status(f"تم الاتصال بالسيرفر {host}:{port} بنجاح!")

    def _client_receive_loop(self):
        while self.is_connected:
            try:
                data = self.client_sock.recv(4096)
                if not data:
                    break
                payload = json.loads(data.decode("utf-8"))
                self.on_msg(payload)
            except Exception:
                break
        self.is_connected = False
        self.on_status("انقطع الاتصال بالسيرفر.")

    def send_chat(self, username, room, text):
        if not self.is_connected or not self.client_sock:
            raise ConnectionError("غير متصل بالسيرفر")

        payload = {
            "type": "msg",
            "user": username,
            "room": room,
            "text": text
        }
        self.client_sock.sendall(json.dumps(payload).encode("utf-8"))
