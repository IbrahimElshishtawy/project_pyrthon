# -*- coding: utf-8 -*-
"""
محرك إدارة وبوت تيليجرام (Bot Core Service)
"""

import json
import random
import threading
import time
import urllib.parse
import urllib.request


class TelegramBotService:
    QUOTES = [
        "الكود النظيف يُقرأ كأنه شعر نثري مكتوب بعناية. - Robert C. Martin",
        "أولاً حل المشكلة، ثم اكتب الكود. - John Johnson",
        "البساطة هي روح الكفاءة البرمجية. - Austin Freeman",
        "أفضل طريقة للتنبؤ بالمستقبل هي برمجته!"
    ]

    def __init__(self, on_event_callback=None):
        self.on_event = on_event_callback or (lambda src, msg: None)
        self.token = ""
        self.is_running = False
        self.is_sim_mode = True
        self.known_chats = set()

    def process_command(self, text, user_name="المستخدم"):
        text = text.strip()
        parts = text.split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        arg = parts[1] if len(parts) > 1 else ""

        if cmd == "/start":
            return (
                f"أهلاً وسهلاً بك يا {user_name}! 👋\n"
                "أنا بوت تيليجرام الذكي المبني بلغة بايثون.\n\n"
                "الأوامر المتاحة:\n"
                "• /weather <المدينة> : طقس اليوم\n"
                "• /remind <ثواني> <نص> : تذكير مؤقت\n"
                "• /quote : حكمة برمجية\n"
                "• /help : قائمة المساعدة"
            )
        elif cmd == "/help":
            return (
                "📖 دليل استخدام البوت:\n"
                "• /start - بدء المحادثة والقائمة\n"
                "• /weather Cairo - معرفة طقس القاهرة\n"
                "• /remind 10 استراحة - تذكير بعد 10 ثوانٍ\n"
                "• /quote - حكمة تقنية ملهمة"
            )
        elif cmd == "/quote":
            return f"💡 حكمة اليوم:\n{random.choice(self.QUOTES)}"
        elif cmd == "/weather":
            city = arg if arg else "القاهرة"
            temps = [24, 27, 29, 22, 26, 31]
            conds = ["مشمس ☀️", "غائم جزئياً ⛅", "صافٍ 🌤️", "معتدل ولطيف 🍃"]
            return f"🌤️ طقس {city}:\n• الحالة: {random.choice(conds)}\n• الحرارة: {random.choice(temps)}°C\n• الرطوبة: {random.randint(35, 65)}%\n• الرياح: {random.randint(10, 25)} كم/س"
        elif cmd == "/remind":
            subparts = arg.split(maxsplit=1)
            if not subparts or not subparts[0].isdigit():
                return "⚠️ الصيغة الصحيحة: /remind <عدد الثواني> <نص التذكير>"
            secs = int(subparts[0])
            note = subparts[1] if len(subparts) > 1 else "تذكير!"

            def trigger():
                time.sleep(secs)
                self.on_event("⏰ منبه البوت", f"حان وقت: {note} (بعد {secs} ثانية)!")

            threading.Thread(target=trigger, daemon=True).start()
            return f"⏳ تم ضبط التذكير بنجاح! سأنبهك بعد {secs} ثانية بـ: \"{note}\""
        else:
            return f"عذراً، لم أفهم الأمر '{text}'. اكتب /help لمعرفة الأوامر."

    def start_real_bot(self, token):
        self.token = token
        self.is_running = True
        self.is_sim_mode = False
        threading.Thread(target=self._real_polling_loop, daemon=True).start()

    def stop_bot(self):
        self.is_running = False

    def _real_polling_loop(self):
        offset = 0
        while self.is_running:
            try:
                url = f"https://api.telegram.org/bot{self.token}/getUpdates?offset={offset}&timeout=5"
                req = urllib.request.Request(url, headers={"User-Agent": "TelegramBotPy/1.0"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                    if data.get("ok"):
                        for update in data.get("result", []):
                            offset = update["update_id"] + 1
                            if "message" in update and "text" in update["message"]:
                                chat_id = update["message"]["chat"]["id"]
                                user_name = update["message"]["from"].get("first_name", "User")
                                text = update["message"]["text"]
                                self.known_chats.add(chat_id)

                                self.on_event(f"📩 {user_name} ({chat_id})", text)
                                reply = self.process_command(text, user_name)

                                send_url = f"https://api.telegram.org/bot{self.token}/sendMessage"
                                post_data = urllib.parse.urlencode({"chat_id": chat_id, "text": reply}).encode("utf-8")
                                urllib.request.urlopen(send_url, data=post_data, timeout=5)
                                self.on_event("🤖 رد البوت", reply)
            except Exception:
                time.sleep(3)
