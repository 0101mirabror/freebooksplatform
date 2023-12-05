import uuid
from django.shortcuts import render, redirect
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, LoginForm, CustomUserChangeForm
from django.contrib.auth import login,  authenticate
from bookhiveapp.models import Book
from django.contrib import messages
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
    print(f"\n\n PROFILE VIEW = {pk}\n\n")
    user = CustomUser.objects.get(id=pk)
    f = user.firstname
     
    return render(request, "user_profile.html", {"user": user, "pk": pk, "f":f, "books":books})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        print(request.POST)
        print(form.errors) 
        if form.errors:
                messages.success(request, f'{form.errors}') 
                return redirect('/account/register')
        print(form.is_valid())
        if form.is_valid():
                username = request.POST.get('username')
                email = request.POST.get('email')
            # try:
                if username == None:
                    messages.success(request, 'username maydoni bo\'sh  bo\'lishi mumkin emas.') 
                    print(1)
                    return redirect('/account/register')
                elif email == None:
                    messages.success(request, 'email maydoni bo\'sh  bo\'lishi mumkin emas.') 
                    print(2)
                    return redirect('/account/register')
                elif CustomUser.objects.filter(username = username).first():
                    messages.success(request,'Username is taken.')
                    print(3)
                    return redirect('/account/register')
                elif CustomUser.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken')
                    print(4)
                    return redirect('/account/register')
                form.save()
                token = str(uuid.uuid4)
                user_obj = CustomUser.objects.get(email=email)
                profile_obj = Profile.objects.create(user = user_obj , auth_token = token)
                profile_obj.save()
                print(5)
                print(email, token, request, username)
                send_mail_after_registration(email='fayzullayevmirabror1@gmail.com', token='<function uuid4 at 0x00000276BD224C20>', request=request, username='admin1')
                print(6)
                return redirect('/account/token')
            # # return redirect('/account/login/')
            # except  Exception:
            #     print(Exception)
    else:
        form = CustomUserCreationForm()
         
    
    return render(request, "register_user.html", {"form": form})


def verify(request, token):
    try:
        print(token, type(token))
        profile_obj = Profile.objects.get(auth_token = token) 
        print(profile_obj)
        profile_obj = Profile.objects.filter(auth_token = token).first() 
        print(Profile.objects.filter(auth_token = token).first())
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

import os
from twilio.rest import Client
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
                # userga tizimga kirganligi haqida sms xabarnoma keladi
                account_sid = 'ACdce79ad6537cd422afa74f133b92efd4'
                auth_token = 'fba8e82ba9ea1f8fde2242add0fe7717'
                client = Client(account_sid, auth_token)

                message = client.messages \
                            .create(
                                 body=f"{username}, siz tizimga muvaffaqiyatli kirdingiz!!!",
                                 from_='+12562903985',
                                 to='+998971010158'
                             )  
                print(message.sid)
                return redirect('/')
            else: 
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(request, 'login.html', {"form": form})

from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('/')

def list_user(request, limit=200):
    users = CustomUser.objects.all()[:200]
    context = {
        "users": users
    }
    return render(request, "list_user.html", context)

from django.contrib.auth.decorators import login_required
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/books')  # Replace 'profile' with the URL name of your user profile view
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
