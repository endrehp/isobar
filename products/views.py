from django.shortcuts import render

def home(request):
    return render(request, 'products/home.html')

def menu(request):
    return render(request, 'products/menu.html')
