from django.shortcuts import render
from .models import Product, Contact,Orders,OrderUpdate
from math import ceil
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
from django.http import HttpResponse

def index(request):


    allProds = []
    catprods = Product.objects.values('catagory', 'id')
    cats = {item['catagory'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(catagory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds':allProds}
    return render(request, 'shop/index.html', params)

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    if request.method =="POST":
        print(request)
        name=request.POST.get('name','')
        phone = request.POST.get('phone', '')
        email=request.POST.get('email','')

        des = request.POST.get('des','')
        print(name ,phone ,email,des)
        contact=Contact(name=name , phone=phone, email = email  , des = des)
        contact.save()





    return render(request, 'shop/contact.html')
def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.des.lower() or query in item.Product_name.lower() or query in item.catagory.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('catagory', 'id')
    cats = {item['catagory'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(catagory=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)




def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({"status":"success", "updates": updates, "itemsJson": order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shop/tracker.html')







def productview(request, myid):
    # Fetch the product using the id
    product = Product.objects.filter(id=myid)


    return render(request, 'shop/productview.html', {'product':product[0]})

def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Orders(items_json=items_json, name=name, email=email, address=address, city=city, state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        update =  OrderUpdate(order_id = order.order_id, update_desc="this order has been placed")
        update.save()
        thank = True
        id = order.order_id
        #request pytm to transfer the  amount to your account alter payment by user
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})

    return render(request, 'shop/checkout.html')














