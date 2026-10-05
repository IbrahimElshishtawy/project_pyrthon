# -*- coding: utf-8 -*-
"""
واجهة المستخدم الرسومية للحاسبة المتقدمة
"""

import math
import tkinter as tk
from ui.theme import THEME


class CalculatorView(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg=THEME["bg"])
        self.engine = engine

        self.setup_ui()
        self.bind_events()

    def setup_ui(self):
        # Main layout: Left Calculator, Right History panel
        main_layout = tk.Frame(self, bg=THEME["bg"])
        main_layout.pack(fill=tk.BOTH, expand=True, padx=16, pady=16)

        calc_frame = tk.Frame(main_layout, bg=THEME["bg"])
        calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 12))

        history_frame = tk.Frame(main_layout, bg=THEME["card"], width=250, bd=1, relief=tk.SOLID)
        history_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        history_frame.pack_propagate(False)

        # 1. Display
        disp_card = tk.Frame(calc_frame, bg=THEME["display_bg"], bd=1, relief=tk.SOLID, padx=14, pady=12)
        disp_card.pack(fill=tk.X, pady=(0, 14))

        self.sub_var = tk.StringVar(value="")
        self.sub_label = tk.Label(
            disp_card,
            textvariable=self.sub_var,
            font=(THEME["font_family"], 11),
            bg=THEME["display_bg"],
            fg=THEME["display_sub"],
            anchor="e"
        )
        self.sub_label.pack(fill=tk.X)

        self.main_var = tk.StringVar(value="0")
        self.main_label = tk.Label(
            disp_card,
            textvariable=self.main_var,
            font=(THEME["font_family"], 28, "bold"),
            bg=THEME["display_bg"],
            fg=THEME["display_text"],
            anchor="e"
        )
        self.main_label.pack(fill=tk.X)

        # 2. Keypad Grid
        grid_frame = tk.Frame(calc_frame, bg=THEME["bg"])
        grid_frame.pack(fill=tk.BOTH, expand=True)

        for i in range(6):
            grid_frame.rowconfigure(i, weight=1)
        for j in range(5):
            grid_frame.columnconfigure(j, weight=1)

        layout = [
            [("C", self.on_clear, "action"), ("⌫", self.on_backspace, "action"), ("xʸ", lambda: self.on_char("**"), "func"), ("√", lambda: self.on_func("sqrt"), "func"), ("÷", lambda: self.on_char("/"), "op")],
            [("sin", lambda: self.on_func("sin"), "func"), ("cos", lambda: self.on_func("cos"), "func"), ("tan", lambda: self.on_func("tan"), "func"), ("n!", lambda: self.on_func("fact"), "func"), ("×", lambda: self.on_char("*"), "op")],
            [("log", lambda: self.on_func("log"), "func"), ("7", lambda: self.on_char("7"), "num"), ("8", lambda: self.on_char("8"), "num"), ("9", lambda: self.on_char("9"), "num"), ("-", lambda: self.on_char("-"), "op")],
            [("ln", lambda: self.on_func("ln"), "func"), ("4", lambda: self.on_char("4"), "num"), ("5", lambda: self.on_char("5"), "num"), ("6", lambda: self.on_char("6"), "num"), ("+", lambda: self.on_char("+"), "op")],
            [("x²", lambda: self.on_func("sqr"), "func"), ("1", lambda: self.on_char("1"), "num"), ("2", lambda: self.on_char("2"), "num"), ("3", lambda: self.on_char("3"), "num"), ("%", lambda: self.on_func("pct"), "func")],
            [("π", lambda: self.on_char(f"{math.pi:.4f}"), "func"), ("±", self.on_negate, "func"), ("0", lambda: self.on_char("0"), "num"), (".", lambda: self.on_char("."), "num"), ("=", self.on_eval, "equal")]
        ]

        for r_idx, row in enumerate(layout):
            for c_idx, (text, cmd, b_type) in enumerate(row):
                bg_col = THEME["num_btn"]
                fg_col = THEME["text"]
                font_spec = (THEME["font_family"], 13, "bold") if b_type in ["op", "equal"] else (THEME["font_family"], 12)

                if b_type == "op":
                    bg_col = THEME["op_btn"]
                elif b_type == "equal":
                    bg_col = THEME["equal_btn"]
                elif b_type == "action":
                    bg_col = THEME["action_btn"]
                elif b_type == "func":
                    bg_col = THEME["func_btn"]

                btn = tk.Button(
                    grid_frame,
                    text=text,
                    command=cmd,
                    font=font_spec,
                    bg=bg_col,
                    fg=fg_col,
                    activebackground="#475569",
                    activeforeground="#FFFFFF",
                    relief=tk.FLAT,
                    bd=0,
                    cursor="hand2"
                )
                btn.grid(row=r_idx, column=c_idx, sticky="nsew", padx=3, pady=3)

        # 3. History Panel
        h_top = tk.Frame(history_frame, bg=THEME["card"], padx=10, pady=10)
        h_top.pack(fill=tk.X)
        tk.Label(h_top, text="سجل العمليات (History)", font=(THEME["font_family"], 11, "bold"), bg=THEME["card"], fg="#F8FAFC").pack(side=tk.LEFT)
        tk.Button(h_top, text="مسح", font=(THEME["font_family"], 8), bg="#334155", fg="#F87171", relief=tk.FLAT, cursor="hand2", command=self.clear_history).pack(side=tk.RIGHT)

        self.hist_listbox = tk.Listbox(
            history_frame,
            bg=THEME["bg"],
            fg="#E2E8F0",
            font=("Consolas", 10),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground=THEME["op_btn"]
        )
        self.hist_listbox.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))
        self.hist_listbox.bind("<Double-Button-1>", self.on_history_select)

    def bind_events(self):
        parent = self.winfo_toplevel()
        parent.bind("<Return>", lambda e: self.on_eval())
        parent.bind("<BackSpace>", lambda e: self.on_backspace())
        parent.bind("<Escape>", lambda e: self.on_clear())
        for ch in "0123456789+-*/.()":
            parent.bind(ch, lambda e, c=ch: self.on_char(c))

    def on_char(self, c):
        self.engine.append(c)
        self.main_var.set(self.engine.expression)

    def on_clear(self):
        self.engine.clear()
        self.main_var.set("0")
        self.sub_var.set("")

    def on_backspace(self):
        self.engine.backspace()
        self.main_var.set(self.engine.expression if self.engine.expression else "0")

    def on_negate(self):
        val = self.engine.negate()
        self.main_var.set(val)

    def on_func(self, func_name):
        res, sub = self.engine.apply_scientific_function(func_name)
        self.main_var.set(res)
        self.sub_var.set(sub)
        self.refresh_history()

    def on_eval(self):
        res, sub = self.engine.evaluate()
        self.main_var.set(res)
        self.sub_var.set(sub)
        self.refresh_history()

    def refresh_history(self):
        self.hist_listbox.delete(0, tk.END)
        for expr, res in reversed(self.engine.history):
            self.hist_listbox.insert(tk.END, f"{expr} = {res}")

    def clear_history(self):
        self.engine.clear_history()
        self.hist_listbox.delete(0, tk.END)

    def on_history_select(self, event):
        sel = self.hist_listbox.curselection()
        if sel:
            idx = sel[0]
            # retrieve from reversed
            real_idx = len(self.engine.history) - 1 - idx
            _, res = self.engine.history[real_idx]
            self.engine.expression = str(res)
            self.main_var.set(str(res))
