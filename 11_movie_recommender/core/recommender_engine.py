# -*- coding: utf-8 -*-
"""
محرك التوصيات السينمائية المعتمد على المحتوى (TF-IDF & Cosine Similarity)
"""

import json
import math
import os
import re


class MovieRecommendationEngine:
    def __init__(self, movies, watchlist_path=None):
        self.movies = movies
        self.watchlist_path = watchlist_path or os.path.join(os.path.dirname(__file__), "..", "watchlist.json")
        self.watchlist = self.load_watchlist()

        self.vocabulary = {}
        self.idf = {}
        self.tfidf_vectors = []
        self._build_model()

    def load_watchlist(self):
        if os.path.exists(self.watchlist_path):
            try:
                with open(self.watchlist_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def save_watchlist(self):
        try:
            with open(self.watchlist_path, "w", encoding="utf-8") as f:
                json.dump(self.watchlist, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def toggle_watchlist(self, movie):
        in_wl = any(w["id"] == movie["id"] for w in self.watchlist)
        if in_wl:
            self.watchlist = [w for w in self.watchlist if w["id"] != movie["id"]]
            added = False
        else:
            self.watchlist.append({
                "id": movie["id"],
                "title": movie["title"],
                "year": movie["year"],
                "rating": movie["rating"]
            })
            added = True
        self.save_watchlist()
        return added

    def _tokenize(self, text):
        clean = re.sub(r'[^\w\s]', ' ', text.lower())
        return [w for w in clean.split() if len(w) > 2]

    def _build_model(self):
        docs = []
        doc_count = len(self.movies)
        df = {}

        for m in self.movies:
            content = f"{m['genre']} {m['genre']} {m['description']} {m.get('director', '')}"
            tokens = self._tokenize(content)
            docs.append(tokens)

            unique_tokens = set(tokens)
            for t in unique_tokens:
                df[t] = df.get(t, 0) + 1

        vocab_idx = 0
        for token, freq in df.items():
            self.vocabulary[token] = vocab_idx
            self.idf[token] = math.log((doc_count + 1) / (freq + 1)) + 1
            vocab_idx += 1

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
            for k in vec:
                vec[k] /= norm
            self.tfidf_vectors.append(vec)

    def get_recommendations(self, movie_idx, top_n=4):
        target_vec = self.tfidf_vectors[movie_idx]
        scores = []

        for idx, vec in enumerate(self.tfidf_vectors):
            if idx == movie_idx:
                continue
            dot = 0.0
            for term_idx, val in target_vec.items():
                if term_idx in vec:
                    dot += val * vec[term_idx]
            scores.append((idx, dot))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]


def get_default_movies():
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
