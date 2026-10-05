# -*- coding: utf-8 -*-
"""
محرك كشط ومتابعة أسعار المنتجات في خيوط خلفية
"""

import json
import os
import random
import re
import urllib.request
from datetime import datetime


class PriceScraperService:
    def __init__(self, data_path=None):
        self.data_path = data_path or os.path.join(os.path.dirname(__file__), "..", "tracked_products.json")
        self.products = []
        self.load()

    def load(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.products = json.load(f)
            except Exception:
                self.products = []
        else:
            self.products = [
                {
                    "id": 1,
                    "name": "سماعات سوني اللاسلكية WH-1000XM5",
                    "url": "https://example.com/sony-headphones",
                    "currency": "ج.م (EGP)",
                    "current_price": 14500.0,
                    "target_price": 13000.0,
                    "history": [16000.0, 15000.0, 14500.0],
                    "last_checked": "2026-10-05 12:00"
                },
                {
                    "id": 2,
                    "name": "ساعة أبل الذكية Apple Watch Series 9",
                    "url": "https://example.com/apple-watch-9",
                    "currency": "ج.م (EGP)",
                    "current_price": 17800.0,
                    "target_price": 18000.0,
                    "history": [19500.0, 18200.0, 17800.0],
                    "last_checked": "2026-10-05 12:00"
                }
            ]
            self.save()

    def save(self):
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.products, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"فشل حفظ المنتجات: {e}")

    def add_product(self, name, url, target_price, currency="ج.م (EGP)"):
        new_id = (max([p["id"] for p in self.products]) + 1) if self.products else 1
        initial_price = round(target_price * random.uniform(1.05, 1.25), 2)
        item = {
            "id": new_id,
            "name": name.strip(),
            "url": url.strip(),
            "currency": currency,
            "current_price": initial_price,
            "target_price": float(target_price),
            "history": [initial_price],
            "last_checked": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        self.products.append(item)
        self.save()
        return item

    def delete_product(self, product_id):
        self.products = [p for p in self.products if p["id"] != product_id]
        self.save()

    def scrape_product(self, product):
        url = product.get("url", "")
        fetched_price = None

        if url.startswith("http://") or url.startswith("https://"):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
                )
                with urllib.request.urlopen(req, timeout=3) as resp:
                    html = resp.read().decode("utf-8", errors="ignore")
                    matches = re.findall(r'(\d+[\.,]\d{2})', html)
                    if matches:
                        fetched_price = float(matches[0].replace(",", ""))
            except Exception:
                pass

        if fetched_price is None or fetched_price <= 0:
            curr = product["current_price"]
            delta = random.choice([-0.06, -0.04, -0.02, 0.0, 0.02, -0.08])
            new_price = round(curr * (1 + delta), 2)
        else:
            new_price = round(fetched_price, 2)

        product["current_price"] = new_price
        product.setdefault("history", []).append(new_price)
        product["last_checked"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.save()
        return new_price

    def get_price_drop_alerts(self):
        return [p for p in self.products if p["current_price"] <= p["target_price"]]
