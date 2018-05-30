from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from products.models import Purchase

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


def profile(request):
    current_user = request.user
    purchases = Purchase.objects.filter(user=current_user.username)
    
    return render(request, 'accounts/profile.html', {'purchases': purchases})


