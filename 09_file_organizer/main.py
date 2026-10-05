#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 9: منظم الملفات التلقائي الذكي (Smart Automatic File Organizer)
يدعم:
- اختيار أي مجلد على الجهاز (مثل Downloads أو Desktop أو مجلد مخصص)
- فحص وتحليل الملفات وتصنيفها إلى مجموعات:
  • الصور (Images)
  • المستندات (Documents & PDFs)
  • مقاطع الفيديو (Videos)
  • الصوتيات (Audio)
  • الملفات المضغوطة (Archives)
  • البرمجة والكود (Code & Scripts)
  • أخرى (Miscellaneous)
- وضع المعاينة المسبقة (Preview / Dry Run) لمعرفة أين ستنتقل الملفات قبل نقلها
- ميزة التراجع الذكي (Undo Feature) لإعادة الملفات لأماكنها السابقة
- واجهة Tkinter منظمة بألوان أنيقة وشريط تقدم
"""

import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("منظم الملفات التلقائي | File Organizer")
        self.geometry("860x680")
        self.minsize(800, 600)
        self.configure(bg="#0F172A")

        self.selected_dir = ""
        self.categories = {
            "الصور (Images)": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
            "المستندات (Documents)": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
            "الفيديوهات (Videos)": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm"],
            "الصوتيات (Audio)": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
            "الملفات المضغوطة (Archives)": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "الأكواد والبرمجة (Code)": [".py", ".js", ".html", ".css", ".json", ".dart", ".cpp", ".java", ".sql"],
            "أخرى (Other)": []
        }

        self.category_colors = {
            "الصور (Images)": "#EC4899",
            "المستندات (Documents)": "#3B82F6",
            "الفيديوهات (Videos)": "#EF4444",
            "الصوتيات (Audio)": "#F59E0B",
            "الملفات المضغوطة (Archives)": "#8B5CF6",
            "الأكواد والبرمجة (Code)": "#10B981",
            "أخرى (Other)": "#64748B"
        }

        self.planned_moves = []  # List of tuples (src, dest, cat)
        self.undo_history = []   # Last executed move list

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#1E293B", pady=14, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="📁 منظم الملفات والمجلدات التلقائي",
            font=("Segoe UI", 18, "bold"),
            bg="#1E293B",
            fg="#38BDF8"
        )
        title.pack(side=tk.RIGHT)

        sub = tk.Label(
            header,
            text="رتب ملفاتك المبعثرة في مجلدات مرتبة حسب النوع بضغطة زر واحدة",
            font=("Segoe UI", 9),
            bg="#1E293B",
            fg="#94A3B8"
        )
        sub.pack(side=tk.RIGHT, padx=(0, 10))

        # Main Body
        body = tk.Frame(self, bg="#0F172A", padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Directory Selector Card
        dir_card = tk.Frame(body, bg="#1E293B", padx=14, pady=10, bd=1, relief=tk.SOLID)
        dir_card.pack(fill=tk.X, pady=(0, 12))

        btn_browse = tk.Button(
            dir_card,
            text="📂 استعراض مجلد...",
            font=("Segoe UI", 10, "bold"),
            bg="#0284C7",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=14,
            pady=3,
            command=self.browse_folder
        )
        btn_browse.pack(side=tk.LEFT)

        self.path_entry = tk.Entry(
            dir_card,
            font=("Segoe UI", 10),
            bg="#0F172A",
            fg="#F8FAFC",
            insertbackground="#38BDF8",
            relief=tk.FLAT
        )
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, ipady=3)
        self.path_entry.bind("<Return>", lambda e: self.on_path_entered())

        tk.Label(dir_card, text="المسار:", font=("Segoe UI", 10, "bold"), bg="#1E293B", fg="#F8FAFC").pack(side=tk.RIGHT)

        # Quick summary banner
        self.summary_frame = tk.Frame(body, bg="#0F172A")
        self.summary_frame.pack(fill=tk.X, pady=(0, 10))

        # Action Buttons Toolbar
        action_bar = tk.Frame(body, bg="#0F172A")
        action_bar.pack(fill=tk.X, pady=(0, 8))

        self.btn_preview = tk.Button(
            action_bar,
            text="🔍 تحليل ومعاينة النقل (Preview)",
            font=("Segoe UI", 10, "bold"),
            bg="#334155",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.preview_organization
        )
        self.btn_preview.pack(side=tk.RIGHT, padx=4)

        self.btn_organize = tk.Button(
            action_bar,
            text="⚡ تنفيذ التنظيم الفعلي الآن",
            font=("Segoe UI", 10, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=16,
            pady=4,
            state=tk.DISABLED,
            command=self.execute_organization
        )
        self.btn_organize.pack(side=tk.RIGHT, padx=4)

        self.btn_undo = tk.Button(
            action_bar,
            text="↩ تراجع عن آخر نقل (Undo)",
            font=("Segoe UI", 9),
            bg="#EF4444",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            state=tk.DISABLED,
            command=self.undo_organization
        )
        self.btn_undo.pack(side=tk.LEFT)

        # Treeview Preview of Files
        table_card = tk.Frame(body, bg="#1E293B", bd=1, relief=tk.SOLID)
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

        # Bottom Status Bar
        self.status_label = tk.Label(
            body,
            text="يرجى اختيار مجلد للبدء بالتحليل",
            font=("Segoe UI", 9),
            bg="#0F172A",
            fg="#94A3B8"
        )
        self.status_label.pack(anchor="w")

    def browse_folder(self):
        folder = filedialog.askdirectory(title="اختر المجلد المراد تنظيمه")
        if folder:
            self.selected_dir = folder
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder)
            self.preview_organization()

    def on_path_entered(self):
        folder = self.path_entry.get().strip()
        if os.path.exists(folder) and os.path.isdir(folder):
            self.selected_dir = folder
            self.preview_organization()
        else:
            messagebox.showerror("خطأ", "المسار المدخل غير صالح أو ليس مجلداً!")

    def get_category_for_ext(self, ext):
        ext = ext.lower()
        for cat_name, ext_list in self.categories.items():
            if ext in ext_list:
                return cat_name
        return "أخرى (Other)"

    def format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def preview_organization(self):
        folder = self.path_entry.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("تنبيه", "يرجى تحديد مسار مجلد صالح أولاً!")
            return

        self.selected_dir = folder
        self.tree.delete(*self.tree.get_children())
        self.planned_moves.clear()

        cat_counts = {}
        total_files = 0

        try:
            for item in os.listdir(folder):
                full_path = os.path.join(folder, item)
                # Skip subdirectories
                if os.path.isdir(full_path):
                    continue

                total_files += 1
                name, ext = os.path.splitext(item)
                cat = self.get_category_for_ext(ext)
                cat_counts[cat] = cat_counts.get(cat, 0) + 1

                folder_name = cat.split(" ")[0]  # Take Arabic name as folder name
                target_dir = os.path.join(folder, folder_name)
                target_path = os.path.join(target_dir, item)

                try:
                    size = os.path.getsize(full_path)
                    size_str = self.format_size(size)
                except Exception:
                    size_str = "--"

                self.planned_moves.append((full_path, target_path, cat, target_dir))

                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        item,
                        ext or "بدون",
                        size_str,
                        cat,
                        folder_name
                    )
                )

            # Update stats
            self.status_label.config(
                text=f"تم فحص المجلد بنجاح: وجد {total_files} ملف جاهز للتنظيم والتوزيع."
            )

            if total_files > 0:
                self.btn_organize.config(state=tk.NORMAL)
            else:
                self.btn_organize.config(state=tk.DISABLED)
                messagebox.showinfo("معلومة", "المجلد لا يحتوي على أي ملفات مفردة لتنظيمها!")

        except Exception as e:
            messagebox.showerror("خطأ", f"تعذر قراءة محتويات المجلد: {e}")

    def execute_organization(self):
        if not self.planned_moves:
            return

        count = len(self.planned_moves)
        if not messagebox.askyesno("تأكيد التنظيم", f"سيتم تنظيم وتوزيع {count} ملف إلى مجلدات مخصصة.\nهل تريد المتابعة؟"):
            return

        executed = []
        errors = 0

        for src, dest, cat, target_dir in self.planned_moves:
            try:
                os.makedirs(target_dir, exist_ok=True)
                # Avoid overwriting
                final_dest = dest
                if os.path.exists(final_dest) and final_dest != src:
                    base, ext = os.path.splitext(dest)
                    final_dest = f"{base}_new{ext}"

                shutil.move(src, final_dest)
                executed.append((final_dest, src))  # Save for undo (current_loc, orig_loc)
            except Exception as e:
                errors += 1

        self.undo_history = executed
        self.btn_undo.config(state=tk.NORMAL)
        self.btn_organize.config(state=tk.DISABLED)
        self.tree.delete(*self.tree.get_children())
        self.status_label.config(
            text=f"✅ اكتمل التنظيم! تم نقل {len(executed)} ملف بنجاح (الأخطاء: {errors})."
        )
        messagebox.showinfo("نجاح التنظيم", f"تم نقل وتصنيف {len(executed)} ملف بنجاح في مجلدات منظمة!")

    def undo_organization(self):
        if not self.undo_history:
            return

        if not messagebox.askyesno("تأكيد التراجع", f"هل تريد التراجع وإعادة {len(self.undo_history)} ملف إلى أماكنهم الأصلية؟"):
            return

        reverted = 0
        for current_path, original_path in self.undo_history:
            try:
                if os.path.exists(current_path):
                    shutil.move(current_path, original_path)
                    reverted += 1
            except Exception:
                pass

        self.undo_history.clear()
        self.btn_undo.config(state=tk.DISABLED)
        self.status_label.config(text=f"↩ تم التراجع بنجاح وإعادة {reverted} ملف.")
        messagebox.showinfo("تم التراجع", f"تمت إعادة {reverted} ملف إلى المجلد الأساسي بنجاح!")
        self.preview_organization()


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
