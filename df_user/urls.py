from django.conf.urls import url
from django.urls import path

from df_user import views

app_name = 'user'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_handler/', views.register_handler, name='register_handler'),
    path('login/', views.login, name='login'),
    path('login_handler/', views.login_handler, name='login_handler'),
    path('check_user_exist/', views.register_user_exist, name='check_user_exist'),
    path('user_center_info/', views.user_center_order, name='user_center_order')
]
