from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("view-rbt/<str:rbt>", views.supervisor_index, name="supervisor_index"),
    path("login", views.login_view, name="login_view"),
    path("logout", views.logout_view, name="logout_view"),
    path("register/<str:staff_type>", views.register, name="register"),
    path("view-hours/<str:table_type>", views.view_hours, name="view_hours"),
    path("log-data/<str:log_type>", views.log_data, name="log_data"),
    path("delete-data/<str:data_type>/<int:primary_key>", views.delete_data, name="delete_data"),
    path("download/<int:user_id>/<str:file_name>", views.download, name="download")
]