from django.shortcuts import render, redirect
from .models import CustomUser
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login,  authenticate
def profileView(request, pk):
    pk = request.user.id
    print(f"\n\n PROFILE VIEW = {pk}\n\n")
    user = CustomUser.objects.get(id=pk)
    f = user.firstname
     
    return render(request, "user_profile.html", {"user": user, "pk": pk, "f":f})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/accounts/login/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, "register_user.html", {"form": form})

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        print(f"\n\n PROFILE VIEW = { 1}\n\n")
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(f"\n\n PROFILE VIEW = {2}\n\n")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/books/')
            else: 
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {"form": form})

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('/books/')

def list_user(request, limit=200):
    users = CustomUser.objects.all()[:200]
    context = {
        "users": users
    }
    return render(request, "list_user.html", context)