# Asdos Tracker
Aplikasi Pencatat Log Asdos

https://asdostracker.adaptable.app/main

## Implementasi
Sebelum memulai, perlu diperhatikan bahwa semua perintah yang dijalankan di _command prompt_ harus berada di direktori utama proyek.
### 1. Membuat proyek Django baru
Saya membuat direktori baru bernama `asdos_tracker`, lalu menambahkan berkas `requirements.txt` di dalam direktori tersebut yang berisi:
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```
Berkas itu berisi _dependencies_ yang akan digunakan. Sebelum memasang _dependencies_, saya membuat _virtual environment_ dengan perintah `python -m venv env` dan mengaktifkannya dengan perintah `env\Scripts\activate.bat`.
Lalu, saya memasang _dependencies_ dengan perintah `pip install -r requirements.txt`.
Terakhir, untuk membuat proyek baru, jalankan perintah `django-admin startproject asdos-tracker .`. Perintah itu akan membuat direktori proyek baru (beserta dengan berkas-berkas yang dibutuhkan) di dalam direktori utama saya.

### 2. Membuat aplikasi _main_ pada proyek tersebut
Jalankan perintah `python manage.py startapp main` untuk membuat aplikasi dengan nama _main_. Lalu, setiap saya menambahkan aplikasi, saya harus mendaftarkan aplikasinya ke dalam proyek. Caranya adalah dengan membuka berkas `settings.py` di dalam direktori proyek, lalu memodifikasi di variabel `INSTALLED_APPS`.
```
INSTALLED_APPS = [
    ...,
    'main',
    ...
]
```

### 3. Melakukan _routing_ agar dapat menjalankan aplikasi

