from django.urls import path, include
from . import views

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.RegisterView, name="register"),
    path("logout_confirm/", views.LogoutConfirmView, name="logout_confirm"),
    path("profile/", views.ProfileView, name="profile")
]
