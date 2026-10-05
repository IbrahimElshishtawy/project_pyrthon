#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 11: نظام توصية الأفلام الذكي (Movie Recommendation System)
يدعم:
- خوارزمية توصية قائمة على المحتوى (Content-Based Filtering) باستخدام TF-IDF وتشابه جيب التمام (Cosine Similarity)
- قاعدة بيانات مدمجة لأشهر الأفلام العالمية مع تفاصيل التصنيف، القصة، التقييم، وسنة الإنتاج
- البحث بالاسم أو الفلترة بالتصنيف (أكشن، خيال علمي، دراما، كوميديا، جريمة، رسوم متحركة)
- عرض التوصيات المشابهة فور اختيار أي فيلم مع نسبة التطابق المئوية (%)
- قائمة المفضلة وقائمة المشاهدة اللاحقة (Watchlist) محفوظة تلقائياً
- واجهة سينمائية حديثة (Cinema Slate) ببطاقات أنيقة
"""

import json
import math
import os
import re
import tkinter as tk
from tkinter import messagebox, ttk


class MovieRecommendationEngine:
    def __init__(self, movies):
        self.movies = movies
        self.vocabulary = {}
        self.idf = {}
        self.tfidf_vectors = []
        self._build_model()

    def _tokenize(self, text):
        clean = re.sub(r'[^\w\s]', ' ', text.lower())
        return [w for w in clean.split() if len(w) > 2]

    def _build_model(self):
        docs = []
        doc_count = len(self.movies)
        df = {}

        for m in self.movies:
            # Combine content features: genre, description, keywords
            content = f"{m['genre']} {m['genre']} {m['description']} {m.get('director', '')}"
            tokens = self._tokenize(content)
            docs.append(tokens)

            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1

        # Build vocabulary & IDF
        vocab_idx = 0
        for token, freq in df.items():
            self.vocabulary[token] = vocab_idx
            self.idf[token] = math.log((doc_count + 1) / (freq + 1)) + 1
            vocab_idx += 1

        # Build TF-IDF vectors
        for tokens in docs:
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1

            vec = {}
            norm_sq = 0.0
            for t, count in tf.items():
                tfidf_val = (count / len(tokens)) * self.idf.get(t, 1.0)
                vec[self.vocabulary[t]] = tfidf_val
                norm_sq += tfidf_val ** 2

            norm = math.sqrt(norm_sq) if norm_sq > 0 else 1.0
            # Normalize vector
            for k in vec:
                vec[k] /= norm
            self.tfidf_vectors.append(vec)

    def get_recommendations(self, movie_idx, top_n=5):
        target_vec = self.tfidf_vectors[movie_idx]
        scores = []

        for idx, vec in enumerate(self.tfidf_vectors):
            if idx == movie_idx:
                continue
            # Cosine similarity between sparse vectors
            dot_product = 0.0
            for term_idx, val in target_vec.items():
                if term_idx in vec:
                    dot_product += val * vec[term_idx]

            scores.append((idx, dot_product))

        # Sort descending
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]


class MovieRecommenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("نظام توصية الأفلام السينمائي | Movie Recommender")
        self.geometry("960x700")
        self.minsize(880, 620)
        self.configure(bg="#0B0F19")

        self.watchlist_file = os.path.join(os.path.dirname(__file__), "watchlist.json")
        self.watchlist = self.load_watchlist()

        self.movies = self.get_movies_dataset()
        self.engine = MovieRecommendationEngine(self.movies)

        self.setup_ui()
        self.refresh_movie_list()

    def get_movies_dataset(self):
        return [
            {"id": 1, "title": "Inception", "year": 2010, "genre": "خيال علمي • إثارة", "rating": "8.8", "director": "Christopher Nolan", "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."},
            {"id": 2, "title": "Interstellar", "year": 2014, "genre": "خيال علمي • دراما", "rating": "8.7", "director": "Christopher Nolan", "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival across distant galaxies."},
            {"id": 3, "title": "The Dark Knight", "year": 2008, "genre": "أكشن • جريمة • إثارة", "rating": "9.0", "director": "Christopher Nolan", "description": "Batman faces the Joker, a criminal mastermind who plunges Gotham City into utter chaos and tests his moral limits."},
            {"id": 4, "title": "Pulp Fiction", "year": 1994, "genre": "جريمة • دراما", "rating": "8.9", "director": "Quentin Tarantino", "description": "The lives of two mob hitmen, a boxer, a gangster and his wife intertwine in four tales of violence and redemption."},
            {"id": 5, "title": "Fight Club", "year": 1999, "genre": "دراما • إثارة", "rating": "8.8", "director": "David Fincher", "description": "An insomniac office worker and a devil-may-care soap maker form an underground fight club that evolves into something much more."},
            {"id": 6, "title": "The Matrix", "year": 1999, "genre": "أكشن • خيال علمي", "rating": "8.7", "director": "The Wachowskis", "description": "A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers."},
            {"id": 7, "title": "Forrest Gump", "year": 1994, "genre": "دراما • رومانسي", "rating": "8.8", "director": "Robert Zemeckis", "description": "The history of the United States from the 1950s to the 70s unfolds from the perspective of an Alabama man with an IQ of 75."},
            {"id": 8, "title": "The Godfather", "year": 1972, "genre": "جريمة • دراما", "rating": "9.2", "director": "Francis Ford Coppola", "description": "The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."},
            {"id": 9, "title": "Spirited Away", "year": 2001, "genre": "رسوم متحركة • مغامرة", "rating": "8.6", "director": "Hayao Miyazaki", "description": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits."},
            {"id": 10, "title": "Spider-Man: Into the Spider-Verse", "year": 2018, "genre": "رسوم متحركة • أكشن • خيال", "rating": "8.4", "director": "Peter Ramsey", "description": "Teen Miles Morales becomes the new Spider-Man and joins other Spider-heroes from parallel dimensions to stop a threat."},
            {"id": 11, "title": "Parasite", "year": 2019, "genre": "دراما • إثارة • كوميديا سوداء", "rating": "8.5", "director": "Bong Joon Ho", "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan."},
            {"id": 12, "title": "Gladiator", "year": 2000, "genre": "أكشن • مغامرة • دراما", "rating": "8.5", "director": "Ridley Scott", "description": "A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery."}
        ]

    def load_watchlist(self):
        if os.path.exists(self.watchlist_file):
            try:
                with open(self.watchlist_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_watchlist(self):
        try:
            with open(self.watchlist_file, "w", encoding="utf-8") as f:
                json.dump(self.watchlist, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def setup_ui(self):
        # Header
        header = tk.Frame(self, bg="#111827", pady=12, padx=20)
        header.pack(fill=tk.X)

        title = tk.Label(
            header,
            text="🎬 نظام توصية الأفلام السينمائي الذكي",
            font=("Segoe UI", 18, "bold"),
            bg="#111827",
            fg="#F59E0B"
        )
        title.pack(side=tk.RIGHT)

        self.btn_show_watchlist = tk.Button(
            header,
            text=f"⭐ قائمة المشاهدة ({len(self.watchlist)})",
            font=("Segoe UI", 10, "bold"),
            bg="#374151",
            fg="#FBBF24",
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.show_watchlist_dialog
        )
        self.btn_show_watchlist.pack(side=tk.LEFT)

        # Body Container
        body = tk.Frame(self, bg="#0B0F19", padx=16, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Search & Filter Toolbar
        tools_frame = tk.Frame(body, bg="#111827", padx=14, pady=10, bd=1, relief=tk.SOLID)
        tools_frame.pack(fill=tk.X, pady=(0, 12))

        # Search Entry
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_movie_list())
        search_entry = tk.Entry(
            tools_frame,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            bg="#1F2937",
            fg="#FFFFFF",
            insertbackground="#F59E0B",
            relief=tk.FLAT
        )
        search_entry.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(10, 6), ipady=3)
        tk.Label(tools_frame, text="🔍 ابحث عن فيلم أو مخرج:", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#E5E7EB").pack(side=tk.RIGHT)

        # Genre Filter
        self.genre_var = tk.StringVar(value="الكل")
        genres = ["الكل", "خيال علمي", "أكشن", "جريمة", "دراما", "رسوم متحركة", "مغامرة"]
        genre_cb = ttk.Combobox(tools_frame, textvariable=self.genre_var, values=genres, state="readonly", width=12)
        genre_cb.pack(side=tk.LEFT, padx=(6, 0))
        genre_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_movie_list())
        tk.Label(tools_frame, text="التصنيف:", font=("Segoe UI", 9), bg="#111827", fg="#9CA3AF").pack(side=tk.LEFT, padx=(10, 2))

        # Split: Left (Movie List), Right (Details & AI Recommendations)
        split = tk.Frame(body, bg="#0B0F19")
        split.pack(fill=tk.BOTH, expand=True)

        # Left Column: Movies Listbox / Treeview
        left_col = tk.Frame(split, bg="#111827", bd=1, relief=tk.SOLID, width=440)
        left_col.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        left_col.pack_propagate(False)

        tk.Label(left_col, text="🎞️ اختر فيلماً تحبه لاستخراج توصيات ذكية:", font=("Segoe UI", 10, "bold"), bg="#111827", fg="#9CA3AF", padx=10, pady=8).pack(anchor="w")

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

        # Right Column: Movie Info & AI Recommendations Card
        self.right_col = tk.Frame(split, bg="#111827", bd=1, relief=tk.SOLID, padx=16, pady=14)
        self.right_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.lbl_selected_title = tk.Label(
            self.right_col,
            text="اختر فيلماً من القائمة",
            font=("Segoe UI", 16, "bold"),
            bg="#111827",
            fg="#F3F4F6",
            anchor="w"
        )
        self.lbl_selected_title.pack(fill=tk.X)

        self.lbl_selected_meta = tk.Label(
            self.right_col,
            text="السنة | التقييم | المخرج",
            font=("Segoe UI", 9),
            bg="#111827",
            fg="#F59E0B",
            anchor="w"
        )
        self.lbl_selected_meta.pack(fill=tk.X, pady=(2, 6))

        self.lbl_selected_desc = tk.Label(
            self.right_col,
            text="حدد فيلماً لعرض القصة وتوصيات الذكاء الاصطناعي المشابهة.",
            font=("Segoe UI", 10),
            bg="#111827",
            fg="#D1D5DB",
            anchor="w",
            justify="left",
            wraplength=380
        )
        self.lbl_selected_desc.pack(fill=tk.X, pady=(0, 10))

        self.btn_add_watchlist = tk.Button(
            self.right_col,
            text="➕ إضافة لقائمة المشاهدة",
            font=("Segoe UI", 9, "bold"),
            bg="#10B981",
            fg="#FFFFFF",
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            command=self.toggle_current_watchlist
        )
        self.btn_add_watchlist.pack(anchor="w", pady=(0, 14))

        # Recommendations Header
        recs_header = tk.Frame(self.right_col, bg="#1F2937", padx=8, pady=4)
        recs_header.pack(fill=tk.X, pady=(0, 6))
        tk.Label(
            recs_header,
            text="✨ أفلام مقترحة بناءً على اختيارك (AI Recommendations):",
            font=("Segoe UI", 10, "bold"),
            bg="#1F2937",
            fg="#60A5FA"
        ).pack(anchor="w")

        # Recommendations listbox
        self.recs_listbox = tk.Listbox(
            self.right_col,
            bg="#0B0F19",
            fg="#E5E7EB",
            font=("Segoe UI", 10),
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0,
            selectbackground="#374151"
        )
        self.recs_listbox.pack(fill=tk.BOTH, expand=True)

        self.current_selected_movie = None

    def refresh_movie_list(self):
        self.tree.delete(*self.tree.get_children())
        query = self.search_var.get().strip().lower()
        selected_genre = self.genre_var.get()

        for m in self.movies:
            if selected_genre != "الكل" and selected_genre not in m["genre"]:
                continue
            if query and query not in m["title"].lower() and query not in m["director"].lower():
                continue

            self.tree.insert(
                "",
                tk.END,
                iid=str(m["id"]),
                values=(
                    m["title"],
                    m["year"],
                    f"⭐ {m['rating']}",
                    m["genre"]
                )
            )

    def on_movie_selected(self, event):
        sel = self.tree.selection()
        if not sel:
            return

        movie_id = int(sel[0])
        m_idx = next(i for i, m in enumerate(self.movies) if m["id"] == movie_id)
        movie = self.movies[m_idx]
        self.current_selected_movie = movie

        self.lbl_selected_title.config(text=f"🎬 {movie['title']}")
        self.lbl_selected_meta.config(text=f"📅 {movie['year']} | ⭐ {movie['rating']}/10 | 🎥 إخراج: {movie['director']} | 🏷️ {movie['genre']}")
        self.lbl_selected_desc.config(text=movie["description"])

        # Check watchlist state
        in_wl = any(w["id"] == movie["id"] for w in self.watchlist)
        self.btn_add_watchlist.config(
            text="❌ إزالة من قائمة المشاهدة" if in_wl else "➕ إضافة لقائمة المشاهدة",
            bg="#EF4444" if in_wl else "#10B981"
        )

        # Get AI recommendations
        recs = self.engine.get_recommendations(m_idx, top_n=4)
        self.recs_listbox.delete(0, tk.END)

        for rec_idx, sim_score in recs:
            rec_movie = self.movies[rec_idx]
            match_pct = int(sim_score * 100)
            self.recs_listbox.insert(
                tk.END,
                f"🔥 {rec_movie['title']} ({rec_movie['year']}) - تطابق: {match_pct}% | {rec_movie['genre']}"
            )

    def toggle_current_watchlist(self):
        if not self.current_selected_movie:
            return
        m = self.current_selected_movie
        in_wl = any(w["id"] == m["id"] for w in self.watchlist)

        if in_wl:
            self.watchlist = [w for w in self.watchlist if w["id"] != m["id"]]
        else:
            self.watchlist.append({"id": m["id"], "title": m["title"], "year": m["year"], "rating": m["rating"]})

        self.save_watchlist()
        self.btn_show_watchlist.config(text=f"⭐ قائمة المشاهدة ({len(self.watchlist)})")
        self.btn_add_watchlist.config(
            text="➕ إضافة لقائمة المشاهدة" if in_wl else "❌ إزالة من قائمة المشاهدة",
            bg="#10B981" if in_wl else "#EF4444"
        )

    def show_watchlist_dialog(self):
        top = tk.Toplevel(self)
        top.title("قائمة أفلامي للمشاهدة")
        top.geometry("450x400")
        top.configure(bg="#111827")

        tk.Label(top, text="⭐ أفلامك المحفوظة للمشاهدة اللاحقة:", font=("Segoe UI", 11, "bold"), bg="#111827", fg="#FBBF24", pady=10).pack()

        lb = tk.Listbox(top, bg="#0B0F19", fg="#FFFFFF", font=("Segoe UI", 10), relief=tk.FLAT)
        lb.pack(fill=tk.BOTH, expand=True, padx=12, pady=6)

        for w in self.watchlist:
            lb.insert(tk.END, f"• {w['title']} ({w['year']}) - ⭐ {w['rating']}")

        if not self.watchlist:
            lb.insert(tk.END, "لم تضف أي أفلام لقائمتك بعد.")


if __name__ == "__main__":
    app = MovieRecommenderApp()
    app.mainloop()
