from django.contrib import admin
from News.models import Article, Comment, Genre
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Genre)