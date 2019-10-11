from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from time import time
from ckeditor.fields import RichTextField
# Create your models here.


def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Article(models.Model):
    R = "R"
    A = "A"
    status_choice = (
        (R, 'На рассмотрении'),
        (A, 'Принято'),
    )
    status = models.CharField('Cтатус', max_length=2, choices=status_choice, default=R)
    article_title = models.CharField('Название cтатьи', max_length=100)
    article_text = RichTextField('Текст статьи')
    genres = models.ManyToManyField('Genre', blank=True, related_name='Жанры')
    article_image = models.ImageField('Фото', upload_to='images', height_field=None, width_field=None, max_length=100, blank=True)
    article_slug = models.SlugField('Идентификатор', unique=False, max_length=150, blank=True)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.article_title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.article_title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    R = "R"
    A = "A"
    status_choice = (
        (R, 'На рассмотрении'),
        (A, 'Принято'),
    )
    status = models.CharField('Cтатус', max_length=2, choices=status_choice, default=R)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name = models.CharField('Имя автора', max_length=50)
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)
    comment_text = models.TextField('Текст комментария')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Genre(models.Model):
    title = models.CharField('Заголовок', max_length=30, unique=True, blank=True)
    slug = models.SlugField('Идентификатор', max_length=150, blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

