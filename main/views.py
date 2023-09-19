from django.shortcuts import render
from django.http import HttpResponseRedirect
from main.forms import ItemForm
from django.urls import reverse
from main.models import Item
from django.http import HttpResponse
from django.core import serializers
from django.db.models import Sum

# Create your views here.
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

def show_main(request):
    items = Item.objects.all()
    context = {
        'name': 'Alif Bintang Elfandra',
        'class': 'PBP B',
        'items': items,
        'jenis_items':len(items),
        'total_items':hitung_jumlah(),
    }
    print(type(items))

    return render(request, "main.html", context)

def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)

def hitung_jumlah():
    total_amount = Item.objects.aggregate(Sum('amount'))['amount__sum']
    if(total_amount is None):
        total_amount = 0
    return total_amount
