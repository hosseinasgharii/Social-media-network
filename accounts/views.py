from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from accounts.models import MyUser

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        
        # Validate the input if needed
        
        MyUser.objects.create_user(email=email, username=username, password=password)
        
        return redirect('login')
    
    return render(request, 'signup.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace 'home' with your desired homepage URL
        
        # Authentication failed
        error_message = 'Invalid email or password.'
        return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout
