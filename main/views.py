from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseRedirect
from main.forms import ItemForm
from django.urls import reverse
from main.models import Item
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Sum
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def create_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_item = Item(name=name, amount=amount, description=description, user=user)
        new_item.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)

@csrf_exempt
def delete_item_ajax(request,id):
    # print("DELETE1")
    if request.method == 'DELETE':
        # print("DELETE2")
        data = Item.objects.get(pk=id)
        data.delete()

        return HttpResponse(b"DELETE", status=201)

    return HttpResponseNotFound()

def delete_item(request, id):
    data = Item.objects.get(pk=id)
    data.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def add_amount(request, id):
    data = Item.objects.get(pk=id)
    data.amount+=1
    data.save()
    return HttpResponseRedirect(reverse('main:show_main'))

def get_item_json(request):
    items = Item.objects.filter(user = request.user)
    
    return HttpResponse(serializers.serialize('json', items))

# Create your views here.
def edit_item(request, id):
    # Get product berdasarkan ID
    item = Item.objects.get(pk = id)

    # Set product sebagai instance dari form
    form = ItemForm(request.POST or None, instance=item)

    if form.is_valid() and request.method == "POST":
        # Simpan form dan kembali ke halaman awal
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_item.html", context)
 

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main")) 
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)

def register(request):
    form = UserCreationForm()
    # print(request.POST)
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def get_total_items(request):
    items = Item.objects.filter(user = request.user)

    items_total = 0
    if(len(items) != 0):
        for x in items:
            items_total += x.amount

    return HttpResponse(items_total)

    

@login_required(login_url='/login')
def show_main(request):
    items = Item.objects.filter(user = request.user)
    # jumlah item
    jumlah_item = items.count()

    # print("ITEMMMMMMMMMMMMMMMMMMMMMSSSSSSSSSSSSSSSSSSS", type(items))
    # jumlah barang
    items_total=0
    if(len(items) != 0):
        for x in items:
            items_total += x.amount

    # if(len(items)==0):
    #     items_total = 0
    # else:
    #     items_total = sum([x.amount for x in items])

    # item akhir
    last_items = items.last()

    # items
    if(items.count()!=0):
        items = items[:items.count()-1]

    context = {
        'name': request.user.username,
        'class': 'PBP B',
        'items': items,
        'last_items': last_items,
        'jenis_items':jumlah_item,
        'total_items':items_total,
        'last_login': request.COOKIES['last_login'],
    }
    # print(type(items))

    return render(request, "main.html", context)

def sub_amount(request, id):
    data = Item.objects.get(pk=id)
    data.amount-=1
    if(data.amount==0):
        data.delete()
        return HttpResponseRedirect(reverse('main:show_main'))
    data.save()
    return HttpResponseRedirect(reverse('main:show_main'))

