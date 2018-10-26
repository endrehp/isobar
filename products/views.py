from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from .models import Category, Product, Purchase, Event, Comment, Rating
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

@login_required
def menu(request):
    categories = Category.objects
    beer = categories.get(category='Beer').product_set.all()
    drinks = categories.get(category='Drink').product_set.all()
    shots = categories.get(category='Shot').product_set.all()
    other = categories.get(category='Other').product_set.all()
    #print(beer[1].title)
    return render(request, 'products/menu.html', {'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other})

@staff_member_required
def create_product(request):
    return render(request, 'products/create_product.html')

@login_required
def product_info(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)
    current_user = request.user
    sales = Purchase.objects.filter(product=product.title)
    n_sales = len(sales)
    n_sales_me = len(sales.filter(user=current_user.username))
    
    rated = len(product.rating_set.filter(author=current_user.username))
    
    if request.method =='POST':
        
        try:
            if request.POST['comment']:
                comment = request.POST['comment']
                product.comment_set.create(author=current_user.username, text=comment)
                product.save()
            elif request.POST['rating']:
                rating = int(request.POST['rating'])
                product.rating_set.create(author=current_user.username, rating=rating)
                product.add_rating(rating)
                product.save()
                rated = 1
        except:
            pass
        
        
        return render(request, 'products/product_info.html', {'product': product, 'pk': product_id, 'rated': rated, 'n_sales':n_sales, 'n_sales_me': n_sales_me})

    else:


        return render(request, 'products/product_info.html', {'product': product, 'pk': product_id, 'rated': rated, 'n_sales':n_sales, 'n_sales_me': n_sales_me})

@staff_member_required
def start_event(request):
    if request.method == 'POST':
        
        event = Event(title=request.POST['title'], active=True)
        event.save()
        
        
        categories = Category.objects
        beer = categories.get(category='Beer').product_set.all()
        drinks = categories.get(category='Drink').product_set.all()
        shots = categories.get(category='Shot').product_set.all()
        other = categories.get(category='Other').product_set.all()
        
        try:
        
            all_customers = User.objects.all().order_by('username')

            customers=[]
            for i in range(len(all_customers)):
                if all_customers[i] not in customers:
                    customers.append(all_customers[i].username)

                #if len(customers)>10:
                #    break

        except:
            customers = None
        
        return render(request, 'products/event.html', {'event': event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'customers':customers})
        
        
    else:
        return render(request, 'products/start_event.html')
    
def quit_event(request):
    try:
        active_events = Event.objects.filter(active=True)
        for event in active_events:
            event.active = False
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
        
        all_customers = User.objects.all().order_by('username')
        
        customers=[]
        for i in range(len(all_customers)):
            if all_customers[i] not in customers:
                customers.append(all_customers[i].username)
                
            #if len(customers)>10:
            #    break
        
    except:
        customers = None
        
    
    if request.method == 'POST':
        if request.POST['username']:
            try:
                user = User.objects.get(username=request.POST['username'])
                products = request.POST.getlist('title')
                product_ids = request.POST.getlist('id')
                prices = request.POST.getlist('price')
                total = sum(list(map(int, prices)))
                
                n_products = len(products) 
                #withdraw
                user.profile.add_money(-total)
                points_gained = user.profile.add_points(n_products)
                user.save()
                
                #register purchases
                for i in range(len(products)):
                    purchase = Purchase(user=user.username, product=products[i], product_id=int(product_ids[i]), amount=int(prices[i]), event=event.title)
                    purchase.save()
                
                return render(request, 'products/payment.html', {'user': user, 'event':event, 'points_gained': points_gained})
            except:
                categories = Category.objects
                beer = categories.get(category='Beer').product_set.all()
                drinks = categories.get(category='Drink').product_set.all()
                shots = categories.get(category='Shot').product_set.all()
                other = categories.get(category='Other').product_set.all()
                
                return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'error': 'noe gikk galt', 'customers': customers})

    else:
        categories = Category.objects
        beer = categories.get(category='Beer').product_set.all()
        drinks = categories.get(category='Drink').product_set.all()
        shots = categories.get(category='Shot').product_set.all()
        other = categories.get(category='Other').product_set.all()
        
        #print(beer[1].title)
        return render(request, 'products/event.html', {'event':event, 'beer':beer, 'drinks': drinks, 'shots': shots, 'other': other, 'customers': customers})

@staff_member_required    
def payment(request):
    return render(request, 'products/payment.html')

@staff_member_required
def select_history(request):
    
    events = Event.objects.all()
    members = User.objects.all()
    
    
    return render(request, 'products/select_history.html', {'events': events.order_by('-start_date'), 'members': members})

@staff_member_required
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
        product_ids = list(df['product_id'])
        unique_products = list(set(products))

        counts = []
        i=0
        for unique in unique_products:
            counts.append(0)
            for product in products:
                if product == unique:
                    counts[i] += 1
            i += 1
            
        categories = list(Category.objects.all())
        categories = [str(i) for i in categories]
        cat_dict = dict.fromkeys(categories, 0)
        
        for product_id in product_ids:
            product_object = Product.objects.get(id=product_id)
            cat_dict[product_object.category.category] += 1
        
        ######Charts#######
        
        #Barchart
        xdata = unique_products
        ydata = counts
        
        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {
            'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'  # container name
        
        
        #Piechart
        xdata2 = list(cat_dict.keys())
        ydata2 = list(cat_dict.values())
        
        color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
        
        extra_serie2 = { "tooltip": {"y_start": "", "y_end": ""}, "color_list": color_list}
        chartdata2 = {'x': xdata2, 'y1': ydata2, 'extra1': extra_serie2}
        charttype2 = "pieChart"
        chartcontainer2 = 'piechart_container'  # container name        
        
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
            'charttype2': charttype2,
            'chartdata2': chartdata2,
            'chartcontainer2': chartcontainer2,
            'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            }
        }

        return render(request, 'products/history.html', data)
    
    except:
        data={'purchases': purchases}
        return render(request, 'products/history.html', data)

    
@staff_member_required
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
        product_ids = list(df['product_id'])
        unique_products = list(set(products))

        counts = []
        i=0
        for unique in unique_products:
            counts.append(0)
            for product in products:
                if product == unique:
                    counts[i] += 1
            i += 1
            
        categories = list(Category.objects.all())
        categories = [str(i) for i in categories]
        cat_dict = dict.fromkeys(categories, 0)
        
        for product_id in product_ids:
            product_object = Product.objects.get(id=product_id)
            cat_dict[product_object.category.category] += 1
        
        ######Charts#######
        
        #Barchart
        xdata = unique_products
        ydata = counts
        
        extra_serie1 = {"tooltip": {"y_start": "", "y_end": " cal"}}
        chartdata = {
            'x': xdata, 'name1': '', 'y1': ydata, 'extra1': extra_serie1,
        }
        charttype = "discreteBarChart"
        chartcontainer = 'discretebarchart_container'  # container name
        
        
        #Piechart
        xdata2 = list(cat_dict.keys())
        ydata2 = list(cat_dict.values())
        
        color_list = ['#5d8aa8', '#e32636', '#efdecd', '#ffbf00', '#ff033e', '#a4c639',
                  '#b2beb5', '#8db600', '#7fffd4', '#ff007f', '#ff55a3', '#5f9ea0']
        
        extra_serie2 = { "tooltip": {"y_start": "", "y_end": ""}, "color_list": color_list}
        chartdata2 = {'x': xdata2, 'y1': ydata2, 'extra1': extra_serie2}
        charttype2 = "pieChart"
        chartcontainer2 = 'piechart_container'  # container name        
        
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
            'charttype2': charttype2,
            'chartdata2': chartdata2,
            'chartcontainer2': chartcontainer2,
            'extra2': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': False,
            }
        }

        return render(request, 'products/history.html', data)

    except:
        data={'purchases': purchases}
        return render(request, 'products/history.html', data)

























