# -*- coding: utf-8 -*-
"""
محرك تحليل ومعالجة بيانات المبيعات والأداء التنفيذي
"""

import csv
import random


class AnalyticsService:
    MONTHS = ["يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو", "يوليو", "أغسطس", "سبتمبر"]
    REGIONS = ["الشرق الأوسط", "أوروبا", "أمريكا الشمالية", "آسيا"]
    CATEGORIES = ["إلكترونيات", "أزياء وملابس", "أثاث ومكتب", "برمجيات وخدمات"]

    def __init__(self):
        self.raw_data = self.generate_sample_dataset()
        self.filtered_data = list(self.raw_data)

    def generate_sample_dataset(self):
        data = []
        random.seed(42)
        base_id = 1001

        for i in range(120):
            m = random.choice(self.MONTHS)
            r = random.choice(self.REGIONS)
            c = random.choice(self.CATEGORIES)
            units = random.randint(1, 15)
            unit_price = random.choice([50, 120, 250, 480, 850, 1400])
            total = units * unit_price

            data.append({
                "id": f"ORD-{base_id + i}",
                "month": m,
                "region": r,
                "category": c,
                "units": units,
                "unit_price": unit_price,
                "revenue": total
            })
        return data

    def filter_data(self, category="جميع الفئات", region="جميع المناطق"):
        self.filtered_data = [
            d for d in self.raw_data
            if (category == "جميع الفئات" or d["category"] == category)
            and (region == "جميع المناطق" or d["region"] == region)
        ]
        return self.filtered_data

    def get_kpis(self):
        total_rev = sum(d["revenue"] for d in self.filtered_data)
        orders_count = len(self.filtered_data)
        aov = (total_rev / orders_count) if orders_count > 0 else 0
        total_units = sum(d["units"] for d in self.filtered_data)

        return {
            "total_revenue": total_rev,
            "orders_count": orders_count,
            "aov": aov,
            "total_units": total_units
        }

    def get_monthly_totals(self):
        totals = {m: 0 for m in self.MONTHS}
        for d in self.filtered_data:
            m = d["month"]
            if m in totals:
                totals[m] += d["revenue"]
        return totals

    def get_category_totals(self):
        cat_totals = {}
        for d in self.filtered_data:
            c = d["category"]
            cat_totals[c] = cat_totals.get(c, 0) + d["revenue"]
        return cat_totals

    def import_csv(self, file_path):
        loaded = []
        with open(file_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for idx, row in enumerate(reader):
                rev = float(row.get("revenue", row.get("المبلغ", row.get("amount", random.randint(100, 1000)))))
                loaded.append({
                    "id": row.get("id", f"CSV-{idx+1}"),
                    "month": row.get("month", "يناير"),
                    "region": row.get("region", "الشرق الأوسط"),
                    "category": row.get("category", "منتجات عامة"),
                    "units": int(row.get("units", 1)),
                    "unit_price": float(row.get("price", rev)),
                    "revenue": rev
                })
        if loaded:
            self.raw_data = loaded
            self.filtered_data = list(loaded)
            return len(loaded)
        return 0

    def export_csv(self, dest_path):
        with open(dest_path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["كود الطلب", "الشهر", "المنطقة", "الفئة", "الكمية", "سعر الوحدة", "الإجمالي"])
            for d in self.filtered_data:
                w.writerow([d["id"], d["month"], d["region"], d["category"], d["units"], d["unit_price"], d["revenue"]])
