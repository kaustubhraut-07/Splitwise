from .views import user_login ,update_userinfo,getuser_Info,deleteuser_Info
from django.urls import path

urlpatterns = [
    path('user_login/', user_login, name='user_login'),
    path('update_userinfo/<id>/', update_userinfo, name='update_userinfo'),
    path('getuser_Info/<id>/', getuser_Info, name='getuser_Info'),
    path('deleteuser_Info/<id>/', deleteuser_Info, name='deleteuser_Info'),
]