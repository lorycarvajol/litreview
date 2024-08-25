from django.urls import path
from .views import CustomLoginView, create_ticket, register
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView, register, home_view, custom_logout_view

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register/", register, name="register"),
    path("home/", home_view, name="home"),
    path("logout/", custom_logout_view, name="logout"),
    path(
        "ticket/create/", create_ticket, name="create_ticket"
    ),  # URL pour créer un ticket
]
