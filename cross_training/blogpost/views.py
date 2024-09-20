from django.db.models import Count
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from .models import Post, Comment, Vote
from .forms import CreatePostForm, CreateCommentForm
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, VoteSerializer, HtagSerializer, UserSerializer

(["GET"])
def index_view(request, format = None):
	return Response({ #app_name is required when reversing urls
		"posts": reverse("blogpost:posts", request = request, format = format),
	})

class Register(APIView):
	def post(self, request, format = None):
		serializer = UserSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class Login(APIView):
	def post(self, request, format = None):
		username = request.data.get("username")
		password = request.data.get("password")

		user = User.objects.get(username = username)

		if not user:
			user = authenticate(username = username, password = password)
		
		if user:
			token, _ = Token.objects.get_or_create(user = user)
			return Response({"token": token.key}, status = status.HTTP_200_OK)
		
		return Response({"error": "Invalid credentials"}, status = status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
	def post(self, request, format = None):
		try:
			request.user.auth_token.delete()
			return Response({"success": "Successfully logged out"}, status = status.HTTP_200_OK)
		except Exception as e:
			return Response({"error": str(e)}, status = status.HTTP_400_BAD_REQUEST)		

class PostList(APIView):
	def get(self, request, format = None):
		posts = Post.objects.all()
		serializer = PostSerializer(posts, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = PostSerializer(data = requsest.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Resposne(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class PostDetails(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

	def get_object(self, id):
		try:
			post = Post.objects.get(id = id)
			post.comments = Comment.objects.filter(post = post)
			return post
		except Post.DoesNotExist:
			raise Http404
	
	def get(self, request, id, format = None):
		post = self.get_object(id)
		serializer = PostSerializer(post)
		return Response(serializer.data)

	def put(self, request, id, format = None):
		post = self.get_object(id)
		serializer = PostSerializer(post, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id, format = None):
		post = self.get_object(id)
		post.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

class CommentList(APIView):
	def get(self, request, format = None):
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many = True)
		return Response(serializer.data)

	def post(self, request, format = None):
		serializer = CommentSerializer(data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CommentDetails(APIView):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

	def get_object(self, id):
		try:
			comment = Comment.objects.get(id = id)
			return comment
		except Comment.DoesNotExist:
			raise Http404

	def get(self, request, id, format = None):
		comment = self.get_object(id)
		serializer = CommentSerializer(comment)
		return Response(serializer.data)

	def put(self, request, id, format = None):
		comment = self.get_object(id)
		serializer = CommentSerializer(comment, data = request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.error_messages, status = status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id, format = None):
		comment = self.get_object(id)
		comment.delete()
		return Response(status = status.HTTP_204_NO_CONTENT)

class CastUpvote(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

	def post(self, request, id, format = None):
		post = Post.objects.get(id = id)
		vote, created = Vote.objects.get_or_create(author = request.user, post = post)
		if created:
			vote.is_upvote = True
			vote.save()
			post.votes += 1
			post.save()
			return Response(status = status.HTTP_204_NO_CONTENT)
		# is this even necessary?
		#return Response(status = status.HTTP_200_OK)

class CastDownvote(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

	def post(self, request, id, format = None):
		post = Post.objects.get(id = id)
		vote, created = Vote.objects.get_or_create(author = request.user, post = post)
		if created:
			vote.is_upvote = True
			vote.save()
			post.votes -= 1
			post.save()
			return Response(status = status.HTTP_204_NO_CONTENT)

class Search(APIView):

	def get_queryset(self):
		title_param = self.request.query_params.get("title")
		htag_param = self.request.query_params.get("htag")

		#this doesn't feel like the most elegant way to validate the data
		if title_param is None and htag_param is None:
			posts = Post.objects.all().order_by("-created_at")
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)
		elif title_param is not None and htag_param is None:
			posts = Post.objects.filter(title = title_param).order_by("-created_at")
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)
		elif title_param is None and htag_param is not None:
			posts = Post.objects.filter(hashtags__name = htag_param).order_by("-created_at")
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)
		else:
			posts = Post.objects.filter(title = title_param).filter(hashtags__name = htag_param).order_by("-created_at")
			serializer = PostSerializer(posts, many = True)
			return Response(serializer.data)

class SearchHot(generics.ListAPIView):
	serializer_class = PostSerializer

	def get_queryset(self):
		return Post.objects.annotate(comments_count = Count("comments")).filter(votes__gte = 1, comments_count__gte = 2)