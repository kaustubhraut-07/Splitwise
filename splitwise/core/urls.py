from .views import user_login ,update_userinfo
from django.urls import path

urlpatterns = [
    path('user_login/', user_login, name='user_login'),
    path('update_userinfo/<id>/', update_userinfo, name='update_userinfo'),
]