from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Purchase
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required



def home(request):
    return render(request, 'products/home.html')

def menu(request):
    products = Product.objects
    beer = products.filter(category='beer')
    drinks = products.filter(category='drink')
    shots = products.filter(category='shot')
    other = products.filter(category='other')
    #print(beer[1].title)
    return render(request, 'products/menu.html', {'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other})

@staff_member_required
def create_product(request):
    return render(request, 'products/create_product.html')

def product_info(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)
    
    return render(request, 'products/product_info.html', {'product': product})

@staff_member_required
def start_event(request):
    if request.method == 'POST':
        
        return redirect('event')
    else:
        return render(request, 'products/start_event.html')

@staff_member_required
def event(request):
    if request.method == 'POST':
        if request.POST['username']:
            try:
                user = User.objects.get(username=request.POST['username'])
                print(user)
                print(user.profile.saldo)
                #product = Product.objects.get(title=request.POST['name'])
                products = request.POST.getlist('title')
                prices = request.POST.getlist('price')
                total = sum(list(map(int, prices)))
                
                #withdraw
                
                user.profile.add_money(-total)
                user.save()
                print('after withdrawal:')
                print(user.profile.saldo)
                #register purchases
                for i in range(len(products)):
                    purchase = Purchase(user=user.username, product=products[i], amount=int(prices[i]))
                    purchase.save()
                
                return render(request, 'products/payment.html', {'user': user})
            except:
                print('exception')
                products = Product.objects
                beer = products.filter(category='beer')
                drinks = products.filter(category='drink')
                shots = products.filter(category='shot')
                other = products.filter(category='other')
                #print(beer[1].title)
                return render(request, 'products/event.html', {'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'error': 'noe gikk galt'})

    else:
        products = Product.objects
        beer = products.filter(category='beer')
        drinks = products.filter(category='drink')
        shots = products.filter(category='shot')
        other = products.filter(category='other')
        #print(beer[1].title)
        return render(request, 'products/event.html', {'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other})

    
def payment(request):
    return render(request, 'products/payment.html')

@staff_member_required
def history(request):
    
    purchases = Purchase.objects.all()
    
    return render(request, 'products/history.html', {'purchases': purchases})

























