from django.urls import path
from Model import views

urlpatterns = [
    path('', views.user_info_update, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('deregister/', views.delete_user, name='deregister'),
    path('userInfo/', views.user_info, name='user_info'),
    path('userInfo/update/', views.user_info_update, name='user_info_update'),
    path('userInfo/credits/', views.info_credits, name='info_credits'),
    path('csrf-token/', views.csrf, name='csrf-token'),
]