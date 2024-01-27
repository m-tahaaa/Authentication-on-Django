from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

@login_required
def index(request):
    return render(request,"auth/index.html")

def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        return redirect('signin')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    
    elif request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, 'auth/signup.html') 

        myuser = User.objects.create_user(username=email, email=email, password=password)
        myuser.first_name = first_name
        myuser.last_name = last_name
        myuser.save()

        return redirect('signin')
    else:
        return render(request, 'auth/signup.html') 

def signin(request):

    if request.user.is_authenticated:
        return redirect('index')
    
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
    return render(request, 'auth/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('home')
