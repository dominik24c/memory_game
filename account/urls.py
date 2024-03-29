from django.contrib.auth import views as auth_views
from django.urls import path

from .views import register_view

app_name = 'auth'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='signup')
]
