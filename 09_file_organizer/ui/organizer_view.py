# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمنظم الملفات التلقائي
"""

import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ui.theme import THEME


class FileOrganizerView(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg=THEME["bg"])
        self.engine = engine

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="📁 منظم الملفات والمجلدات التلقائي",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        sub = tk.Label(
            header,
            text="رتب ملفاتك المبعثرة في مجلدات مرتبة حسب النوع بضغطة زر واحدة",
            font=(THEME["font_family"], 9),
            bg=THEME["surface"],
            fg=THEME["text_muted"]
        )
        sub.pack(side=tk.RIGHT, padx=(0, 10))

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Directory Selector Card
        dir_card = tk.Frame(body, bg=THEME["surface"], padx=14, pady=10, bd=1, relief=tk.SOLID)
        dir_card.pack(fill=tk.X, pady=(0, 12))

        btn_browse = tk.Button(
            dir_card,
            text="📂 استعراض مجلد...",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["primary"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=3,
            command=self.on_browse
        )
        btn_browse.pack(side=tk.LEFT)

        self.path_entry = tk.Entry(
            dir_card,
            font=(THEME["font_family"], 10),
            bg=THEME["bg"],
            fg="#F8FAFC",
            insertbackground=THEME["accent_cyan"],
            relief=tk.FLAT
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=3)
        self.path_entry.bind("<Return>", lambda e: self.on_preview())

        tk.Label(dir_card, text="المسار:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(side=tk.RIGHT)

        # Action Toolbar
        action_bar = tk.Frame(body, bg=THEME["bg"])
        action_bar.pack(fill=tk.X, pady=(0, 8))

        self.btn_preview = tk.Button(
            action_bar,
            text="🔍 تحليل ومعاينة النقل (Preview)",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["surface_light"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.on_preview
        )
        self.btn_preview.pack(side=tk.RIGHT, padx=4)

        self.btn_organize = tk.Button(
            action_bar,
            text="⚡ تنفيذ التنظيم الفعلي الآن",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["success"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4,
            state=tk.DISABLED,
            command=self.on_execute
        )
        self.btn_organize.pack(side=tk.RIGHT, padx=4)

        self.btn_undo = tk.Button(
            action_bar,
            text="↩ تراجع عن آخر نقل (Undo)",
            font=(THEME["font_family"], 9),
            bg=THEME["danger"],
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            state=tk.DISABLED,
            command=self.on_undo
        )
        self.btn_undo.pack(side=tk.LEFT)

        # Table
        table_card = tk.Frame(body, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_card.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        cols = ("name", "ext", "size", "category", "target_folder")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("name", text="اسم الملف")
        self.tree.heading("ext", text="الامتداد")
        self.tree.heading("size", text="الحجم")
        self.tree.heading("category", text="التصنيف المقترح")
        self.tree.heading("target_folder", text="المجلد الوجهة")

        self.tree.column("name", width=260, anchor="w")
        self.tree.column("ext", width=70, anchor="center")
        self.tree.column("size", width=80, anchor="center")
        self.tree.column("category", width=140, anchor="center")
        self.tree.column("target_folder", width=200, anchor="w")

        scroll = ttk.Scrollbar(table_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.status_lbl = tk.Label(body, text="يرجى اختيار مجلد للبدء بالتحليل", font=(THEME["font_family"], 9), bg=THEME["bg"], fg=THEME["text_muted"])
        self.status_lbl.pack(anchor="w")

    def on_browse(self):
        f = filedialog.askdirectory(title="اختر المجلد المراد تنظيمه")
        if f:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, f)
            self.on_preview()

    def on_preview(self):
        folder = self.path_entry.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("تنبيه", "يرجى تحديد مسار مجلد صالح أولاً!")
            return

        self.tree.delete(*self.tree.get_children())
        try:
            files = self.engine.analyze_folder(folder)
            for f in files:
                self.tree.insert("", tk.END, values=(f["name"], f["ext"], f["size"], f["category"], f["target_folder"]))

            self.status_lbl.config(text=f"تم فحص المجلد بنجاح: وجد {len(files)} ملف جاهز للتنظيم.")
            if files:
                self.btn_organize.config(state=tk.NORMAL)
            else:
                self.btn_organize.config(state=tk.DISABLED)
                messagebox.showinfo("معلومة", "المجلد لا يحتوي على أي ملفات مفردة لتنظيمها!")
        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر قراءة المجلد: {e}")

    def on_execute(self):
        if not self.engine.planned_moves:
            return

        count = len(self.engine.planned_moves)
        if not messagebox.askyesno("تأكيد التنظيم", f"سيتم تنظيم وتوزيع {count} ملف إلى مجلدات مخصصة.\nهل تريد المتابعة؟"):
            return

        moved, errors = self.engine.execute_organization()
        self.btn_undo.config(state=tk.NORMAL)
        self.btn_organize.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.status_lbl.config(text=f"✅ اكتمل التنظيم! تم نقل {moved} ملف بنجاح (الأخطاء: {errors}).")
        messagebox.showinfo("نجاح التنظيم", f"تم نقل وتصنيف {moved} ملف بنجاح!")

    def on_undo(self):
        if not self.engine.undo_history:
            return
        if not messagebox.askyesno("تأكيد التراجع", f"هل تريد التراجع وإعادة {len(self.engine.undo_history)} ملف إلى أماكنهم السابقة؟"):
            return

        reverted = self.engine.undo_organization()
        self.btn_undo.config(state=tk.DISABLED)
        self.status_lbl.config(text=f"↩ تم التراجع بنجاح وإعادة {reverted} ملف.")
        messagebox.showinfo("تم التراجع", f"تمت إعادة {reverted} ملف إلى المجلد الأساسي بنجاح!")
        self.on_preview()
