from django.urls import path
from .views import register_user,login_user

urlpatterns = [
    path('login/', login_user),
    path('register/', register_user, name='register_user'),
]
