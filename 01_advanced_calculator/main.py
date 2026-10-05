#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 1: حاسبة متقدمة (Advanced Scientific Calculator)
يدعم:
- العمليات الحسابية الأساسية (+, -, ×, ÷)
- الأسس والجذور (x², xʸ, √x, ³√x)
- الدوال المثلثية (sin, cos, tan) واللوغاريتمات (log, ln)
- النسبة المئوية والقيمة المطلقة والعاملي (n!)
- سجل كامل للعمليات السابقة مع إمكانية استرجاعها
- واجهة Tkinter عصرية ذات تصميم داكن أنيق
"""

import math
import tkinter as tk
from tkinter import ttk, messagebox


class AdvancedCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("حاسبة متقدمة | Advanced Calculator")
        self.geometry("780x560")
        self.minsize(680, 500)
        self.configure(bg="#0F172A")  # Slate 900

        # State variables
        self.expression = ""
        self.history = []

        # Color Palette
        self.colors = {
            "bg": "#0F172A",
            "card": "#1E293B",
            "display_bg": "#0B1120",
            "display_text": "#F8FAFC",
            "display_sub": "#94A3B8",
            "num_btn": "#334155",
            "num_hover": "#475569",
            "op_btn": "#6366F1",      # Indigo
            "op_hover": "#4F46E5",
            "func_btn": "#1E293B",    # Slate
            "func_hover": "#334155",
            "action_btn": "#EF4444",  # Red for clear
            "action_hover": "#DC2626",
            "equal_btn": "#10B981",   # Emerald
            "equal_hover": "#059669",
            "text": "#FFFFFF",
            "border": "#334155"
        }

        self.setup_ui()
        self.bind_keys()

    def setup_ui(self):
        # Main layout: Left is Calculator, Right is History panel
        main_frame = tk.Frame(self, bg=self.colors["bg"])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        # Left Frame: Calculator
        calc_frame = tk.Frame(main_frame, bg=self.colors["bg"])
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right Frame: History Panel
        history_frame = tk.Frame(main_frame, bg=self.colors["card"], width=240, bd=1, relief=tk.SOLID)
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        history_frame.pack_propagate(False)

        self.setup_display(calc_frame)
        self.setup_buttons(calc_frame)
        self.setup_history(history_frame)

    def setup_display(self, parent):
        display_frame = tk.Frame(parent, bg=self.colors["display_bg"], bd=2, relief=tk.FLAT)
        display_frame.pack(fill=tk.X, pady=(0, 14), ipady=10)

        # Sub expression display (previous operation)
        self.sub_var = tk.StringVar(value="")
        self.sub_display = tk.Label(
            display_frame,
            textvariable=self.sub_var,
            font=("Segoe UI", 12),
            bg=self.colors["display_bg"],
            fg=self.colors["display_sub"],
            anchor="e",
            padx=14
        )
        self.sub_display.pack(fill=tk.X)

        # Main result / input display
        self.main_var = tk.StringVar(value="0")
        self.main_display = tk.Label(
            display_frame,
            textvariable=self.main_var,
            font=("Segoe UI", 26, "bold"),
            bg=self.colors["display_bg"],
            fg=self.colors["display_text"],
            anchor="e",
            padx=14
        )
        self.main_display.pack(fill=tk.X)

    def setup_buttons(self, parent):
        btn_frame = tk.Frame(parent, bg=self.colors["bg"])
        btn_frame.pack(fill=tk.BOTH, expand=True)

        for i in range(6):
            btn_frame.rowconfigure(i, weight=1)
        for j in range(5):
            btn_frame.columnconfigure(j, weight=1)

        # Grid of buttons: (Label, Command, Type)
        # Type: 'func', 'op', 'num', 'action', 'equal'
        buttons = [
            ("2nd / C", self.action_clear, "action"),
            ("CE", self.action_backspace, "action"),
            ("(", lambda: self.append_char("("), "func"),
            (")", lambda: self.append_char(")"), "func"),
            ("÷", lambda: self.append_char("/"), "op"),

            ("sin", lambda: self.calc_func("sin"), "func"),
            ("cos", lambda: self.calc_func("cos"), "func"),
            ("tan", lambda: self.calc_func("tan"), "func"),
            ("π", lambda: self.append_char(str(math.pi)), "func"),
            ("×", lambda: self.append_char("*"), "op"),

            ("x²", lambda: self.append_char("**2"), "func"),
            ("xʸ", lambda: self.append_char("**"), "func"),
            ("7", lambda: self.append_char("7"), "num"),
            ("8", lambda: self.append_char("8"), "num"),
            ("9", lambda: self.append_char("9"), "num"),

            ("√x", lambda: self.calc_func("sqrt"), "func"),
            ("n!", lambda: self.calc_func("fact"), "func"),
            ("4", lambda: self.append_char("4"), "num"),
            ("5", lambda: self.append_char("5"), "num"),
            ("6", lambda: self.append_char("6"), "num"),

            ("ln", lambda: self.calc_func("ln"), "func"),
            ("log", lambda: self.calc_func("log"), "func"),
            ("1", lambda: self.append_char("1"), "num"),
            ("2", lambda: self.append_char("2"), "num"),
            ("3", lambda: self.append_char("3"), "num"),

            ("%", lambda: self.append_char("/100"), "func"),
            ("±", self.action_negate, "func"),
            ("0", lambda: self.append_char("0"), "num"),
            (".", lambda: self.append_char("."), "num"),
            ("=", self.calculate_result, "equal"),
        ]

        # Extra operator column placement
        # Let's organize into standard 6 rows x 5 columns
        button_layout = [
            [("C", self.action_clear, "action"), ("CE", self.action_backspace, "action"), ("(", lambda: self.append_char("("), "func"), (")", lambda: self.append_char(")"), "func"), ("÷", lambda: self.append_char("/"), "op")],
            [("sin", lambda: self.calc_func("sin"), "func"), ("cos", lambda: self.calc_func("cos"), "func"), ("tan", lambda: self.calc_func("tan"), "func"), ("π", lambda: self.append_char(f"{math.pi:.4f}"), "func"), ("×", lambda: self.append_char("*"), "op")],
            [("x²", lambda: self.calc_func("sqr"), "func"), ("√x", lambda: self.calc_func("sqrt"), "func"), ("7", lambda: self.append_char("7"), "num"), ("8", lambda: self.append_char("8"), "num"), ("9", lambda: self.append_char("9"), "num")],
            [("xʸ", lambda: self.append_char("**"), "func"), ("n!", lambda: self.calc_func("fact"), "func"), ("4", lambda: self.append_char("4"), "num"), ("5", lambda: self.append_char("5"), "num"), ("6", lambda: self.append_char("6"), "num")],
            [("log", lambda: self.calc_func("log"), "func"), ("ln", lambda: self.calc_func("ln"), "func"), ("1", lambda: self.append_char("1"), "num"), ("2", lambda: self.append_char("2"), "num"), ("3", lambda: self.append_char("3"), "num")],
            [("±", self.action_negate, "func"), ("%", lambda: self.calc_func("pct"), "func"), ("0", lambda: self.append_char("0"), "num"), (".", lambda: self.append_char("."), "num"), ("=", self.calculate_result, "equal")],
        ]

        # In addition, we need + and - operations. Let's make an intuitive 6x6 or adjust column 5
        # Let's create an elegant 6x5 layout with +, -, *, / nicely mapped:
        layout = [
            [("C", self.action_clear, "action"), ("⌫", self.action_backspace, "action"), ("^", lambda: self.append_char("**"), "func"), ("√", lambda: self.calc_func("sqrt"), "func"), ("÷", lambda: self.append_char("/"), "op")],
            [("sin", lambda: self.calc_func("sin"), "func"), ("cos", lambda: self.calc_func("cos"), "func"), ("tan", lambda: self.calc_func("tan"), "func"), ("n!", lambda: self.calc_func("fact"), "func"), ("×", lambda: self.append_char("*"), "op")],
            [("log", lambda: self.calc_func("log"), "func"), ("7", lambda: self.append_char("7"), "num"), ("8", lambda: self.append_char("8"), "num"), ("9", lambda: self.append_char("9"), "num"), ("-", lambda: self.append_char("-"), "op")],
            [("ln", lambda: self.calc_func("ln"), "func"), ("4", lambda: self.append_char("4"), "num"), ("5", lambda: self.append_char("5"), "num"), ("6", lambda: self.append_char("6"), "num"), ("+", lambda: self.append_char("+"), "op")],
            [("x²", lambda: self.calc_func("sqr"), "func"), ("1", lambda: self.append_char("1"), "num"), ("2", lambda: self.append_char("2"), "num"), ("3", lambda: self.append_char("3"), "num"), ("%", lambda: self.calc_func("pct"), "func")],
            [("π", lambda: self.append_char(f"{math.pi:.4f}"), "func"), ("±", self.action_negate, "func"), ("0", lambda: self.append_char("0"), "num"), (".", lambda: self.append_char("."), "num"), ("=", self.calculate_result, "equal")]
        ]

        for r_idx, row in enumerate(layout):
            for c_idx, (text, cmd, b_type) in enumerate(row):
                bg_col = self.colors["num_btn"]
                fg_col = self.colors["text"]
                font_spec = ("Segoe UI", 13, "bold") if b_type in ["op", "equal"] else ("Segoe UI", 12)

                if b_type == "op":
                    bg_col = self.colors["op_btn"]
                elif b_type == "equal":
                    bg_col = self.colors["equal_btn"]
                elif b_type == "action":
                    bg_col = self.colors["action_btn"]
                elif b_type == "func":
                    bg_col = self.colors["func_btn"]

                btn = tk.Button(
                    btn_frame,
                    text=text,
                    command=cmd,
                    font=font_spec,
                    bg=bg_col,
                    fg=fg_col,
                    activebackground="#64748B",
                    activeforeground="#FFFFFF",
                    relief=tk.FLAT,
                    bd=0,
                    cursor="hand2"
                )
                btn.grid(row=r_idx, column=c_idx, sticky="nsew", padx=3, pady=3)

    def setup_history(self, parent):
        header = tk.Frame(parent, bg=self.colors["card"])
        header.pack(fill=tk.X, padx=10, pady=10)

        title = tk.Label(
            header,
            text="سجل العمليات (History)",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["card"],
            fg="#F8FAFC"
        )
        title.pack(side=tk.LEFT)

        clear_btn = tk.Button(
            header,
            text="مسح",
            font=("Segoe UI", 9),
            bg="#334155",
            fg="#F87171",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_history
        )
        clear_btn.pack(side=tk.RIGHT)

        # History listbox
        self.history_listbox = tk.Listbox(
            parent,
            bg="#0F172A",
            fg="#E2E8F0",
            font=("Consolas", 10),
            selectbackground="#4F46E5",
            selectforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.history_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.history_listbox.bind("<Double-Button-1>", self.reuse_history_item)

        hint = tk.Label(
            parent,
            text="انقر مرتين على أي عملية لإعادة استخدامها",
            font=("Segoe UI", 8),
            bg=self.colors["card"],
            fg="#94A3B8",
            pady=4
        )
        hint.pack(fill=tk.X)

    def bind_keys(self):
        self.bind("<Return>", lambda e: self.calculate_result())
        self.bind("<BackSpace>", lambda e: self.action_backspace())
        self.bind("<Escape>", lambda e: self.action_clear())
        for ch in "0123456789+-*/.()":
            self.bind(ch, lambda e, c=ch: self.append_char(c))

    def append_char(self, char):
        if self.main_var.get() == "0" and char not in ".+-*/":
            self.expression = char
        else:
            self.expression += char
        self.main_var.set(self.expression)

    def action_clear(self):
        self.expression = ""
        self.main_var.set("0")
        self.sub_var.set("")

    def action_backspace(self):
        self.expression = self.expression[:-1]
        self.main_var.set(self.expression if self.expression else "0")

    def action_negate(self):
        if not self.expression:
            return
        try:
            val = float(eval(self.expression))
            self.expression = str(-val)
            self.main_var.set(self.expression)
        except Exception:
            pass

    def calc_func(self, func_name):
        try:
            val = float(eval(self.expression)) if self.expression else 0.0
            result = 0
            expr_str = ""

            if func_name == "sqrt":
                if val < 0:
                    raise ValueError("Negative root")
                result = math.sqrt(val)
                expr_str = f"√({val})"
            elif func_name == "sqr":
                result = val ** 2
                expr_str = f"({val})²"
            elif func_name == "sin":
                result = math.sin(math.radians(val))
                expr_str = f"sin({val}°)"
            elif func_name == "cos":
                result = math.cos(math.radians(val))
                expr_str = f"cos({val}°)"
            elif func_name == "tan":
                result = math.tan(math.radians(val))
                expr_str = f"tan({val}°)"
            elif func_name == "log":
                if val <= 0:
                    raise ValueError("Log of <= 0")
                result = math.log10(val)
                expr_str = f"log({val})"
            elif func_name == "ln":
                if val <= 0:
                    raise ValueError("Ln of <= 0")
                result = math.log(val)
                expr_str = f"ln({val})"
            elif func_name == "fact":
                if val < 0 or not val.is_integer() or val > 100:
                    raise ValueError("Factorial invalid")
                result = math.factorial(int(val))
                expr_str = f"{int(val)}!"
            elif func_name == "pct":
                result = val / 100.0
                expr_str = f"{val}%"

            self.sub_var.set(f"{expr_str} =")
            # Format nicely (remove trailing .0)
            res_str = f"{result:.8f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            self.main_var.set(res_str)
            self.add_to_history(expr_str, res_str)
            self.expression = res_str
        except Exception as e:
            self.main_var.set("خطأ | Error")
            self.expression = ""

    def calculate_result(self):
        if not self.expression:
            return
        try:
            safe_expr = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(safe_expr, {"__builtins__": None}, {"math": math})
            res_str = f"{result:.8f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            
            self.sub_var.set(f"{self.expression} =")
            self.main_var.set(res_str)
            self.add_to_history(self.expression, res_str)
            self.expression = res_str
        except Exception:
            self.main_var.set("خطأ | Error")
            self.expression = ""

    def add_to_history(self, expr, res):
        item = f"{expr} = {res}"
        self.history.append((expr, res))
        self.history_listbox.insert(0, item)

    def clear_history(self):
        self.history.clear()
        self.history_listbox.delete(0, tk.END)

    def reuse_history_item(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            idx = selection[0]
            _, res = self.history[len(self.history) - 1 - idx]
            self.expression = str(res)
            self.main_var.set(self.expression)


if __name__ == "__main__":
    app = AdvancedCalculator()
    app.mainloop()
