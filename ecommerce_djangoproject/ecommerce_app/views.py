from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .utils import cart_data, guest_order
import json
import datetime


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')

    context = {'form': form}
    return render(request, 'ecommerce_app/register.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'ecommerce_app/login.html')


def logout_page(request):
    logout(request)
    return redirect('/')


def store(request):
    data = cart_data(request)
    cart_items = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cart_items}
    return render(request, 'ecommerce_app/store.html', context)


def cart(request):
    data = cart_data(request)
    cart_items = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'ecommerce_app/cart.html', context)


def checkout(request):
    data = cart_data(request)
    cart_items = data['cartItems']
    items = data['items']
    order = data['order']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'ecommerce_app/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer,
                                                 complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guest_order(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment completed', safe=False)
