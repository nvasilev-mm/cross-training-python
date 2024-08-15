from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    votes = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        hashtags_list = self.hashtags()
        htags_list = [None] * len(hashtags_list)
        for tag in hashtags_list:
            if not Htag.objects.filter(name = tag).exists():
                htags_list[hashtags_list.index(tag)] = htag
        if not htags_list.empty():
            Htag.objects.bulk_create(htags_list)
        super(Post, self).save(*args, **kwargs)

    def hashtags(self):
        return [tag.strip() for tag in self.content.split() if tag.startswith("#")]

class Htag(models.Model):
    name = models.CharField(max_length = 500, unique = True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None) 

    def __str__(self):
        return self.content
