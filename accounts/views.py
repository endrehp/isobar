from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from products.models import Purchase, Category, Product

#import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt



def signup(request):
    if request.method == 'POST':
        try:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    User.objects.get(username=request.POST['username'])

                    return render(request, 'accounts/signup.html', {'error': 'Username has already been taken'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                    auth.login(request, user)
                    return redirect('home')
            else:
                return render(request, 'accounts/signup.html', {'error': "passwords don't match"})
        except:
            return render(request, 'accounts/signup.html', {'error': 'one of the required fields are missing'})

    else:
        return render(request, 'accounts/signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect'}) 
            
    return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    #and don't forget to logout 
    return redirect('home')

@login_required
def my_profile(request):
    this_user = request.user
    purchases = Purchase.objects.filter(user=this_user.username).order_by('-time')

    try:
        df = pd.DataFrame(list(purchases.values()))
        
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
        '''
        n_products = len(Product.objects.all())
        n_unique = len(unique_products)
        unique_short = []
        max_length = n_products-n_unique+2
        for unique in unique_products:
            if len(unique) >= max_length:
                unique_short.append(unique[0:max_length])
            else:
                unique_short.append(unique)
        '''
        
        
        categories = list(Category.objects.all())
        categories = [str(i) for i in categories]
        cat_dict = dict.fromkeys(categories, 0)
        
        for product_id in product_ids:
            product_object = Product.objects.get(id=product_id)
            cat_dict[product_object.category.category] += 1
        
    
        fav_df = pd.DataFrame()
        fav_df['product'] = unique_products
        fav_df['count'] = counts
        fav_df.sort_values(by=['count'],ascending=False, inplace=True)
        #fav_df.reset_index(inplace=True, drop=True)
        fav_list = list(fav_df['product'])

        if len(fav_list)>5:
            fav_list = fav_list[0:5]
            
        try:
            drunkness = this_user.profile.get_drunkness(purchases)
        except:
            drunkness = 0
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
            'this_user': this_user,
            'purchases': purchases,
            'favourites': fav_list,
            'drunkness': drunkness,
            'my_profile': True,
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
        

        return render(request, 'accounts/profile.html', data)
    
    except:
        data={'this_user': this_user}
        return render(request, 'accounts/profile.html', data)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        try:
            current_user = request.user
            old_name = current_user.username
            new_name = request.POST['username']
            if old_name != new_name:
                current_user.username = new_name
                purchases = Purchase.objects.filter(user = old_name)
                for purchase in purchases:
                    purchase.user = new_name
                    purchase.save()
                    
            try:
                current_user.profile.image = request.FILES['image']
            except:
                pass
            
            current_user.save()
            return redirect('my_profile')
        except:
            return redirect('my_profile')
    else:
        return render(request, 'accounts/edit_profile.html')
    
@login_required
def members(request):
    
    members = User.objects.all()
    
    return render(request, 'accounts/members.html', {'members': members})
    
@login_required  
def member_profile(request, member_id):
    
    this_user = get_object_or_404(User, pk=member_id)
    purchases = Purchase.objects.filter(user=this_user.username).order_by('-time')
    if this_user == request.user:
        my_profile = True
        print('my profile')
    else:
        my_profile = False
    
    try:
        df = pd.DataFrame(list(purchases.values()))
        
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
        '''
        n_products = len(Product.objects.all())
        n_unique = len(unique_products)
        unique_short = []
        max_length = n_products-n_unique+2
        for unique in unique_products:
            if len(unique) >= max_length:
                unique_short.append(unique[0:max_length])
            else:
                unique_short.append(unique)
        '''
        
        
        categories = list(Category.objects.all())
        categories = [str(i) for i in categories]
        cat_dict = dict.fromkeys(categories, 0)
        
        for product_id in product_ids:
            product_object = Product.objects.get(id=product_id)
            cat_dict[product_object.category.category] += 1
        
    
        fav_df = pd.DataFrame()
        fav_df['product'] = unique_products
        fav_df['count'] = counts
        fav_df.sort_values(by=['count'],ascending=False, inplace=True)
        #fav_df.reset_index(inplace=True, drop=True)
        fav_list = list(fav_df['product'])

        if len(fav_list)>5:
            fav_list = fav_list[0:5]
            
        try:
            drunkness = this_user.profile.get_drunkness(purchases)
        except:
            drunkness = 0
        
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
            'this_user': this_user,
            'purchases': purchases,
            'favourites': fav_list,
            'drunkness': drunkness,
            'my_profile': my_profile,
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
        

        return render(request, 'accounts/profile.html', data)
    
    except:
        data={'this_user': this_user}
        return render(request, 'accounts/profile.html', data)

    
    
    
    
@login_required    
def my_consumption(request):
    """
    discretebarchart page
    """
    this_user = request.user
    purchases = Purchase.objects.filter(user=this_user.username).order_by('-time')
    df = pd.DataFrame(list(purchases.values()))
    #print(pd.DataFrame(list(purchases.values())))
    
    products = list(df['product'])
    print(products)
    unique_products = list(set(products))
    print(unique_products)
    
    counts = []
    i=0
    for unique in unique_products:
        counts.append(0)
        for product in products:
            if product == unique:
                counts[i] += 1
        i += 1
    
    
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
        'text': 'heihei',
        'extra': {
            'x_is_date': False,
            'x_axis_format': '',
            'tag_script_js': True,
            'jquery_on_ready': True,
        },
    }
    return render_to_response('accounts/my_consumption.html', data)
    
    
    
@staff_member_required
def balances(request):
    
    if request.method == 'POST':
        users = request.POST.getlist('username')
        amounts = request.POST.getlist('amount')
        print(users)
        
        for i in range(len(amounts)):
            try:
                user = User.objects.get(username=users[i])
                user.profile.add_money(int(amounts[i]))
                print('penger overført')
                user.save()
            except:
                pass
                
        members = User.objects.all().order_by('username')
        return render(request, 'accounts/balances.html', {'members': members})
    
    else:
        members = User.objects.all().order_by('username')
        
        return render(request, 'accounts/balances.html', {'members': members})
    
    
    
    
    
    
    
    
    
    