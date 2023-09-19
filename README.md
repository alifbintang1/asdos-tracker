# Tugas 3
## Implementasi
### Membuat Input Form
Membuat `forms.py` pada direktori APP (dalam hal ini adalah `main`) dengan isi:
```python
from django.forms import ModelForm
from main.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'description']
```
Setelah itu, saya membuat fungsi `create_item` untuk membuat formulir yang dapat secara otomatis menambahkan data produk yang disubmit pada `create_item.html`
```python
def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)
```
Lalu, saya membuat file `create_item.html` yang diletakkan di direktori `templates`, file ini adalah tampilan form kepada user, dan user dapat memasukkan data yang diinginkan
```html
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Item</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Item"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```

Tidak lupa, saya tambahkan path nya pada `urls.py` di direktori `main`
```python
path('create-product', create_item, name='create_item'),
```

### Menampilkan Objek yang Ditambahkan (dalam Format HTML, XML, JSON, XML by ID, dan JSON by ID)
#### 1. HTML
Karena dalam pengerjaan ini saya ingin menampilkan objeknya pada halaman utama, maka saya perlu memodifikasi fungsi `show_main` pada `views.py` agar data produk dapat ditampilkan.
```python
def show_main(request):
    items = Item.objects.all()
    context = {
        'name': 'Alif Bintang Elfandra',
        'class': 'PBP B',
        'items': items, # Modifikasi di sini
    }

    return render(request, "main.html", context)
```
Saya juga perlu melakukan sedikit modifikasi pada `main.html` untuk menampilkan objeknya.
```html
...
<!-- Untuk menampilkan tabel -->
<table>
    <tr>
        <th>Name</th>
        <th>Amount</th>
        <th>Description</th>
    
    </tr>

    {% comment %} Berikut cara memperlihatkan data produk di bawah baris ini {% endcomment %}

    {% for item in items %}
        <tr>
            <td>{{item.name}}</td>
            <td>{{item.amount}}</td>
            <td>{{item.description}}</td>
            
        </tr>
    {% endfor %}
</table>

<br />

<!-- Untuk button Add New Item -->
<a href="{% url 'main:create_item' %}">
    <button>
        Add New Item
    </button>
</a>
```


#### 2. XML dan JSON
Saya menambahkan fungsi `show_xml` dan `show_json` yang akan return HttpResponse berisi data yang sudah diserialize menjadi XML dan JSON.
```python
def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

#### 3. XML dan JSON (by ID)
Untuk ini, mirip seperti yang nomor 2, hanya saja sekarang saya hanya akan menampilkan barang sesuai ID saja.
```python
def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```


### Membuat _Routing_ URL
Untuk setiap fungsi pada `views.py` yang ditambahkan, saya perlu menambahkan path nya pada `urls.py`. Hasil akhirnya, file `urls.py` pada direktori `main` akan berisi:
```python
from django.urls import path
from main.views import show_main, create_item, show_xml, show_json, show_xml_by_id, show_json_by_id 

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_item, name='create_item'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
]
```

## Perbedaan Form POST dan GET
Perbedaan utamanya adalah terletak pada URL-nya.
Pada GET, data/variabel akan ditampilkan pada URL, sebaliknya pada POST, data/variabel tidak akan ditampilkan di URL.

GET tidak cocok bila digunakan untuk mengirim data-data penting, contohnya seperti password. Namun, user dapat dengan mudah memasukkan variabel baru, jadi cocok untuk mengirim data-data yang tidal terlalu penting/tidak rahasia.

POST cenderung lebih aman, dan dapat digunakan untuk mengirim data-data penting. Panjang string URL pun tidak dibatasi. Namun, POST kurang efisien bila data yang dikirim adalah data-data yang tidak penting.
## Perbedaan XML, JSON, dan HTML dalam Pengiriman Data
XML (eXtensible Markup Language) menggunakan sintaks berbasis tag (mirip seperti HTML). Ini memungkinkan untuk mendefinisikan struktur data yang sangat fleksibel dan kompleks, tetapi jadi lebih sulit dibaca oleh manusia. XML dirancang untuk menjadi format data yang digunakan oleh komputer dan aplikasi, bukan untuk keterbacaan manusia. 

HTML (Hypertext Markup Language) adalah bahasa yang digunakan untuk membangun tampilan web dan memiliki tujuan utama untuk mengorganisasi dan menampilkan konten di browser. Ini memiliki struktur dasar yang berbeda dan **biasanya tidak digunakan untuk pengiriman data** dalam konteks yang sama seperti XML atau JSON. HTML digunakan untuk tujuan yang berbeda dan memiliki fokus utama pada tampilan dan interaksi dengan pengguna.

JSON (JavaScript Object Notation) adalah adalah format data yang digunakan untuk mengirim dan menyimpan informasi dalam bentuk teks yang mudah dibaca oleh manusia dan mudah diproses oleh komputer. JSON umum digunakan dalam pengembangan web dan aplikasi, khususnya dalam pertukaran data antara browser dan server, karena komunikasi web umumnya berbasis JavaScript.


## Pentingnya JSON dalam Pertukaran Data antara Aplikasi Web Modern
* JSON menggunakan sintaks yang lebih sederhana dan mudah dibaca oleh manusia, menggunakan struktur List dan Dictionary pada Python.

* JSON memiliki overhead (jumlah karakter) yang lebih kecil dibandingkan dengan XML dan HTML, sehingga memerlukan lebih sedikit sumber daya untuk mengurai data

* JSON  didukung untuk mengurai dan menghasilkan data oleh banyak bahasa pemrograman. Ini memungkinkan aplikasi yang ditulis dalam bahasa yang berbeda untuk berkomunikasi dengan mudah dan mempertukarkan data dengan format yang sama.

## Screenshot Postman
### 1. HTML
![Alt text](images/data_html.jpg)
### 2. JSON
![Alt text](images/json_without_id.jpg)
### 3. JSON by ID
![Alt text](images/json_with_id.jpg)
### 4. XML
![Alt text](images/xml_without_id.jpg)
### 5. XML by ID
![Alt text](images/xml_with_id.jpg)




# Tugas 2
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
Fungsi _virtual environment_ adalah untuk memisahkan _packages_ dan _dependencies_ untuk setiap proyek kita, sehingga setiap proyek kita dapat menggunakan paket _Python_ yang berbeda-beda. Kita sebenarnya bisa saja membuat proyek tanpa _virtual environment_, tetapi akan sangat berisiko. Tanpa virtual environment, semua paket Python yang saya instal akan berada dalam lingkungan Python global di sistem saya. Ini dapat menyebabkan konflik jika dua proyek berbeda memerlukan versi yang berbeda dari paket yang sama. Dengan virtual environment, saya dapat mengisolasi dependensi untuk setiap proyek, mencegah konflik tersebut.

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
