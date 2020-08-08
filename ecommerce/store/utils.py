import json
from .models import  *


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', {}))
    except:
        cart = {}
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    item_count = order['get_cart_items']

    for i in cart:

        item_count += cart[i]['quantity']
        try:
            product = Product.objects.get(id=i)
        except:
            continue
        total = (product.price * cart[i]['quantity'])
        order['get_cart_total'] += total
        order['get_cart_items'] += cart[i]['quantity']

        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'imageUrl': product.imageUrl
            },
            'quantity': cart[i]['quantity'],
            'get_total': total
        }
        items.append(item)

        if not product.digital:
            order['shipping'] = True
    return {'itemCount': item_count, 'order': order, 'items': items}


def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        item_count = order.get_cart_items
    else:
        cookie_data = cookie_cart(request)
        items = cookie_data['items']
        item_count = cookie_data['itemCount']
        order = cookie_data['order']

    return {'item_count': item_count, 'order': order, 'items': items}


def guest_order(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookie_data = cookie_cart(request)
    items = cookie_data['items']

    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return order, customer