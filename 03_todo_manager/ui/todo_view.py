# -*- coding: utf-8 -*-
"""
واجهة المستخدم الرسومية لمدير المهام
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from ui.theme import THEME


class TodoView(tk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent, bg=THEME["bg"])
        self.manager = manager
        self.current_filter = "all"

        self.setup_ui()
        self.refresh()

    def setup_ui(self):
        # Header Bar
        header = tk.Frame(self, bg=THEME["surface"], pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="📋 مدير المهام اليومية الذكي",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        self.stats_lbl = tk.Label(
            header,
            text="الإنجاز: 0/0 (0%)",
            font=(THEME["font_family"], 11, "bold"),
            bg="#334155",
            fg=THEME["text_main"],
            padx=12,
            pady=4
        )
        self.stats_lbl.pack(side=tk.LEFT)

        # Body Container
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # New Task Creation Panel
        create_panel = tk.Frame(body, bg=THEME["surface"], padx=14, pady=12, bd=1, relief=tk.SOLID)
        create_panel.pack(fill=tk.X, pady=(0, 12))

        # Title entry row
        e_row = tk.Frame(create_panel, bg=THEME["surface"])
        e_row.pack(fill=tk.X, pady=(0, 8))

        tk.Label(e_row, text="المهمة الجديدة:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(side=tk.RIGHT, padx=(6, 0))

        self.entry_task = tk.Entry(
            e_row,
            font=(THEME["font_family"], 11),
            bg=THEME["bg"],
            fg="#FFFFFF",
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT,
            bd=2
        )
        self.entry_task.pack(side=tk.RIGHT, fill=tk.X, expand=True, ipady=4, padx=6)
        self.entry_task.bind("<Return>", lambda e: self.on_add())

        # Options Row
        opt_row = tk.Frame(create_panel, bg=THEME["surface"])
        opt_row.pack(fill=tk.X)

        btn_add = tk.Button(
            opt_row,
            text="➕ إضافة مهمة",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            activebackground="#0369A1",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=3,
            command=self.on_add
        )
        btn_add.pack(side=tk.LEFT)

        self.cat_var = tk.StringVar(value="شخصي")
        cat_cb = ttk.Combobox(opt_row, textvariable=self.cat_var, values=["عمل", "دراسة", "شخصي", "عاجل", "أخرى"], state="readonly", width=10)
        cat_cb.pack(side=tk.RIGHT, padx=(6, 0))
        tk.Label(opt_row, text="التصنيف:", font=(THEME["font_family"], 10), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT, padx=(10, 2))

        self.prio_var = tk.StringVar(value="متوسطة")
        prio_cb = ttk.Combobox(opt_row, textvariable=self.prio_var, values=["عالية", "متوسطة", "منخفضة"], state="readonly", width=10)
        prio_cb.pack(side=tk.RIGHT, padx=(6, 0))
        tk.Label(opt_row, text="الأولوية:", font=(THEME["font_family"], 10), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.RIGHT, padx=(10, 2))

        # Toolbar: Filter & Search
        tools = tk.Frame(body, bg=THEME["bg"])
        tools.pack(fill=tk.X, pady=(0, 8))

        self.btn_f_all = tk.Button(tools, text="جميع المهام", bg="#334155", fg="#FFFFFF", relief=tk.FLAT, font=(THEME["font_family"], 9), command=lambda: self.set_filter("all"))
        self.btn_f_all.pack(side=tk.RIGHT, padx=2)

        self.btn_f_pend = tk.Button(tools, text="⏳ قيد التنفيذ", bg=THEME["surface"], fg=THEME["text_muted"], relief=tk.FLAT, font=(THEME["font_family"], 9), command=lambda: self.set_filter("pending"))
        self.btn_f_pend.pack(side=tk.RIGHT, padx=2)

        self.btn_f_done = tk.Button(tools, text="✅ المكتملة", bg=THEME["surface"], fg=THEME["text_muted"], relief=tk.FLAT, font=(THEME["font_family"], 9), command=lambda: self.set_filter("completed"))
        self.btn_f_done.pack(side=tk.RIGHT, padx=2)

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh())
        s_entry = tk.Entry(tools, textvariable=self.search_var, font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#FFFFFF", insertbackground=THEME["accent_cyan"], relief=tk.FLAT)
        s_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=3, padx=(0, 10))
        tk.Label(tools, text="🔍 بحث:", font=(THEME["font_family"], 9), bg=THEME["bg"], fg=THEME["text_muted"]).pack(side=tk.LEFT, padx=(0, 4))

        # Tasks Table
        table_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True)

        cols = ("id", "status", "title", "category", "priority", "date")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

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

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-Button-1>", lambda e: self.on_toggle())

        # Action Buttons Bottom
        actions = tk.Frame(body, bg=THEME["bg"], pady=8)
        actions.pack(fill=tk.X)

        tk.Button(actions, text="✔ تغيير الحالة (مكتمل / قيد التنفيذ)", font=(THEME["font_family"], 10), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_toggle).pack(side=tk.RIGHT, padx=4)
        tk.Button(actions, text="✏ تعديل", font=(THEME["font_family"], 10), bg="#6366F1", fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_edit).pack(side=tk.RIGHT, padx=4)
        tk.Button(actions, text="🗑 حذف", font=(THEME["font_family"], 10), bg=THEME["danger"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_delete).pack(side=tk.RIGHT, padx=4)
        tk.Button(actions, text="🧹 مسح المكتملة", font=(THEME["font_family"], 10), bg="#475569", fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_clear_completed).pack(side=tk.LEFT, padx=4)

    def set_filter(self, f_type):
        self.current_filter = f_type
        self.btn_f_all.config(bg="#334155" if f_type == "all" else THEME["surface"], fg="#FFFFFF" if f_type == "all" else THEME["text_muted"])
        self.btn_f_pend.config(bg="#334155" if f_type == "pending" else THEME["surface"], fg="#FFFFFF" if f_type == "pending" else THEME["text_muted"])
        self.btn_f_done.config(bg="#334155" if f_type == "completed" else THEME["surface"], fg="#FFFFFF" if f_type == "completed" else THEME["text_muted"])
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        stats = self.manager.get_stats()
        self.stats_lbl.config(text=f"الإنجاز: {stats['completed']}/{stats['total']} ({stats['pct']}%)")

        tasks = self.manager.filter_tasks(self.current_filter, self.search_var.get())
        for task in tasks:
            status_tag = "✅ منجزة" if task.get("completed", False) else "⏳ جارية"
            p = task.get("priority", "متوسطة")
            p_badge = f"🔴 {p}" if p == "عالية" else (f"🟡 {p}" if p == "متوسطة" else f"🟢 {p}")
            self.tree.insert("", tk.END, values=(task["id"], status_tag, task["title"], task["category"], p_badge, task.get("date", "")))

    def on_add(self):
        title = self.entry_task.get().strip()
        if not title:
            messagebox.showwarning("تنبيه", "يرجى كتابة عنوان المهمة!")
            return
        self.manager.add_task(title, self.cat_var.get(), self.prio_var.get())
        self.entry_task.delete(0, tk.END)
        self.refresh()

    def get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def on_toggle(self):
        t_id = self.get_selected_id()
        if t_id is None:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة أولاً!")
            return
        self.manager.toggle_completed(t_id)
        self.refresh()

    def on_edit(self):
        t_id = self.get_selected_id()
        if t_id is None:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة لتعديلها!")
            return
        task = next((t for t in self.manager.tasks if t["id"] == t_id), None)
        if not task:
            return
        new_title = simpledialog.askstring("تعديل المهمة", "اكتب العنوان الجديد:", initialvalue=task["title"])
        if new_title and new_title.strip():
            self.manager.update_task_title(t_id, new_title)
            self.refresh()

    def on_delete(self):
        t_id = self.get_selected_id()
        if t_id is None:
            messagebox.showinfo("ملاحظة", "يرجى تحديد مهمة لحذفها!")
            return
        if messagebox.askyesno("تأكيد الحذف", "هل تريد بالتأكيد حذف هذه المهمة؟"):
            self.manager.delete_task(t_id)
            self.refresh()

    def on_clear_completed(self):
        count = self.manager.clear_completed()
        if count == 0:
            messagebox.showinfo("معلومة", "لا توجد أي مهام مكتملة للمسح!")
        else:
            self.refresh()
            messagebox.showinfo("نجاح", f"تم مسح {count} مهمة مكتملة.")
