from django.urls import path
from .views import profileView, register_user, login_user
app_name = "accounts"
urlpatterns = [
    path("", view=profileView, name="user"),
    path("register/", view=register_user, name="register-user"),
    path("login/", view=login_user, name="login-user"),
]