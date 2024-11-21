from .views import user_login ,update_userinfo,getuser_Info,deleteuser_Info , create_group,get_group_user_present,get_groups,add_user_to_group,delete_group
from django.urls import path

urlpatterns = [

    #-------------- user apis endpoitns --------------
    path('user_login/', user_login, name='user_login'),
    path('update_userinfo/<id>/', update_userinfo, name='update_userinfo'),
    path('getuser_Info/<id>/', getuser_Info, name='getuser_Info'),
    path('deleteuser_Info/<id>/', deleteuser_Info, name='deleteuser_Info'),

    # ---------------group api endpoints------------------
    path('create_group/', create_group, name='create_group'),
    path('get_group_user_present/<id>/', get_group_user_present, name='get_group_user_present'),
    path('getall_groups/',get_groups, name='get_group_user_present'),
    path('add_user_to_group/<id>/', add_user_to_group, name='add_user_to_group'),
    path('delete_group/<id>/', delete_group, name='delete_group'),
]