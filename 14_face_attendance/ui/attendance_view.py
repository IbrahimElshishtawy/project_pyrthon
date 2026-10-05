# -*- coding: utf-8 -*-
"""
واجهة المستخدم لمنظومة تسجيل الحضور
"""

import csv
import random
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, ttk
from ui.theme import THEME
from ui.scanner_canvas import draw_biometric_hud


class AttendanceView(tk.Frame):
    def __init__(self, parent, service):
        super().__init__(parent, bg=THEME["bg"])
        self.service = service
        self.scan_y = 50
        self.scan_dir = 4
        self.is_scanning = True

        self.setup_ui()
        self.refresh_table()
        self.start_animation()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🛡️ منظومة التعرف على الوجوه وتسجيل الحضور الذكية",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_cyan"]
        )
        title.pack(side=tk.RIGHT)

        lbl_cam = tk.Label(
            header,
            text="✨ ماسح بيومتري محاكي فائق الذكاء",
            font=(THEME["font_family"], 10, "bold"),
            bg="#065F46",
            fg="#A7F3D0",
            padx=10,
            pady=4
        )
        lbl_cam.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Top KPI
        stats_frame = tk.Frame(body, bg=THEME["bg"])
        stats_frame.pack(fill=tk.X, pady=(0, 12))

        st = self.service.get_stats()
        self.card_total = self.create_kpi_card(stats_frame, "إجمالي المسجلين", str(st["total_members"]), THEME["accent_cyan"])
        self.card_present = self.create_kpi_card(stats_frame, "حضور اليوم", f"{st['today_present']} موظف", THEME["success"])
        self.create_kpi_card(stats_frame, "حالة المسح", "نشط ومستعد ✅", THEME["gold"])

        # Split
        split = tk.Frame(body, bg=THEME["bg"])
        split.pack(fill=tk.BOTH, expand=True)

        # Right Column: Scanner
        scanner_col = tk.Frame(split, bg=THEME["surface"], width=420, bd=1, relief=tk.SOLID, padx=14, pady=12)
        scanner_col.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        scanner_col.pack_propagate(False)

        tk.Label(scanner_col, text="🎥 عدسة التعرف البيومتري على الوجه:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(anchor="e", pady=(0, 6))

        self.cam_canvas = tk.Canvas(scanner_col, width=380, height=260, bg="#030712", highlightthickness=1, highlightbackground=THEME["accent_cyan"])
        self.cam_canvas.pack(pady=4)

        tk.Label(scanner_col, text="اختر العضو لتسجيل البصمة:", font=(THEME["font_family"], 9, "bold"), bg=THEME["surface"], fg=THEME["text_muted"]).pack(anchor="e", pady=(8, 2))

        self.sel_member_var = tk.StringVar()
        member_names = [f"{m['name']} ({m['id']})" for m in self.service.members]
        if member_names:
            self.sel_member_var.set(member_names[0])
        self.member_combo = ttk.Combobox(scanner_col, textvariable=self.sel_member_var, values=member_names, state="readonly")
        self.member_combo.pack(fill=tk.X, pady=(0, 8))

        btn_frame = tk.Frame(scanner_col, bg=THEME["surface"])
        btn_frame.pack(fill=tk.X, pady=4)

        btn_checkin = tk.Button(btn_frame, text="🟢 تسجيل حضور (Check In)", font=(THEME["font_family"], 10, "bold"), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, pady=4, command=lambda: self.on_record_attendance("حضور"))
        btn_checkin.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=(4, 0))

        btn_checkout = tk.Button(btn_frame, text="🔴 تسجيل انصراف (Check Out)", font=(THEME["font_family"], 10, "bold"), bg=THEME["danger"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, pady=4, command=lambda: self.on_record_attendance("انصراف"))
        btn_checkout.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 4))

        btn_new_emp = tk.Button(scanner_col, text="➕ تسجيل عضو / موظف جديد بالبصمة", font=(THEME["font_family"], 10), bg=THEME["surface_light"], fg="#60A5FA", relief=tk.FLAT, cursor="hand2", pady=4, command=self.open_register_dialog)
        btn_new_emp.pack(fill=tk.X, pady=(10, 0))

        # Left Column: Table
        table_col = tk.Frame(split, bg=THEME["surface"], bd=1, relief=tk.SOLID)
        table_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        t_head = tk.Frame(table_col, bg=THEME["surface"], padx=10, pady=8)
        t_head.pack(fill=tk.X)
        tk.Label(t_head, text="📋 سجل الحضور والانصراف المباشر:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg=THEME["text_main"]).pack(side=tk.RIGHT)
        tk.Button(t_head, text="تصدير السجل إلى CSV", font=(THEME["font_family"], 8), bg=THEME["primary"], fg="#FFFFFF", relief=tk.FLAT, command=self.export_csv).pack(side=tk.LEFT)

        cols = ("id", "name", "dept", "time", "type")
        self.tree = ttk.Treeview(table_col, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("id", text="الرقم")
        self.tree.heading("name", text="الاسم")
        self.tree.heading("dept", text="القسم")
        self.tree.heading("time", text="التاريخ والوقت")
        self.tree.heading("type", text="الحالة")

        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=140, anchor="w")
        self.tree.column("dept", width=110, anchor="center")
        self.tree.column("time", width=140, anchor="center")
        self.tree.column("type", width=80, anchor="center")

        scroll = ttk.Scrollbar(table_col, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def create_kpi_card(self, parent, title, val, color):
        c = tk.Frame(parent, bg=THEME["surface"], padx=14, pady=8, bd=1, relief=tk.SOLID)
        c.pack(side=tk.RIGHT, expand=True, fill=tk.X, padx=4)
        tk.Label(c, text=title, font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(anchor="e")
        lbl = tk.Label(c, text=val, font=(THEME["font_family"], 15, "bold"), bg=THEME["surface"], fg=color)
        lbl.pack(anchor="e")
        return lbl

    def start_animation(self):
        def loop():
            if not self.is_scanning:
                return
            draw_biometric_hud(self.cam_canvas, self.scan_y)
            self.scan_y += self.scan_dir
            if self.scan_y > 230 or self.scan_y < 30:
                self.scan_dir *= -1
            self.after(50, loop)

        loop()

    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in self.service.attendance_records:
            type_tag = "🟢 حضور" if r["type"] == "حضور" else "🔴 انصراف"
            self.tree.insert("", tk.END, values=(r["id"], r["name"], r["dept"], r["time"], type_tag))

        st = self.service.get_stats()
        self.card_total.config(text=str(st["total_members"]))
        self.card_present.config(text=f"{st['today_present']} موظف")

    def on_record_attendance(self, att_type):
        sel = self.sel_member_var.get()
        if not sel:
            messagebox.showwarning("تنبيه", "يرجى اختيار عضو لتسجيل حضوره!")
            return

        emp_id = sel.split("(")[-1].rstrip(")")
        try:
            rec = self.service.record_attendance(emp_id, att_type)
            self.refresh_table()
            messagebox.showinfo("تم التسجيل بنجاح", f"✅ تم تسجيل {att_type} للموظف:\n{rec['name']} ({rec['id']})\nالوقت: {rec['time']}")
        except Exception as e:
            messagebox.showerror("خطأ", str(e))

    def open_register_dialog(self):
        top = tk.Toplevel(self)
        top.title("تسجيل عضو جديد بالبصمة الوجهية")
        top.geometry("400x320")
        top.configure(bg=THEME["surface"])

        tk.Label(top, text="👤 بيانات العضو الجديد:", font=(THEME["font_family"], 12, "bold"), bg=THEME["surface"], fg=THEME["accent_cyan"]).pack(pady=12)

        tk.Label(top, text="الاسم الكامل:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg="#E5E7EB").pack(anchor="e", padx=20)
        e_name = tk.Entry(top, font=(THEME["font_family"], 10), bg=THEME["surface_card"], fg="#FFFFFF", relief=tk.FLAT)
        e_name.pack(fill=tk.X, padx=20, pady=(2, 8))

        tk.Label(top, text="الرقم الوظيفي / المعرف:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg="#E5E7EB").pack(anchor="e", padx=20)
        e_id = tk.Entry(top, font=(THEME["font_family"], 10), bg=THEME["surface_card"], fg="#FFFFFF", relief=tk.FLAT)
        e_id.pack(fill=tk.X, padx=20, pady=(2, 8))
        e_id.insert(0, f"EMP-{random.randint(104, 999)}")

        tk.Label(top, text="القسم:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg="#E5E7EB").pack(anchor="e", padx=20)
        e_dept = tk.Entry(top, font=(THEME["font_family"], 10), bg=THEME["surface_card"], fg="#FFFFFF", relief=tk.FLAT)
        e_dept.pack(fill=tk.X, padx=20, pady=(2, 12))
        e_dept.insert(0, "الهندسة والتقنية")

        def submit():
            name = e_name.get().strip()
            mem_id = e_id.get().strip()
            dept = e_dept.get().strip()
            if not name or not mem_id:
                messagebox.showwarning("تنبيه", "يرجى إكمال البيانات المطلوبة!")
                return

            self.service.register_member(name, mem_id, dept)
            names = [f"{m['name']} ({m['id']})" for m in self.service.members]
            self.member_combo["values"] = names
            self.sel_member_var.set(names[-1])
            self.refresh_table()
            top.destroy()
            messagebox.showinfo("نجاح", f"تم تسجيل العضو {name} بالبصمة بنجاح!")

        tk.Button(top, text="حفظ والتقاط البصمة", font=(THEME["font_family"], 10, "bold"), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", command=submit).pack(fill=tk.X, padx=20, pady=8)

    def export_csv(self):
        if not self.service.attendance_records:
            messagebox.showinfo("تنبيه", "لا توجد سجلات لتصديرها!")
            return
        dest = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("ملف CSV", "*.csv")], initialfile="سجل_الحضور_الكامل.csv")
        if dest:
            try:
                with open(dest, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.writer(f)
                    w.writerow(["الرقم الوظيفي", "الاسم", "القسم", "التاريخ والوقت", "الحالة"])
                    for r in self.service.attendance_records:
                        w.writerow([r["id"], r["name"], r["dept"], r["time"], r["type"]])
                messagebox.showinfo("تم التصدير", "تم تصدير ملف الحضور بنجاح!")
            except Exception as e:
                messagebox.showerror("خطأ", str(e))
