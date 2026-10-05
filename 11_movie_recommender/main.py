#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
مشروع 11: نظام توصية الأفلام السينمائي الذكي (Movie Recommendation System)
نقطة الدخول الرئيسية للبرنامج (Bootstrap)
"""

import sys
import os
import tkinter as tk

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.recommender_engine import MovieRecommendationEngine, get_default_movies
from ui.movie_view import MovieRecommenderView
from ui.theme import THEME


class MovieRecommenderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("نظام توصية الأفلام السينمائي | Movie Recommender")
        self.geometry("980x720")
        self.minsize(880, 620)
        self.configure(bg=THEME["bg"])

        try:
            self.tk.call('tk', 'scaling', 1.25)
        except Exception:
            pass

        movies = get_default_movies()
        self.engine = MovieRecommendationEngine(movies)
        self.view = MovieRecommenderView(self, self.engine)
        self.view.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = MovieRecommenderApp()
    app.mainloop()
