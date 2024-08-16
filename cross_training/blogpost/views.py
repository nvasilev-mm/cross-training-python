from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Post, Comment
from .forms import CreatePostForm, CreateCommentForm

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
			return redirect("blogpost:posts")
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

@login_required(login_url = "blogpost:login")
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

def post_detail_view(request, id):
	post = Post.objects.get(id = id)
	if request.method == "POST":
		form = CreateCommentForm(request.POST)
		if form.is_valid():
			comment = Comment(
				post = post,
				content = form.cleaned_data["content"],
				author=request.user
			)
			comment.save()
			return redirect("blogpost:detail", id)
	else:
		form = CreateCommentForm()
		comments = Comment.objects.filter(post = post)
		return render(request, "blogpost/detail.html", {"post": post, "form": form, "comments": comments})

@login_required(login_url = "blogpost:login")
def upvote_post(request, id):
	post = Post.objects.get(id = id)
	post.votes += 1
	post.save()
	return redirect("blogpost:posts")

@login_required(login_url = "blogpost:login")
def downvote_post(request, id):
	post = Post.objects.get(id = id)
	post.votes -= 1
	post.save()
	return redirect("blogpost:posts")

#django url creation parse template