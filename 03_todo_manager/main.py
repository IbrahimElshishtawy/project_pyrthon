#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 3: مدير المهام الاحترافي (To-Do List Task Manager)
يدعم:
- إضافة وحذف وتعديل وتحديد حالة المهام (مكتملة / قيد التنفيذ)
- تصنيف المهام حسب الأولوية (🔴 عالية، 🟡 متوسطة، 🟢 منخفضة) والقسم (عمل، دراسة، شخصي)
- حفظ واسترجاع تلقائي في ملف JSON
- شريط بحث وفلاتر سريعة (الكل، المتبقية، المكتملة)
- لوحة إحصائيات سريعة بنسبة الإنجاز
"""

import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk


class TodoManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("مدير المهام الاحترافي | Task Manager")
        self.geometry("820x650")
        self.minsize(750, 580)
        self.configure(bg="#0F172A")

        self.data_file = os.path.join(os.path.dirname(__file__), "tasks.json")
        self.tasks = []
        self.current_filter = "all"  # all, pending, completed

        self.setup_ui()
        self.load_tasks()
        self.refresh_task_list()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="📋 مدير المهام اليومية الذكي",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        self.stats_label = tk.Label(
            header,
            text="الإنجاز: 0/0 (0%)",
            font=("Segoe UI", 11, "bold"),
            bg="#334155",
            fg="#F8FAFC",
            padx=12,
            pady=4
        )
        self.stats_label.pack(side=tk.LEFT)

        # Main Body
        body = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # New Task Creation Panel
        create_panel = tk.Frame(body, bg="#1E293B", padx=14, pady=12, bd=1, relief=tk.SOLID)
        create_panel.pack(fill=tk.X, pady=(0, 12))

        # Title entry
        entry_row = tk.Frame(create_panel, bg="#1E293B")
        entry_row.pack(fill=tk.X, pady=(0, 8))

        lbl_task = tk.Label(entry_row, text="المهمة الجديدة:", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC")
        lbl_task.pack(side=tk.RIGHT, padx=(6, 0))

        self.task_entry = tk.Entry(
            entry_row,
            font=("Segoe UI", 11),
            bg="#0F172A",
            fg="#FFFFFF",
            insertbackground="#38BDF8",
            relief=tk.FLAT,
            bd=2
        )
        self.task_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=4, padx=6)
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Options row (Priority & Category & Add Button)
        opts_row = tk.Frame(create_panel, bg="#1E293B")
        opts_row.pack(fill=tk.X)

        add_btn = tk.Button(
            opts_row,
            text="➕ إضافة مهمة",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            activebackground="#0369A1",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=3,
            command=self.add_task
        )
        add_btn.pack(side=tk.LEFT)

        # Category
        self.cat_var = tk.StringVar(value="شخصي")
        cat_cb = ttk.Combobox(opts_row, textvariable=self.cat_var, values=["عمل", "دراسة", "شخصي", "عاجل", "أخرى"], state="readonly", width=10)
        cat_cb.pack(side=tk.RIGHT, padx=(6, 0))
        tk.Label(opts_row, text="التصنيف:", font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT, padx=(10, 2))

        # Priority
        self.prio_var = tk.StringVar(value="متوسطة")
        prio_cb = ttk.Combobox(opts_row, textvariable=self.prio_var, values=["عالية", "متوسطة", "منخفضة"], state="readonly", width=10)
        prio_cb.pack(side=tk.RIGHT, padx=(6, 0))
        tk.Label(opts_row, text="الأولوية:", font=("Segoe UI", 10), bg="#1E293B", fg="#94A3B8").pack(side=tk.RIGHT, padx=(10, 2))

        # Toolbar: Search & Filter buttons
        tools_frame = tk.Frame(body, bg="#0F172A")
        tools_frame.pack(fill=tk.X, pady=(0, 8))

        # Filters
        self.btn_filter_all = tk.Button(tools_frame, text="جميع المهام", bg="#334155", fg="#FFFFFF", relief=tk.FLAT, font=("Segoe UI", 9), command=lambda: self.set_filter("all"))
        self.btn_filter_all.pack(side=tk.RIGHT, padx=2)

        self.btn_filter_pend = tk.Button(tools_frame, text="⏳ قيد التنفيذ", bg="#1E293B", fg="#94A3B8", relief=tk.FLAT, font=("Segoe UI", 9), command=lambda: self.set_filter("pending"))
        self.btn_filter_pend.pack(side=tk.RIGHT, padx=2)

        self.btn_filter_done = tk.Button(tools_frame, text="✅ المكتملة", bg="#1E293B", fg="#94A3B8", relief=tk.FLAT, font=("Segoe UI", 9), command=lambda: self.set_filter("completed"))
        self.btn_filter_done.pack(side=tk.RIGHT, padx=2)

        # Search Bar
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_task_list())
        search_entry = tk.Entry(tools_frame, textvariable=self.search_var, font=("Segoe UI", 10), bg="#1E293B", fg="#FFFFFF", insertbackground="#38BDF8", relief=tk.FLAT)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 10))
        tk.Label(tools_frame, text="🔍 بحث:", font=("Segoe UI", 9), bg="#0F172A", fg="#94A3B8").pack(side=tk.LEFT, padx=(0, 4))

        # Task Listbox / Treeview
        list_container = tk.Frame(body, bg="#1E293B", bd=1, relief=tk.SOLID)
        list_container.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "status", "title", "category", "priority", "date")
        self.tree = ttk.Treeview(list_container, columns=cols, show="headings", selectmode="browse")
        
        self.tree.heading("id", text="#")
        self.tree.heading("status", text="الحالة")
        self.tree.heading("title", text="عنوان المهمة")
        self.tree.heading("category", text="التصنيف")
        self.tree.heading("priority", text="الأولوية")
        self.tree.heading("date", text="تاريخ الإضافة")

        self.tree.column("id", width=35, anchor="center")
        self.tree.column("status", width=80, anchor="center")
        self.tree.column("title", width=340, anchor="w")
        self.tree.column("category", width=90, anchor="center")
        self.tree.column("priority", width=90, anchor="center")
        self.tree.column("date", width=110, anchor="center")

        scroll = ttk.Scrollbar(list_container, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-Button-1>", lambda e: self.toggle_complete())

        # Action Buttons Bottom
        actions_bar = tk.Frame(body, bg="#0F172A", pady=8)
        actions_bar.pack(fill=tk.X)

        tk.Button(
            actions_bar,
            text="✔ تغيير الحالة (مكتمل / غير مكتمل)",
            font=("Segoe UI", 10),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.toggle_complete
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            actions_bar,
            text="✏ تعديل",
            font=("Segoe UI", 10),
            bg="#6366F1",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.edit_task
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            actions_bar,
            text="🗑 حذف",
            font=("Segoe UI", 10),
            bg="#EF4444",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.delete_task
        ).pack(side=tk.RIGHT, padx=4)

        tk.Button(
            actions_bar,
            text="🧹 مسح المكتملة",
            font=("Segoe UI", 10),
            bg="#475569",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.clear_completed
        ).pack(side=tk.LEFT, padx=4)

    def load_tasks(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    self.tasks = json.load(f)
            except Exception:
                self.tasks = []
        else:
            # Default Starter Tasks
            self.tasks = [
                {"id": 1, "title": "مراجعة مشروع البايثون", "category": "عمل", "priority": "عالية", "completed": False, "date": "2026-10-05"},
                {"id": 2, "title": "قراءة كتاب الذكاء الاصطناعي", "category": "دراسة", "priority": "متوسطة", "completed": True, "date": "2026-10-04"},
                {"id": 3, "title": "الذهاب للنادي الرياضي", "category": "شخصي", "priority": "منخفضة", "completed": False, "date": "2026-10-05"}
            ]
            self.save_tasks()

    def save_tasks(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("خطأ في الحفظ", str(e))

    def set_filter(self, filter_type):
        self.current_filter = filter_type
        # Update button visual states
        self.btn_filter_all.config(bg="#334155" if filter_type == "all" else "#1E293B", fg="#FFFFFF" if filter_type == "all" else "#94A3B8")
        self.btn_filter_pend.config(bg="#334155" if filter_type == "pending" else "#1E293B", fg="#FFFFFF" if filter_type == "pending" else "#94A3B8")
        self.btn_filter_done.config(bg="#334155" if filter_type == "completed" else "#1E293B", fg="#FFFFFF" if filter_type == "completed" else "#94A3B8")
        self.refresh_task_list()

    def refresh_task_list(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()

        total = len(self.tasks)
        completed_count = sum(1 for t in self.tasks if t.get("completed", False))

        # Update stats
        pct = int((completed_count / total) * 100) if total > 0 else 0
        self.stats_label.config(text=f"الإنجاز: {completed_count}/{total} ({pct}%)")

        for task in self.tasks:
            # Filter check
            if self.current_filter == "pending" and task.get("completed", False):
                continue
            if self.current_filter == "completed" and not task.get("completed", False):
                continue

            # Search check
            if query and query not in task.get("title", "").lower() and query not in task.get("category", "").lower():
                continue

            status_icon = "✅ منجزة" if task.get("completed", False) else "⏳ جارية"
            prio_badge = f"🔴 {task['priority']}" if task['priority'] == "عالية" else (f"🟡 {task['priority']}" if task['priority'] == "متوسطة" else f"🟢 {task['priority']}")

            self.tree.insert(
                "",
                tk.END,
                values=(
                    task["id"],
                    status_icon,
                    task["title"],
                    task["category"],
                    prio_badge,
                    task.get("date", "")
                )
            )

    def add_task(self):
        title = self.task_entry.get().strip()
        if not title:
            messagebox.showwarning("تنبيه", "يرجى كتابة عنوان للمهمة!")
            return

        new_id = (max([t["id"] for t in self.tasks]) + 1) if self.tasks else 1
        new_task = {
            "id": new_id,
            "title": title,
            "category": self.cat_var.get(),
            "priority": self.prio_var.get(),
            "completed": False,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.tasks.append(new_task)
        self.save_tasks()
        self.task_entry.delete(0, tk.END)
        self.refresh_task_list()

    def get_selected_task(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item_vals = self.tree.item(sel[0], "values")
        task_id = int(item_vals[0])
        for t in self.tasks:
            if t["id"] == task_id:
                return t
        return None

    def toggle_complete(self):
        task = self.get_selected_task()
        if not task:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة أولاً!")
            return
        task["completed"] = not task["completed"]
        self.save_tasks()
        self.refresh_task_list()

    def edit_task(self):
        task = self.get_selected_task()
        if not task:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة لتعديلها!")
            return
        new_title = simpledialog.askstring("تعديل المهمة", "اكتب العنوان الجديد:", initialvalue=task["title"])
        if new_title and new_title.strip():
            task["title"] = new_title.strip()
            self.save_tasks()
            self.refresh_task_list()

    def delete_task(self):
        task = self.get_selected_task()
        if not task:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة لحذفها!")
            return
        if messagebox.askyesno("تأكيد الحذف", f"هل تريد بالتأكيد حذف مهمة:\n\"{task['title']}\"؟"):
            self.tasks.remove(task)
            self.save_tasks()
            self.refresh_task_list()

    def clear_completed(self):
        completed = [t for t in self.tasks if t.get("completed", False)]
        if not completed:
            messagebox.showinfo("معلومة", "لا توجد أي مهام مكتملة للمسح!")
            return
        if messagebox.askyesno("تأكيد", f"سيتم مسح {len(completed)} مهمة مكتملة، هل أنت متأكد؟"):
            self.tasks = [t for t in self.tasks if not t.get("completed", False)]
            self.save_tasks()
            self.refresh_task_list()


if __name__ == "__main__":
    app = TodoManagerApp()
    app.mainloop()
