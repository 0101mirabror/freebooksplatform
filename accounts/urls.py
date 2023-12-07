from django.urls import path
from .views import *
app_name = "accounts"
urlpatterns = [
    path("<int:pk>/", view=profileView, name="user"),
    path("register/", view=register_user, name="register-user"),
    path("login/", view=login_user, name="login-user"),
    path("logout/", view=logout_user, name="logout-user"),
    path("users/", view=list_user, name="list-user"),
    path("profile/edit", view=edit_profile, name="edit-profile"),
    path('token' , view=token_send , name='token_send'),
    path('success' , view=success, name ='success'),
    path('error' , view=error_page , name = "error"),
    path('verify/<token>' , verify ,name = "verify"),
     
]