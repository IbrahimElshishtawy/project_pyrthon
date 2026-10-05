# -*- coding: utf-8 -*-
"""
محرك فحص وتنظيم الملفات التلقائي (File Organization Engine)
"""

import os
import shutil


class FileOrganizerEngine:
    CATEGORIES = {
        "الصور (Images)": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
        "المستندات (Documents)": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
        "الفيديوهات (Videos)": [".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm"],
        "الصوتيات (Audio)": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
        "الملفات المضغوطة (Archives)": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "الأكواد والبرمجة (Code)": [".py", ".js", ".html", ".css", ".json", ".dart", ".cpp", ".java", ".sql"],
        "أخرى (Other)": []
    }

    def __init__(self):
        self.planned_moves = []
        self.undo_history = []

    def get_category_for_ext(self, ext):
        ext = ext.lower()
        for cat_name, ext_list in self.CATEGORIES.items():
            if ext in ext_list:
                return cat_name
        return "أخرى (Other)"

    @staticmethod
    def format_size(size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"

    def analyze_folder(self, folder_path):
        self.planned_moves.clear()
        if not os.path.isdir(folder_path):
            raise ValueError("المسار ليس مجلداً صالحاً")

        files_info = []
        for item in os.listdir(folder_path):
            full_path = os.path.join(folder_path, item)
            if os.path.isdir(full_path):
                continue

            name, ext = os.path.splitext(item)
            cat = self.get_category_for_ext(ext)
            folder_name = cat.split(" ")[0]
            target_dir = os.path.join(folder_path, folder_name)
            target_path = os.path.join(target_dir, item)

            try:
                sz = os.path.getsize(full_path)
                sz_str = self.format_size(sz)
            except Exception:
                sz_str = "--"

            self.planned_moves.append((full_path, target_path, cat, target_dir))
            files_info.append({
                "name": item,
                "ext": ext or "بدون",
                "size": sz_str,
                "category": cat,
                "target_folder": folder_name
            })

        return files_info

    def execute_organization(self):
        executed = []
        errors = 0

        for src, dest, cat, target_dir in self.planned_moves:
            try:
                os.makedirs(target_dir, exist_ok=True)
                final_dest = dest
                if os.path.exists(final_dest) and final_dest != src:
                    base, ext = os.path.splitext(dest)
                    final_dest = f"{base}_new{ext}"

                shutil.move(src, final_dest)
                executed.append((final_dest, src))
            except Exception:
                errors += 1

        self.undo_history = executed
        self.planned_moves.clear()
        return len(executed), errors

    def undo_organization(self):
        reverted = 0
        for current_path, original_path in self.undo_history:
            try:
                if os.path.exists(current_path):
                    shutil.move(current_path, original_path)
                    reverted += 1
            except Exception:
                pass
        self.undo_history.clear()
        return reverted
