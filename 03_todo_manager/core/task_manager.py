# -*- coding: utf-8 -*-
"""
محرك إدارة وحفظ المهام اليومية (Task Management Business Logic)
"""

import json
import os
from datetime import datetime


class TaskManager:
    def __init__(self, data_path=None):
        self.data_path = data_path or os.path.join(os.path.dirname(__file__), "..", "tasks.json")
        self.tasks = []
        self.load()

    def load(self):
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []
        else:
            self.tasks = [
                {"id": 1, "title": "مراجعة مشروع بايثون", "category": "عمل", "priority": "عالية", "completed": False, "date": datetime.now().strftime("%Y-%m-%d")},
                {"id": 2, "title": "قراءة مقال عن الذكاء الاصطناعي", "category": "دراسة", "priority": "متوسطة", "completed": True, "date": datetime.now().strftime("%Y-%m-%d")},
                {"id": 3, "title": "الذهاب للتمارين الرياضية", "category": "شخصي", "priority": "منخفضة", "completed": False, "date": datetime.now().strftime("%Y-%m-%d")}
            ]
            self.save()

    def save(self):
        try:
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            raise IOError(f"فشل حفظ البيانات: {e}")

    def add_task(self, title, category="شخصي", priority="متوسطة"):
        new_id = (max([t["id"] for t in self.tasks]) + 1) if self.tasks else 1
        task = {
            "id": new_id,
            "title": title.strip(),
            "category": category,
            "priority": priority,
            "completed": False,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.tasks.append(task)
        self.save()
        return task

    def toggle_completed(self, task_id):
        for t in self.tasks:
            if t["id"] == task_id:
                t["completed"] = not t["completed"]
                self.save()
                return t
        return None

    def update_task_title(self, task_id, new_title):
        for t in self.tasks:
            if t["id"] == task_id:
                t["title"] = new_title.strip()
                self.save()
                return t
        return None

    def delete_task(self, task_id):
        orig_len = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) != orig_len:
            self.save()
            return True
        return False

    def clear_completed(self):
        count = sum(1 for t in self.tasks if t.get("completed", False))
        self.tasks = [t for t in self.tasks if not t.get("completed", False)]
        self.save()
        return count

    def get_stats(self):
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.get("completed", False))
        pending = total - completed
        pct = int((completed / total) * 100) if total > 0 else 0
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "pct": pct
        }

    def filter_tasks(self, filter_type="all", search_query=""):
        query = search_query.strip().lower()
        results = []
        for t in self.tasks:
            if filter_type == "pending" and t.get("completed", False):
                continue
            if filter_type == "completed" and not t.get("completed", False):
                continue
            if query and query not in t.get("title", "").lower() and query not in t.get("category", "").lower():
                continue
            results.append(t)
        return results
