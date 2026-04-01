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
   git clone https://github.com/onkbaonk/Web.git
   cd Web
2. **Buat & Aktifkan Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
4. **Persiapkan Database:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
5. **Jalankan Server:**
   ```bash
   uvicorn core.asgi:application

Web ini dapat diakses secara online di: [url://BELUM_ADA_HOSTING]

Developed by onkbaonk