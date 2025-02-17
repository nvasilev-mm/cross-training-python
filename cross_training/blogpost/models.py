from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    votes = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        hashtags_list = self.hashtags()
        htags_list = []
        for tag in hashtags_list:
            if not Htag.objects.filter(name = tag).exists():
                htags_list.append(tag)
        if htags_list:
            batch = [Htag(name = new_tag) for new_tag in htags_list]
            Htag.objects.bulk_create(batch)
        super(Post, self).save(*args, **kwargs)

    def hashtags(self):
        return [tag.strip() for tag in self.content.split() if tag.startswith("#")]

class Htag(models.Model):
    name = models.CharField(max_length = 500, unique = True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name = "comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = None, related_name = "comments") 

    def __str__(self):
        return self.content

class Vote(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, default = None)
    post = models.ForeignKey(Post, on_delete = models.CASCADE, default = None)
    is_upvote = models.BooleanField(default = True)