import uuid
from django.shortcuts import render, redirect
from .models import CustomUser, Profile
import os

from django.contrib.auth import login, logout,  authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from twilio.rest import Client

from bookhiveapp.models import Book
from .forms import CustomUserCreationForm, LoginForm, CustomUserChangeForm
from .tokens import send_mail_after_registration

def token_send (request):
    return render(request , 'token_send.html')


def success (request):
    return render(request , 'success.html')


def error_page(request):
    return render(request, 'error.html') 

def profileView(request, pk):
    pk = request.user.id
    books = Book.objects.filter(owner=request.user)
    user = CustomUser.objects.get(id=pk)
    f = user.firstname
    return render(request, "user_profile.html", {"user": user, "pk": pk, "f":f, "books":books})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.errors:
                messages.success(request, f'{form.errors}') 
                return redirect('/account/register')
        if form.is_valid():
                username = request.POST.get('username')
                email = request.POST.get('email')
                if username == None:
                    messages.success(request, 'username maydoni bo\'sh  bo\'lishi mumkin emas.') 
                    return redirect('/account/register')
                elif email == None:
                    messages.success(request, 'email maydoni bo\'sh  bo\'lishi mumkin emas.') 
                    return redirect('/account/register')
                elif CustomUser.objects.filter(username = username).first():
                    messages.success(request,'Username is taken.')
                    return redirect('/account/register')
                elif CustomUser.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken')
                    return redirect('/account/register')
                form.save()
                token = str(uuid.uuid4)
                print(token, "token")
                user_obj = CustomUser.objects.get(email=email)
                print(user_obj)
                profile_obj = Profile.objects.create(user = user_obj , auth_token = token)
                profile_obj.save()
                send_mail_after_registration(email=email, token=token, request=request, username='admin1')
                return redirect('/account/token')
    else:
        form = CustomUserCreationForm()
    return render(request, "register_user.html", {"form": form})

def verify(request, token):
    try:
        print("\n\n\n", token)
        profile_obj = Profile.objects.get(auth_token = token) 
        profile_obj = Profile.objects.filter(auth_token = token).first() 
        
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            print("profile is saved")
            messages.success(request, 'You account is been verified')
            return redirect('/account/login')
        else:
            return redirect('/account/error')
    except Exception as e:
        print(e)
        
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            user_id = CustomUser.objects.get(username=username)
            print(user_id, user_id.pk)
            # Profile.objects.get(user=user_id.pk).is_verified and
            if  user is not None:
                login(request, user)
                return redirect('/')
            # elif not Profile.objects.get(user=username).is_verified:
            #     form.add_error(None, "Foydalanuvchi tasdiqlanmagan")
            else: 
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {"form": form})



def logout_user(request):
    logout(request)
    return redirect('/')

def list_user(request, limit=200):
    users = CustomUser.objects.all()[:200]
    context = {
        "users": users
    }
    return render(request, "list_user.html", context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')  # Replace 'profile' with the URL name of your user profile view
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
