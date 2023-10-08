from django.urls import path
from .views import profileView, register_user, login_user, logout_user, list_user
app_name = "accounts"
urlpatterns = [
    path("<int:pk>/", view=profileView, name="user"),
    path("register/", view=register_user, name="register-user"),
    path("login/", view=login_user, name="login-user"),
    path("logout/", view=logout_user, name="logout-user"),
    path("users/", view=list_user, name="list-user")
]