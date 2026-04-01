# 🚀 Web Project - Django & WebSockets

Proyek aplikasi web berbasis **Django** yang mendukung fitur real-time chat menggunakan **WebSockets**. Dikembangkan menggunakan lingkungan **Termux** di perangkat mobile.

## 🛠️ Fitur Utama
* **User Authentication**: Sistem login, registrasi, dan profil user.
* **Real-time Chat**: Komunikasi instan antar pengguna menggunakan Django Channels & Daphne.
* **Blog & Forum**: Sistem konten dengan kategori dan komentar (Cusdis).
* **Interactive Features**: Tombol "Like" (Lyket API) dan notifikasi.
* **Production Ready**: Konfigurasi siap hosting (WhiteNoise, Gunicorn/Daphne).

## 📦 Teknologi yang Digunakan
* **Framework**: Django 4.x / 5.x
* **Real-time**: Django Channels & WebSockets
* **Database**: SQLite (Development) / PostgreSQL (Production)
* **Frontend**: HTML5, CSS (Dark Mode optimized), JavaScript
* **Server/Hosting**: Daphne (ASGI), Railway/Render

## 🚀 Cara Menjalankan di Lokal (Termux)

1. **Clone Repository:**
   ```bash
   git clone [https://github.com/onkbaonk/Web.git](https://github.com/onkbaonk/Web.git)
   cd Web
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   uvicorn core.asgi:application
