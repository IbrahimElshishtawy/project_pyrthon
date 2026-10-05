# -*- coding: utf-8 -*-
"""
محرك إدارة وتحليل المصروفات الشخصية (Data & Analytics Service)
"""

import csv
import json
import os
from datetime import datetime


class ExpenseManager:
    CATEGORIES = {
        "طعام": "#EF4444",
        "مواصلات": "#F59E0B",
        "فواتير": "#3B82F6",
        "ترفيه": "#EC4899",
        "صحة": "#10B981",
        "تسوق": "#8B5CF6",
        "أخرى": "#64748B"
    }

    def __init__(self, data_path=None):
        self.data_path = data_path or os.path.join(os.path.dirname(__file__), "..", "expenses.json")
        self.expenses = []
        self.load()

    def load(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
            except Exception:
                self.expenses = []
        else:
            self.expenses = [
                {"id": 1, "date": "2026-10-05 10:30", "category": "طعام", "amount": 150.0, "note": "وجبة غداء"},
                {"id": 2, "date": "2026-10-04 14:15", "category": "مواصلات", "amount": 60.0, "note": "تاكسي للجامعة"},
                {"id": 3, "date": "2026-10-03 19:00", "category": "فواتير", "amount": 420.0, "note": "فاتورة الإنترنت"},
                {"id": 4, "date": "2026-10-02 21:00", "category": "ترفيه", "amount": 200.0, "note": "تذكرة سينما"},
                {"id": 5, "date": "2026-10-01 11:00", "category": "تسوق", "amount": 350.0, "note": "مستلزمات مكتبية"}
            ]
            self.save()

    def save(self):
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"فشل حفظ المصروفات: {e}")

    def add_expense(self, amount, category, note="بدون ملاحظة"):
        new_id = (max([e["id"] for e in self.expenses]) + 1) if self.expenses else 1
        rec = {
            "id": new_id,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": category,
            "amount": float(amount),
            "note": note
        }
        self.expenses.insert(0, rec)
        self.save()
        return rec

    def delete_expense(self, exp_id):
        orig_len = len(self.expenses)
        self.expenses = [e for e in self.expenses if e["id"] != exp_id]
        if len(self.expenses) != orig_len:
            self.save()
            return True
        return False

    def get_summary(self):
        total = sum(e["amount"] for e in self.expenses)
        count = len(self.expenses)
        cat_totals = {}
        for e in self.expenses:
            c = e["category"]
            cat_totals[c] = cat_totals.get(c, 0.0) + e["amount"]

        top_cat = max(cat_totals, key=cat_totals.get) if cat_totals else "--"
        top_cat_amount = cat_totals.get(top_cat, 0.0)

        return {
            "total": total,
            "count": count,
            "cat_totals": cat_totals,
            "top_cat": top_cat,
            "top_cat_amount": top_cat_amount
        }

    def export_csv(self, dest_path):
        with open(dest_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["المعرف", "التاريخ والوقت", "التصنيف", "المبلغ", "الملاحظة"])
            for e in self.expenses:
                writer.writerow([e["id"], e["date"], e["category"], e["amount"], e["note"]])
