from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.place_bid, name="place_bid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
