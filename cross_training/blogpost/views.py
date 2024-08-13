from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post
from .forms import CreatePostForm

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
			return posts_view(request)
	else:
		form = AuthenticationForm()
	return render(request, "blogpost/login.html", {"form": form})

def logout_view(request):
	if request.method == "POST":
		logout(request)
		return redirect("blogpost:index")

def posts_view(request):
	posts = Post.objects.all().order_by("-created_at")
	if not posts:
		post_one = Post(title = "First Post", content = "Some Content", author=request.user)
		post_two = Post(title = "Second Post", content = "Some Other Content", author=request.user)
		post_one.save()
		post_two.save()
		posts = Post.objects.all().order_by("-created_at")
		pass
	
	return render(request, "blogpost/posts.html", {"posts" : posts})

def post_create_view(request):
	if request.method == "POST":
		form = CreatePostForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.author = request.user
			instance.save()
			return redirect("blogpost:posts")
	else:
		form = CreatePostForm()
	return render(request, "blogpost/create.html", {"form": form})

#django url creation parse template