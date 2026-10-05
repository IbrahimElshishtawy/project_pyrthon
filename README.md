# 🚀 حزمة مشاريع بايثون الاحترافية الـ 15 (Tkinter GUI Projects Suite)

مجموعة شاملة ومتطورة تضم **15 مشروع بايثون عملي متكامل** بواجهات رسومية فائقة الاحترافية مبنية بـ **Tkinter** معتمدة على مكتبة بايثون القياسية بالكامل (بدون أي تبعيات خارجية معقدة وتعمل على بايثون 3.14 بسلاسة).

تمت إعادة هيكلة كل مشروع بالكامل ليعتمد على **معمارية ملفات قياسية ومنظمة (Clean Modular Architecture)** تفصل طبقة المنطق الحسابي والخدمات (`core/`) عن طبقة واجهة المستخدم والتصميم (`ui/`) مع نقطة دخول موحدة (`main.py`).

---

## 🎛️ بوابة التشغيل السريعة (Master Launcher)

يمكنك تشغيل المنصة الرئيسية التي تمكنك من تصفح وتشغيل أي مشروع بنقرة زر واحدة عبر الأمر:

```bash
python3 launcher.py
```

أو تشغيل أي مشروع بشكل فردي ومستقل تماماً:

```bash
python3 01_advanced_calculator/main.py
python3 06_expense_tracker/main.py
python3 15_data_dashboard/main.py
```

---

## 🏗️ معمارية تنظيم الملفات لكل مشروع (Clean Architecture)

تم تنظيم كل مشروع وفق نموذج التصميم الهيكلي التالي:

```text
اسم_المشروع/
├── core/                   # 🧠 طبقة منطق الأعمال وقواعد البيانات والخدمات (Business Logic)
│   ├── engine.py           # الخوارزميات، المحركات، والخدمات المستقلة تماماً عن الواجهة
│   └── database.py         # التعامل مع التخزين (JSON / SQLite / CSV)
├── ui/                     # 🎨 طبقة التصميم والواجهة الرسومية (Presentation Layer)
│   ├── theme.py            # لوحة الألوان الموحدة (Dark Palette)، الخطوط، والأيقونات
│   ├── components.py       # الرسوم البيانية التفاعلية (Canvas Charts) والمكونات الخاصة
│   └── view.py             # إطارات الشاشة، النماذج، الجداول، والأزرار
└── main.py                 # 🚀 نقطة التشغيل الرئيسية وتجميع المكونات (App Entrypoint)
```

---

## 📁 هيكلية المستودع الكاملة للمشاريع الـ 15

```text
project_pyrthon/
├── launcher.py                         # منصة التشغيل الرسومية الشاملة لجميع المشاريع
│
├── 01_advanced_calculator/             # 1. حاسبة علمية متقدمة
│   ├── core/calc_engine.py
│   ├── ui/theme.py & ui/calc_view.py
│   └── main.py
│
├── 02_number_guessing_game/            # 2. لعبة تخمين الرقم مع التلميحات الحرارية
│   ├── core/game_logic.py
│   ├── ui/theme.py & ui/game_view.py
│   └── main.py
│
├── 03_todo_manager/                    # 3. مدير المهام اليومية مع تصنيفات وحفظ JSON
│   ├── core/task_manager.py
│   ├── ui/theme.py & ui/todo_view.py
│   └── main.py
│
├── 04_password_generator/              # 4. مولد كلمات سر قوية ومقياس إنتروبيا
│   ├── core/generator_logic.py
│   ├── ui/theme.py & ui/password_view.py
│   └── main.py
│
├── 05_rock_paper_scissors/             # 5. لعبة حجر ورقة مقص التفاعلية
│   ├── core/game_rules.py
│   ├── ui/theme.py & ui/game_view.py
│   └── main.py
│
├── 06_expense_tracker/                 # 6. متتبع المصروفات مع رسم بياني Donut وتصدير CSV
│   ├── core/expense_manager.py
│   ├── ui/theme.py, ui/charts.py & ui/expense_view.py
│   └── main.py
│
├── 07_price_scraper/                   # 7. كاشط ومتتبع أسعار المنتجات
│   ├── core/scraper_service.py
│   ├── ui/theme.py & ui/scraper_view.py
│   └── main.py
│
├── 08_telegram_bot_manager/            # 8. لوحة تحكم ومحاكي بوت تيليجرام
│   ├── core/bot_service.py
│   ├── ui/theme.py & ui/bot_view.py
│   └── main.py
│
├── 09_file_organizer/                  # 9. منظم الملفات التلقائي مع المعاينة والتراجع
│   ├── core/organizer_engine.py
│   ├── ui/theme.py & ui/organizer_view.py
│   └── main.py
│
├── 10_url_shortener/                   # 10. مختصر الروابط مع SQLite وسيرفر محلي
│   ├── core/database.py & core/redirect_server.py
│   ├── ui/theme.py & ui/shortener_view.py
│   └── main.py
│
├── 11_movie_recommender/               # 11. نظام توصية الأفلام (TF-IDF & Cosine Similarity)
│   ├── core/recommender_engine.py
│   ├── ui/theme.py & ui/movie_view.py
│   └── main.py
│
├── 12_sentiment_analyzer/              # 12. محلل مشاعر النصوص مع عداد سرعة المشاعر
│   ├── core/sentiment_engine.py
│   ├── ui/theme.py, ui/gauge_canvas.py & ui/sentiment_view.py
│   └── main.py
│
├── 13_chat_application/                # 13. تطبيق دردشة فورية متعدد الغرف (Sockets)
│   ├── core/chat_network.py
│   ├── ui/theme.py & ui/chat_view.py
│   └── main.py
│
├── 14_face_attendance/                 # 14. منظومة الحضور بالبصمة الوجهية وسجل CSV
│   ├── core/attendance_service.py
│   ├── ui/theme.py, ui/scanner_canvas.py & ui/attendance_view.py
│   └── main.py
│
└── 15_data_dashboard/                  # 15. لوحة مؤشرات وتحليل بيانات المبيعات التنفيذية
    ├── core/analytics_service.py
    ├── ui/theme.py, ui/charts.py & ui/dashboard_view.py
    └── main.py
```

---

## 🎨 ملامح التصميم الاحترافي للواجهات (UI/UX Highlights)

- **نظام الألوان الداكن الحديث (Modern Sleek Dark Mode)**: باليت ألوان متناسق ومريح للعين (`#0F172A`, `#1E293B`, `#38BDF8`, `#10B981`, `#F59E0B`).
- **رسومات بيانية أصلية على Canvas**: رسوم بيانية تفاعلية (Donut Charts, Bar Charts, Speedometer Gauges, Biometric HUD) مبنية بمرونة عالية دون الحاجة لمكتبات طرف ثالث.
- **توافق مع الشاشات عالية الدقة (High-DPI Scaling)**: ضبط تلقائي للخطوط والأبعاد لمنع التشويش.
- **تعدد المهام والخيوط (Multi-threading)**: العمليات الطويلة (مثل الكشط، السيرفرات، والشبكات) تعمل في الخلفية دون تجمد الواجهة.
