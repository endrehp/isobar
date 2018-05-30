from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Purchase, Event
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required



def home(request):
    try:
        event = Event.objects.get(active=True)
        print(event)
        if event is not None:
            return render(request, 'products/home.html', {'event': event})

        else:
            return render(request, 'products/home.html', {'event': event})
    except:
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
        
        event = Event(title=request.POST['title'], active=True)
        event.save()
        
        products = Product.objects
        beer = products.filter(category='beer')
        drinks = products.filter(category='drink')
        shots = products.filter(category='shot')
        other = products.filter(category='other')
        #print(beer[1].title)
        return render(request, 'products/event.html', {'event': event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other})
        
    else:
        return render(request, 'products/start_event.html')
    
def quit_event(request):
    try:
        event = Event.objects.get(active=True)
        print('hentet event:')
        print(event.title)
        event.active = False
        print('avsluttet')
        event.save()
        return redirect('home')
    except:
        return redirect('home')

@staff_member_required
def event(request):
    
    try:
        event = Event.objects.get(active=True)
    except:
        event = Event()
    
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
                    purchase = Purchase(user=user.username, product=products[i], amount=int(prices[i]), event=event.title)
                    purchase.save()
                
                return render(request, 'products/payment.html', {'user': user, 'event':event})
            except:
                print('exception')
                products = Product.objects
                beer = products.filter(category='beer')
                drinks = products.filter(category='drink')
                shots = products.filter(category='shot')
                other = products.filter(category='other')
                #print(beer[1].title)
                return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'error': 'noe gikk galt'})

    else:
        products = Product.objects
        beer = products.filter(category='beer')
        drinks = products.filter(category='drink')
        shots = products.filter(category='shot')
        other = products.filter(category='other')
        #print(beer[1].title)
        return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other})

    
def payment(request):
    return render(request, 'products/payment.html')

@staff_member_required
def select_history(request):
    
    events = Event.objects.all()
    
    return render(request, 'products/select_history.html', {'events': events.order_by('-start_date')})

def event_history(request, event_id):
    
    event = get_object_or_404(Event, pk=event_id)
    purchases = Purchase.objects.filter(event=event.title)
    
    return render(request, 'products/history.html', {'purchases': purchases})

@staff_member_required
def history(request):
    
    purchases = Purchase.objects.all()
    
    return render(request, 'products/history.html', {'purchases': purchases.order_by('-time')})

























