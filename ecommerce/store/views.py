import datetime
import json

from django.shortcuts import render
from django.http import JsonResponse
from . models import *
from .utils import cookie_cart, cart_data, guest_order


# Create your views here.


def store(request):
    data = cart_data(request)
    item_count = data['item_count']
    products = Product.objects.all()
    context = {'products': products, 'itemCount': item_count}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    item_count = data['item_count']

    context = {'items': items, 'order': order, 'itemCount': item_count}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cart_data(request)
    items = data['items']
    order = data['order']
    item_count = data['item_count']
    context = {'items': items, 'order': order, 'itemCount': item_count}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    print(request)
    data = json.loads(request.body)
    action = data['action']
    product_id = data['productId']
    customer = request.user.customer
    product = Product.objects.get(id=product_id)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity < 1:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.utcnow().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        order, customer = guest_order(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode']

        )
    return JsonResponse('Payment complete', safe=False)