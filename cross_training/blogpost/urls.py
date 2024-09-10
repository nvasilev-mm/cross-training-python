from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register("posts", views.PostDetails, basename = "posts")

app_name = "blogpost"
urlpatterns = [
	path("", views.index_view, name = "index"),
	path("register/", views.Register.as_view(), name = "register"),
	path("login/", views.Login.as_view(), name = "login"),
	path("logout/", views.Logout.as_view(), name = "logout"),
	path("posts/", views.PostList.as_view(), name = "posts"),
	# path("posts/create/", views.post_create_view, name = "create"),
	path("posts/upvote/<int:id>", views.CastUpvote.as_view(), name = "upvote"),
	path("posts/downvote/<int:id>", views.CastDownvote.as_view(), name = "downvote"),
	path("posts/<int:id>", views.PostDetails.as_view(), name = "post_details"),
	path("comments/", views.CommentList.as_view(), name = "comments"),
	path("comments/<int:id>", views.CommentDetails.as_view(), name = "comment_details"),
	path("search/", views.Search.as_view(), name = "search"),
]