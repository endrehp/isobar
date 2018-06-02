from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Product, Purchase, Event, Comment
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

import pandas as pd



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
    
    if request.method =='POST':
        
        try:
            current_user = request.user
            comment = request.POST['comment']
            product.comment_set.create(author=current_user.username, text=comment)
            product.save()
            
        except:
            pass
        
        
        return render(request, 'products/product_info.html', {'product': product, 'pk': product_id})

    else:


        return render(request, 'products/product_info.html', {'product': product, 'pk': product_id})

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
        active_events = Event.objects.filter(active=True)
        for event in active_events:
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
        
    try:
        purchases = Purchase.objects.all().order_by('-time')
        df = pd.DataFrame(list(purchases.values()))
        all_customers = list(df['user'])
        #unique_customers = list(set(list(df['user'])))
        #print(customers)
        
        customers=[]
        for i in range(len(all_customers)):
            if all_customers[i] not in customers:
                customers.append(all_customers[i])
                
            if len(customers)>10:
                break
        
    except:
        customers = None
        
    
    if request.method == 'POST':
        if request.POST['username']:
            try:
                user = User.objects.get(username=request.POST['username'])
                products = request.POST.getlist('title')
                prices = request.POST.getlist('price')
                total = sum(list(map(int, prices)))
                
                n_products = len(products) 
                #withdraw
                user.profile.add_money(-total)
                points_gained = user.profile.add_points(n_products)
                user.save()
                
                #register purchases
                for i in range(len(products)):
                    purchase = Purchase(user=user.username, product=products[i], amount=int(prices[i]), event=event.title)
                    purchase.save()
                
                return render(request, 'products/payment.html', {'user': user, 'event':event, 'points_gained': points_gained})
            except:
                print('exception')
                products = Product.objects
                beer = products.filter(category='beer')
                drinks = products.filter(category='drink')
                shots = products.filter(category='shot')
                other = products.filter(category='other')
                #print(beer[1].title)
                return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'error': 'noe gikk galt', 'customers': customers})

    else:
        products = Product.objects
        beer = products.filter(category='beer')
        drinks = products.filter(category='drink')
        shots = products.filter(category='shot')
        other = products.filter(category='other')
        
        #print(beer[1].title)
        return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'customers': customers})

    
def payment(request):
    return render(request, 'products/payment.html')

@staff_member_required
def select_history(request):
    
    events = Event.objects.all()
    members = User.objects.all()
    
    
    return render(request, 'products/select_history.html', {'events': events.order_by('-start_date'), 'members': members})

def event_history(request, event_id):
    
    event = get_object_or_404(Event, pk=event_id)
    purchases = Purchase.objects.filter(event=event.title).order_by('-time')
    
    try:

        df = pd.DataFrame(list(purchases.values()))
        
        n_contenders = len(list(set(list(df['user']))))
        n_sales = len(purchases)
        revenue = df['amount'].sum()
        cost = 0 #TODO
        earnings = revenue - cost 
        key_data = {'n_contenders':n_contenders, 'n_sales': n_sales, 'revenue': revenue, 'cost': cost, 'earnings': earnings}
        
        products = list(df['product'])
        unique_products = list(set(products))

        counts = []
        i=0
        for unique in unique_products:
            counts.append(0)
            for product in products:
                if product == unique:
                    counts[i] += 1
            i += 1

        fav_df = pd.DataFrame()
        fav_df['product'] = unique_products
        fav_df['count'] = counts
        fav_df.sort_values(by=['count'],ascending=False, inplace=True)
        #fav_df.reset_index(inplace=True, drop=True)
        fav_list = list(fav_df['product'])

        if len(fav_list)>5:
            fav_list = fav_list[0:5]


        xdata = unique_products
        ydata = counts

        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {
            'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'  # container name
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'event': event,
            'purchases': purchases,
            'key_data': key_data,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': True,
            },
        }

        return render(request, 'products/history.html', data)
    
    except:
        data={'purchases': purchases}
        return render(request, 'products/history.html', data)

    

def member_history(request, member_id):
    
    member = get_object_or_404(User, pk=member_id)
    purchases = Purchase.objects.filter(user=member.username)
    
    return render(request, 'products/history.html', {'purchases': purchases})

@staff_member_required
def history(request):
    
    purchases = Purchase.objects.all().order_by('-time')
    
    try:

        df = pd.DataFrame(list(purchases.values()))
        
        n_contenders = len(list(set(list(df['user']))))
        n_sales = len(purchases)
        revenue = df['amount'].sum()
        cost = 0 #TODO
        earnings = revenue - cost 
        key_data = {'n_contenders':n_contenders, 'n_sales': n_sales, 'revenue': revenue, 'cost': cost, 'earnings': earnings}

        products = list(df['product'])
        unique_products = list(set(products))

        counts = []
        i=0
        for unique in unique_products:
            counts.append(0)
            for product in products:
                if product == unique:
                    counts[i] += 1
            i += 1

        fav_df = pd.DataFrame()
        fav_df['product'] = unique_products
        fav_df['count'] = counts
        fav_df.sort_values(by=['count'],ascending=False, inplace=True)
        #fav_df.reset_index(inplace=True, drop=True)
        fav_list = list(fav_df['product'])

        if len(fav_list)>5:
            fav_list = fav_list[0:5]


        xdata = unique_products
        ydata = counts

        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {
            'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'  # container name
        data = {
            'charttype': charttype,
            'chartdata': chartdata,
            'chartcontainer': chartcontainer,
            'purchases': purchases,
            'key_data': key_data,
            'extra': {
                'x_is_date': False,
                'x_axis_format': '',
                'tag_script_js': True,
                'jquery_on_ready': True,
            },
        }

        return render(request, 'products/history.html', data)

    except:
        data={'purchases': purchases}
        return render(request, 'products/history.html', data)

























