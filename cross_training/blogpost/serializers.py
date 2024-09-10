from django.contrib.auth.models import User
from rest_framework import serializers
from blogpost.models import Post, Htag, Comment, Vote

"""
Explicit serializers are also available. Example:
class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length = 200)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(auto_now_add = True)
    votes = serializers.IntegerField(default = 0)
    author = serializers.CharField()
"""

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = "author.username")

    class Meta:
        model = Comment
        fields = ["post", "content", "created_at", "author"]
        # fields = "__all__"

class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = "author.username")
    comments = CommentSerializer(many = True, read_only = True)

    class Meta:
        model = Post
        fields = ["title", "content", "created_at", "author", "votes", "comments"]
        # fields = "__all__"

class VoteSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source = "author.username")

    class Meta:
        model = Vote
        fields = ["author", "post", "is_upvote"]


class HtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Htag
        fields = ["name"]
