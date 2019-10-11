from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='main_url'),
    path('view/<str:slug>/', views.view_article, name='view_article_url'),
    path('view/<str:slug>/leave_comment/', views.leave_comment, name='leave_comment_url'),
    path('info/', views.info, name='info_url'),
    path('author/<int:id>/', views.author_search, name='author_url'),
    path('tag/<str:slug>/', views.tag_view, name='tag_view_url'),
    path('cooperation/', views.cooperation_view, name='cooperation_url')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)