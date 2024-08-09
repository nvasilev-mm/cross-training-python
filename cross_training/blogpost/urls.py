from django.urls import path

from . import views

app_name = "blogpost"
urlpatterns = [
	path("", views.index, name = "index"),
	path("register/", views.register, name = "register"),
	path("login/", views.login, name = "login"),
	path("success/", views.success, name = "success"),
]