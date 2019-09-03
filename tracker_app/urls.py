from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("register", views.register, name="register"),
    path("view-hours", views.view_hours, name="view_hours"),
    path("log-data", views.log_data, name="log_data"),
]