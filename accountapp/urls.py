from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.homepage, name='homepage'),

]
