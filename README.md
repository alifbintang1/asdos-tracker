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

### 2. Membuat aplikasi `main` pada proyek tersebut
Jalankan perintah `python manage.py startapp main` untuk membuat aplikasi dengan nama `main`. Lalu, setiap saya menambahkan aplikasi, saya harus mendaftarkan aplikasinya ke dalam proyek. Caranya adalah dengan membuka berkas `settings.py` di dalam direktori proyek, lalu memodifikasi di variabel `INSTALLED_APPS`.
```python
INSTALLED_APPS = [
    ...,
    'main',
    ...
]
```

### 3. Melakukan _routing_ agar dapat menjalankan aplikasi
Saya membuat `urls.py` di dalam direktori `main` yang berisi:
```python
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```
Berkas ini berguna untuk mengatur rute URL yang terkait pada aplikasi `main`.
Untuk mengimport rute URL dari aplikasi `main` ke dalam `urls.py` proyek, maka buka berkas `urls.py` yang ada di dalam direktori proyek, lalu modifikasi _code_-nya menjadi seperti ini:
```python
...
from django.urls import path, include
...
urlpatterns = [
    ...
    path('main/', include('main.urls')),
    ...
]
```

### 4. Membuat model pada aplikasi `main`
Saya membuka `models.py` yang ada di direktori aplikasi, lalu mengisinya dengan _code_ berikut:
```python
from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
```
Nama model saya adalah _Item_ yang mempunyai atribut-atribut _name, amount,_ dan _description_. Setiap atribut/_field_ memiliki tipe data yang sesuai, yaitu _CharField, IntegerField,_ dan _TextField_. Lalu, setiap saya mengubah model, saya melakukan migrasi model untuk melacak perubahan pada model basis data saya. Hal itu dilakukan dengan cara menjalankan perintah `python manage.py makemigrations`, setelah itu `python manage.py migrate`.

### 5. Membuat fungsi pada `views.py`
Untuk menentukan tampilan apa yang akan saya lihat di `http://localhost:8000/main`, saya membuat direktori `templates` pada direktori aplikasi `main`. Di dalam direktori tersebut, saya menambahkan berkas `main.html` berisi _HTML code_ yang ingin saya tampilkan. Pada `views.py`, saya dapat mengembalikan `main.html` tesebut dengan memodifikasi _code_ menjadi seperti:
```python
from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Alif Bintang Elfandra',
        'class': 'PBP B'
    }
    return render(request, "main.html", context)
```

### 6. Melakukan _deployment_
Pada adaptable, pilih opsi _deploy a new app_. Karena saya ingin men-_deploy_ _repository_ `asdos-tracker`, maka saya memilih _repository_ tersebut. Pilih _Python App Template_ sebagai _template deployment_. Selanjutnya adalah opsi tipe _database_, pilih PostgreSQL. Sesuaikan versi python dengan versi lokal. Dan masukan `python manage.py migrate && gunicorn asdos_tracker.wsgi` pada _Start Command_. Tentukan nama applikasi dan checklist _HTTP Listener on PORT_.

## Bagan
![Alt text](images/bagan_django.png)
_Client_ meminta untuk membuka suatu situs kepada _browser_, yang akan mengirimkan HTTP _request_, lalu diteruskan ke sistem _routing_ dan mencari pola URL yang sesuai dengan permintaan _client_. Django akan memanggil fungsi yang terkait dalam berkas `views.py` yang telah terhubung dengan URL tersebut. `views.py` akan mengambil data yang dibutuhkan pada `models.py`. Setelah itu, `views.py` akan mengirimkan _webpage_ dalam bentuk HTML yang terdapat pada direktori `templates`. Terakhir, HTTP _request_ akan dikembalikan oleh view menjadi HTTP _response_ berupa HTML _page_.

## Virtual Environment
Fungsi _virtual environment_ adalah untuk memisahkan _packages_ dan _dependencies_ untuk setiap proyek kita, sehingga setiap proyek kita dapat menggunakan paket _Python_ yang berbeda-beda. Kita sebenarnya bisa saja membuat proyek tanpa _virtual environment_, tetapi akan sangat berisiko. Tanpa virtual environment, semua paket Python yang saya instal akan berada dalam lingkungan Python global di sistem Anda. Ini dapat menyebabkan konflik jika dua proyek berbeda memerlukan versi yang berbeda dari paket yang sama. Dengan virtual environment, Anda dapat mengisolasi dependensi untuk setiap proyek, mencegah konflik tersebut.

## MVC, MVT, MVVM
Setiap pola ini memiliki pendekatan yang berbeda dalam memisahkan komponen aplikasi dan memfasilitasi pengembangan dan pemeliharaan aplikasi yang lebih baik. Pemilihan pola tergantung pada jenis aplikasi yang dikembangkan, teknologi yang digunakan, dan preferensi pengembang.
### 1. MVC (Model-View-Controller)
* Model: Ini mewakili data dan logika bisnis aplikasi.
* View: Ini bertanggung jawab untuk menampilkan informasi kepada pengguna dan menerima input dari mereka.
* Controller: Ini bertindak sebagai penghubung antara Model dan View. Ini mengatur alur kontrol, mengolah input dari pengguna, dan memutuskan bagaimana meresponsnya.

Pada arsitektur MVC, Model dan View biasanya tidak mengetahui satu sama lain secara langsung, dan komunikasi antara keduanya diatur melalui Controller. Ini adalah pola arsitektur yang umum digunakan dalam pengembangan aplikasi web tradisional.
### 2. MVT (Model-View-Template)
* Model: Mirip dengan MVC, ini mewakili data dan logika bisnis aplikasi.
* View: Ini adalah bagian yang bertanggung jawab untuk menampilkan data, tetapi dalam konteks Django, yang merupakan framework web Python yang menggunakan pola MVT, View lebih mirip dengan Controller dalam pola MVC. Ini mengatur alur kontrol dan menentukan apa yang harus ditampilkan kepada pengguna.
* Template: Ini adalah bagian yang menangani tampilan HTML. Template mengambil data dari Model dan menggabungkannya dengan HTML untuk membuat tampilan yang akhir kepada pengguna.

Pola MVT digunakan khususnya dalam pengembangan web dengan framework Django, yang secara konseptual mirip dengan pola MVC, tetapi dengan istilah yang sedikit berbeda.
### 3. MVVM (Model-View-ViewModel)
* Model: Seperti dalam pola-pola lain, Model mewakili data dan logika bisnis aplikasi.
* View: Ini bertanggung jawab untuk menampilkan informasi kepada pengguna.
* ViewModel: Ini berfungsi sebagai perantara antara Model dan View. ViewModel berisi logika presentasi dan mengubah data Model menjadi format yang lebih sesuai untuk ditampilkan oleh View. ViewModel juga mengelola input dari pengguna dan mengirimkannya ke Model jika diperlukan.

MVVM adalah pola arsitektur yang umum digunakan dalam pengembangan aplikasi berbasis antarmuka pengguna (UI), terutama dalam aplikasi yang menggunakan teknologi seperti WPF (Windows Presentation Foundation) atau dalam pengembangan aplikasi mobile menggunakan kerangka kerja seperti Xamarin.
