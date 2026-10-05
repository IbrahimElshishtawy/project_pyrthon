# -*- coding: utf-8 -*-
"""
محرك العمليات الحسابية للحاسبة المتقدمة
مفصول تماماً عن واجهة المستخدم (Pure Python Business Logic)
"""

import math


class CalculatorEngine:
    def __init__(self):
        self.expression = ""
        self.history = []

    def clear(self):
        self.expression = ""

    def backspace(self):
        self.expression = self.expression[:-1]

    def append(self, text):
        if self.expression == "0" and text not in ".+-*/":
            self.expression = text
        else:
            self.expression += text

    def negate(self):
        if not self.expression:
            return "0"
        try:
            val = float(eval(self.expression))
            self.expression = str(-val)
            return self.expression
        except Exception:
            return self.expression

    def evaluate(self):
        if not self.expression:
            return "0", ""
        try:
            safe_expr = self.expression.replace("×", "*").replace("÷", "/")
            result = eval(safe_expr, {"__builtins__": None}, {"math": math})
            res_str = f"{result:.8f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            orig_expr = self.expression
            self.add_history(orig_expr, res_str)
            self.expression = res_str
            return res_str, f"{orig_expr} ="
        except Exception:
            self.expression = ""
            return "خطأ | Error", ""

    def apply_scientific_function(self, func_name):
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
                    raise ValueError("Log of non-positive")
                result = math.log10(val)
                expr_str = f"log({val})"
            elif func_name == "ln":
                if val <= 0:
                    raise ValueError("Ln of non-positive")
                result = math.log(val)
                expr_str = f"ln({val})"
            elif func_name == "fact":
                if val < 0 or not val.is_integer() or val > 100:
                    raise ValueError("Invalid factorial")
                result = math.factorial(int(val))
                expr_str = f"{int(val)}!"
            elif func_name == "pct":
                result = val / 100.0
                expr_str = f"{val}%"

            res_str = f"{result:.8f}".rstrip("0").rstrip(".") if isinstance(result, float) else str(result)
            self.add_history(expr_str, res_str)
            self.expression = res_str
            return res_str, f"{expr_str} ="
        except Exception:
            self.expression = ""
            return "خطأ | Error", ""

    def add_history(self, expr, res):
        self.history.append((expr, res))

    def clear_history(self):
        self.history.clear()
