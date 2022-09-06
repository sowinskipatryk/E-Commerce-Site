from django.shortcuts import render


def store(request):
    return render(request, 'ecommerce_app/store.html')


def cart(request):
    return render(request, 'ecommerce_app/cart.html')


def checkout(request):
    return render(request, 'ecommerce_app/checkout.html')
