# -*- coding: utf-8 -*-
"""
وحدة معالجة وتنسيق النصوص والخطوط العربية (Universal Arabic & BiDi Formatting Helper)
تقوم بـ:
1. معالجة اتصال الحروف العربية ومنع تقطيعها أو عكسها (Glyph Reshaping & BiDi Layout)
2. الكشف الذكي عن أفضل خط عربي مثبت في النظام (Cross-Platform Font Resolution)
3. التفعيل التلقائي (enable_arabic_support) لضبط جميع عناصر Tkinter لتدعم العربية فورياً
"""

import sys
import os

# التحقق من توفر مكتبات التشكيل وإعادة التوجيه
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_BIDI_LIBS = True
except ImportError:
    HAS_BIDI_LIBS = False


def ar(text):
    """
    تنسيق النص العربي ليتصل بشكل صحيح ولا يظهر مقطعاً أو معكوساً في نوافذ Tkinter.
    إذا كان النص يحتوي على محارف عربية، يتم تطبيق Reshaping و BiDi.
    """
    if not text or not isinstance(text, str):
        return text

    # فحص ما إذا كان النص يحتوي على حروف عربية
    has_arabic = any(
        "\u0600" <= c <= "\u06ff" or "\u0750" <= c <= "\u077f" or "\u08a0" <= c <= "\u08ff" or "\ufb50" <= c <= "\ufdff" or "\ufe70" <= c <= "\ufeff"
        for c in text
    )
    if not has_arabic:
        return text

    if HAS_BIDI_LIBS:
        try:
            configuration = {
                'delete_harakat': False,
                'support_ligatures': True,
            }
            reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
            reshaped = reshaper.reshape(text)
            return get_display(reshaped)
        except Exception:
            return text

    return text


def detect_best_arabic_font():
    """
    اكتشاف أفضل خط عربي مثبت على نظام التشغيل الحالي (Linux / Windows / macOS)
    """
    candidate_fonts = [
        "Noto Sans Arabic",
        "Noto Kufi Arabic",
        "Noto Naskh Arabic",
        "DejaVu Sans",
        "Segoe UI",
        "Tahoma",
        "Cairo",
        "Amiri",
        "Arial"
    ]

    try:
        import tkinter as tk
        import tkinter.font as tkfont
        root = tk._default_root
        temp_root = False
        if root is None:
            root = tk.Tk()
            root.withdraw()
            temp_root = True

        available = set(tkfont.families(root))
        if temp_root:
            root.destroy()

        for f in candidate_fonts:
            if f in available:
                return f
    except Exception:
        pass

    return "Noto Sans Arabic" if sys.platform.startswith("linux") else "Segoe UI"


FONT_FAMILY = detect_best_arabic_font()


def get_font(size=10, weight="normal"):
    """
    إرجاع مواصفات الخط المناسب لنظام التشغيل
    """
    if weight == "bold":
        return (FONT_FAMILY, size, "bold")
    return (FONT_FAMILY, size)


_ARABIC_SUPPORT_ENABLED = False

def enable_arabic_support():
    """
    تفعيل دعم اللغة العربية تلقائياً في كافة عناصر Tkinter
    يقوم باعتراض وضبط نصوص الـ Labels, Buttons, Canvas, Treeview, و Messagebox
    بحيث تظهر الحروف متصلة وبالاتجاه الصحيح دائماً بدون الحاجة لتعديل يدوي في كل سطر
    """
    global _ARABIC_SUPPORT_ENABLED
    if _ARABIC_SUPPORT_ENABLED:
        return
    _ARABIC_SUPPORT_ENABLED = True

    try:
        import tkinter as tk
        from tkinter import ttk, messagebox

        def _patch_widget_class(cls):
            orig_init = cls.__init__
            orig_config = cls.configure
            orig_setitem = cls.__setitem__

            def new_init(self, *args, **kwargs):
                if "text" in kwargs and isinstance(kwargs["text"], str):
                    kwargs["text"] = ar(kwargs["text"])
                if "font" not in kwargs:
                    kwargs["font"] = (FONT_FAMILY, 9)
                orig_init(self, *args, **kwargs)

            def new_config(self, *args, **kwargs):
                if "text" in kwargs and isinstance(kwargs["text"], str):
                    kwargs["text"] = ar(kwargs["text"])
                orig_config(self, *args, **kwargs)

            def new_setitem(self, key, value):
                if key == "text" and isinstance(value, str):
                    value = ar(value)
                orig_setitem(self, key, value)

            cls.__init__ = new_init
            cls.configure = new_config
            cls.config = new_config
            cls.__setitem__ = new_setitem

        # 1. عناصر Tkinter القياسية
        for wcls in [tk.Label, tk.Button, tk.Radiobutton, tk.Checkbutton,
                     ttk.Label, ttk.Button, ttk.Radiobutton, ttk.Checkbutton]:
            _patch_widget_class(wcls)

        # 2. حقول الإدخال لتكون المحاذاة لليمين عند الكتابة بالعربية
        orig_entry_init = tk.Entry.__init__
        def new_entry_init(self, *args, **kwargs):
            if "justify" not in kwargs:
                kwargs["justify"] = "right"
            if "font" not in kwargs:
                kwargs["font"] = (FONT_FAMILY, 10)
            orig_entry_init(self, *args, **kwargs)
        tk.Entry.__init__ = new_entry_init

        # 3. نصوص الـ Canvas
        orig_create_text = tk.Canvas.create_text
        def new_create_text(self, *args, **kwargs):
            if "text" in kwargs and isinstance(kwargs["text"], str):
                kwargs["text"] = ar(kwargs["text"])
            if "font" not in kwargs:
                kwargs["font"] = (FONT_FAMILY, 9)
            return orig_create_text(self, *args, **kwargs)
        tk.Canvas.create_text = new_create_text

        orig_itemconfig = tk.Canvas.itemconfigure
        def new_itemconfig(self, tagOrId, cnf=None, **kwargs):
            if "text" in kwargs and isinstance(kwargs["text"], str):
                kwargs["text"] = ar(kwargs["text"])
            return orig_itemconfig(self, tagOrId, cnf=cnf, **kwargs)
        tk.Canvas.itemconfigure = new_itemconfig
        tk.Canvas.itemconfig = new_itemconfig

        # 4. عناوين الجداول Treeview
        orig_tree_heading = ttk.Treeview.heading
        def new_tree_heading(self, column, option=None, **kwargs):
            if "text" in kwargs and isinstance(kwargs["text"], str):
                kwargs["text"] = ar(kwargs["text"])
            return orig_tree_heading(self, column, option=option, **kwargs)
        ttk.Treeview.heading = new_tree_heading

        # 5. صناديق التنبيه Messagebox
        for fn_name in ["showinfo", "showwarning", "showerror", "askyesno", "askokcancel", "askquestion"]:
            if hasattr(messagebox, fn_name):
                orig_fn = getattr(messagebox, fn_name)
                def make_wrapper(orig):
                    def wrapper(title=None, message=None, **kwargs):
                        return orig(title=ar(title), message=ar(message), **kwargs)
                    return wrapper
                setattr(messagebox, fn_name, make_wrapper(orig_fn))

    except Exception as e:
        print(f"Warning: Could not enable full Arabic Tkinter patch: {e}")
