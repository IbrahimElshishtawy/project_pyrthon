# -*- coding: utf-8 -*-
"""
محرك إدارة الأعضاء وسجلات الحضور والانصراف
"""

import csv
import json
import os
import random
from datetime import datetime


class AttendanceService:
    def __init__(self, members_path=None, csv_path=None):
        self.members_path = members_path or os.path.join(os.path.dirname(__file__), "..", "members.json")
        self.csv_path = csv_path or os.path.join(os.path.dirname(__file__), "..", "attendance_log.csv")
        self.members = []
        self.attendance_records = []

        self.load_members()
        self.load_attendance_csv()

    def load_members(self):
        if os.path.exists(self.members_path):
            try:
                with open(self.members_path, "r", encoding="utf-8") as f:
                    self.members = json.load(f)
            except Exception:
                self.members = []
        else:
            self.members = [
                {"id": "EMP-101", "name": "إبراهيم الششتاوي", "dept": "تطوير البرمجيات", "color": "#38BDF8"},
                {"id": "EMP-102", "name": "أحمد محمود", "dept": "الذكاء الاصطناعي", "color": "#10B981"},
                {"id": "EMP-103", "name": "سارة خالد", "dept": "تصميم تجربة المستخدم", "color": "#EC4899"}
            ]
            self.save_members()

    def save_members(self):
        try:
            with open(self.members_path, "w", encoding="utf-8") as f:
                json.dump(self.members, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"فشل حفظ الأعضاء: {e}")

    def load_attendance_csv(self):
        self.attendance_records.clear()
        if os.path.exists(self.csv_path):
            try:
                with open(self.csv_path, "r", encoding="utf-8-sig") as f:
                    reader = csv.reader(f)
                    next(reader, None)
                    for row in reader:
                        if len(row) >= 5:
                            self.attendance_records.append({
                                "id": row[0],
                                "name": row[1],
                                "dept": row[2],
                                "time": row[3],
                                "type": row[4]
                            })
            except Exception:
                pass

    def record_attendance(self, member_id, att_type):
        m = next((x for x in self.members if x["id"] == member_id), None)
        if not m:
            raise ValueError("العضو غير موجود")

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rec = {
            "id": m["id"],
            "name": m["name"],
            "dept": m["dept"],
            "time": now_str,
            "type": att_type
        }
        self.attendance_records.insert(0, rec)

        file_exists = os.path.exists(self.csv_path)
        with open(self.csv_path, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["الرقم الوظيفي", "الاسم", "القسم", "التاريخ والوقت", "النوع"])
            writer.writerow([rec["id"], rec["name"], rec["dept"], rec["time"], rec["type"]])

        return rec

    def register_member(self, name, emp_id, dept):
        item = {"id": emp_id, "name": name, "dept": dept, "color": "#38BDF8"}
        self.members.append(item)
        self.save_members()
        return item

    def get_stats(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        today_ids = {r["id"] for r in self.attendance_records if r["time"].startswith(today_str)}
        return {
            "total_members": len(self.members),
            "today_present": len(today_ids)
        }
