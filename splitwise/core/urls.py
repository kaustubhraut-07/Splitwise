from .views import user_login
from django.urls import path

urlpatterns = [
    path('user_login/', user_login, name='user_login'),
]