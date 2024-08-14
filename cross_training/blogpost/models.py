from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length = 200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    votes = models.IntegerField(default = 0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def hashtags(self):
        return [tag.strip() for tag in self.content.split() if tag.startswith("#")]

    def __str__(self):
        return self.title