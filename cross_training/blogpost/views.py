from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, LoginForm

def index(request):
	return render(request, "blogpost/index.html")

def register(request):
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.save()
			return index(request)
	else:
		form = RegisterForm()
	return render(request, "blogpost/register.html", {"form": form})

def login(request):
	return render(request, "blogpost/login.html")

def success(request):
	return render(request, "blogpost/success.html")

#django url creation parse template