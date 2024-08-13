from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post

def index_view(request):
	return render(request, "blogpost/index.html")

def register_view(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			return login_view(request)
	else:
		form = UserCreationForm()
	return render(request, "blogpost/register.html", {"form": form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data = request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return render(request, "blogpost/posts.html")
	else:
		form = AuthenticationForm()
	return render(request, "blogpost/login.html", {"form": form})

def posts_view(request):
	posts = Post.objects.all().order_by("-created_at")
	if not posts:
		post_one = Post(title = "First Post", content = "Some Content")
		post_two = Post(title = "Second Post", content = "Some Other Content")
		post_one.save()
		post_two.save()
		posts = Post.objects.all().order_by("-created_at")
	
	return render(request, "blogpost/posts.html", {"posts" : posts})

#django url creation parse template