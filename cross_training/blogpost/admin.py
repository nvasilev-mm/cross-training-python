from django.contrib import admin
from .models import Post, Htag, Comment

admin.site.register(Post)
admin.site.register(Htag)
admin.site.register(Comment)
