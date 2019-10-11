from django.contrib.auth import views
from django.urls import path
from . import views as view

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login_url'),
    path('logout/', view.logout_view, name='logout_url'),
    path('registration/', view.registration_view, name='registration_url')
]