# -*- coding: utf-8 -*-
"""
واجهة المستخدم لنظام توصية الأفلام السينمائي
"""

import tkinter as tk
from tkinter import ttk
from ui.theme import THEME


class MovieRecommenderView(tk.Frame):
    def __init__(self, parent, engine):
        super().__init__(parent, bg=THEME["bg"])
        self.engine = engine
        self.movies = engine.movies
        self.current_movie = None

        self.setup_ui()
        self.refresh_movie_list()

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg=THEME["surface"], pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎬 نظام توصية الأفلام السينمائي الذكي",
            font=(THEME["font_family"], 18, "bold"),
            bg=THEME["surface"],
            fg=THEME["accent_gold"]
        )
        title.pack(side=tk.RIGHT)

        self.btn_wl = tk.Button(
            header,
            text=f"⭐ قائمة المشاهدة ({len(self.engine.watchlist)})",
            font=(THEME["font_family"], 10, "bold"),
            bg=THEME["surface_light"],
            fg="#FBBF24",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.show_watchlist_dialog
        )
        self.btn_wl.pack(side=tk.LEFT)

        # Body
        body = tk.Frame(self, bg=THEME["bg"], padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Search Bar
        tools = tk.Frame(body, bg=THEME["surface"], padx=14, pady=10, bd=1, relief=tk.SOLID)
        tools.pack(fill=tk.X, pady=(0, 12))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_movie_list())
        s_entry = tk.Entry(tools, textvariable=self.search_var, font=(THEME["font_family"], 10), bg=THEME["surface_card"], fg="#FFFFFF", insertbackground=THEME["accent_gold"], relief=tk.FLAT)
        s_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 6), ipady=3)
        tk.Label(tools, text="🔍 ابحث عن فيلم أو مخرج:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg="#E5E7EB").pack(side=tk.RIGHT)

        self.genre_var = tk.StringVar(value="الكل")
        genres = ["الكل", "خيال علمي", "أكشن", "جريمة", "دراما", "رسوم متحركة", "مغامرة"]
        genre_cb = ttk.Combobox(tools, textvariable=self.genre_var, values=genres, state="readonly", width=12)
        genre_cb.pack(side=tk.LEFT, padx=(6, 0))
        genre_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_movie_list())
        tk.Label(tools, text="التصنيف:", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["text_muted"]).pack(side=tk.LEFT, padx=(10, 2))

        # Split
        split = tk.Frame(body, bg=THEME["bg"])
        split.pack(fill=tk.BOTH, expand=True)

        # Left Column: Movies Tree
        left_col = tk.Frame(split, bg=THEME["surface"], bd=1, relief=tk.SOLID, width=440)
        left_col.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        left_col.pack_propagate(False)

        tk.Label(left_col, text="🎞️ اختر فيلماً تحبه لاستخراج توصيات ذكية:", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface"], fg=THEME["text_muted"], padx=10, pady=8).pack(anchor="w")

        cols = ("title", "year", "rating", "genre")
        self.tree = ttk.Treeview(left_col, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("title", text="الفيلم")
        self.tree.heading("year", text="السنة")
        self.tree.heading("rating", text="التقييم")
        self.tree.heading("genre", text="النوع")

        self.tree.column("title", width=160, anchor="w")
        self.tree.column("year", width=50, anchor="center")
        self.tree.column("rating", width=60, anchor="center")
        self.tree.column("genre", width=130, anchor="center")

        scroll = ttk.Scrollbar(left_col, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<<TreeviewSelect>>", self.on_movie_selected)

        # Right Column: Movie Info & AI Recommendations
        right_col = tk.Frame(split, bg=THEME["surface"], bd=1, relief=tk.SOLID, padx=16, pady=14)
        right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_title = tk.Label(right_col, text="اختر فيلماً من القائمة", font=(THEME["font_family"], 16, "bold"), bg=THEME["surface"], fg=THEME["text_main"], anchor="w")
        self.lbl_title.pack(fill=tk.X)

        self.lbl_meta = tk.Label(right_col, text="السنة | التقييم | المخرج", font=(THEME["font_family"], 9), bg=THEME["surface"], fg=THEME["accent_gold"], anchor="w")
        self.lbl_meta.pack(fill=tk.X, pady=(2, 6))

        self.lbl_desc = tk.Label(right_col, text="حدد فيلماً لعرض القصة وتوصيات الذكاء الاصطناعي المشابهة.", font=(THEME["font_family"], 10), bg=THEME["surface"], fg="#D1D5DB", anchor="w", justify="left", wraplength=380)
        self.lbl_desc.pack(fill=tk.X, pady=(0, 10))

        self.btn_add_wl = tk.Button(right_col, text="➕ إضافة لقائمة المشاهدة", font=(THEME["font_family"], 9, "bold"), bg=THEME["success"], fg="#FFFFFF", relief=tk.FLAT, cursor="hand2", padx=10, command=self.on_toggle_watchlist)
        self.btn_add_wl.pack(anchor="w", pady=(0, 14))

        # Recommendations Box
        recs_head = tk.Frame(right_col, bg=THEME["surface_card"], padx=8, pady=4)
        recs_head.pack(fill=tk.X, pady=(0, 6))
        tk.Label(recs_head, text="✨ أفلام مقترحة بناءً على اختيارك (AI Recommendations):", font=(THEME["font_family"], 10, "bold"), bg=THEME["surface_card"], fg=THEME["accent_blue"]).pack(anchor="w")

        self.recs_listbox = tk.Listbox(right_col, bg=THEME["bg"], fg="#E5E7EB", font=(THEME["font_family"], 10), relief=tk.FLAT, bd=0, highlightthickness=0, selectbackground=THEME["surface_light"])
        self.recs_listbox.pack(fill=tk.BOTH, expand=True)

    def refresh_movie_list(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()
        selected_genre = self.genre_var.get()

        for m in self.movies:
            if selected_genre != "الكل" and selected_genre not in m["genre"]:
                continue
            if query and query not in m["title"].lower() and query not in m["director"].lower():
                continue

            self.tree.insert("", tk.END, iid=str(m["id"]), values=(m["title"], m["year"], f"⭐ {m['rating']}", m["genre"]))

    def on_movie_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        movie_id = int(sel[0])
        m_idx = next(i for i, m in enumerate(self.movies) if m["id"] == movie_id)
        movie = self.movies[m_idx]
        self.current_movie = movie

        self.lbl_title.config(text=f"🎬 {movie['title']}")
        self.lbl_meta.config(text=f"📅 {movie['year']} | ⭐ {movie['rating']}/10 | 🎥 إخراج: {movie['director']} | 🏷️ {movie['genre']}")
        self.lbl_desc.config(text=movie["description"])

        in_wl = any(w["id"] == movie["id"] for w in self.engine.watchlist)
        self.btn_add_wl.config(
            text="❌ إزالة من قائمة المشاهدة" if in_wl else "➕ إضافة لقائمة المشاهدة",
            bg=THEME["danger"] if in_wl else THEME["success"]
        )

        recs = self.engine.get_recommendations(m_idx, top_n=4)
        self.recs_listbox.delete(0, tk.END)
        for rec_idx, sim_score in recs:
            rec_m = self.movies[rec_idx]
            match_pct = int(sim_score * 100)
            self.recs_listbox.insert(tk.END, f"🔥 {rec_m['title']} ({rec_m['year']}) - تطابق: {match_pct}% | {rec_m['genre']}")

    def on_toggle_watchlist(self):
        if not self.current_movie:
            return
        added = self.engine.toggle_watchlist(self.current_movie)
        self.btn_wl.config(text=f"⭐ قائمة المشاهدة ({len(self.engine.watchlist)})")
        self.btn_add_wl.config(
            text="❌ إزالة من قائمة المشاهدة" if added else "➕ إضافة لقائمة المشاهدة",
            bg=THEME["danger"] if added else THEME["success"]
        )

    def show_watchlist_dialog(self):
        top = tk.Toplevel(self)
        top.title("قائمة المشاهدة")
        top.geometry("450x400")
        top.configure(bg=THEME["surface"])

        tk.Label(top, text="⭐ أفلامك المحفوظة للمشاهدة اللاحقة:", font=(THEME["font_family"], 11, "bold"), bg=THEME["surface"], fg="#FBBF24", pady=10).pack()
        lb = tk.Listbox(top, bg=THEME["bg"], fg="#FFFFFF", font=(THEME["font_family"], 10), relief=tk.FLAT)
        lb.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        for w in self.engine.watchlist:
            lb.insert(tk.END, f"• {w['title']} ({w['year']}) - ⭐ {w['rating']}")
        if not self.engine.watchlist:
            lb.insert(tk.END, "لم تضف أي أفلام لقائمتك بعد.")
