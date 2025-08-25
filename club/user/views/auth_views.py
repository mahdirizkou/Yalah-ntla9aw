
from ..models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)  
        return redirect("profile")

    return render(request, "registre.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  
            return redirect("profile")
        else:
            return render(request, "login.html", {"error": "username or password incorrect"})

    return render(request, "login.html")
