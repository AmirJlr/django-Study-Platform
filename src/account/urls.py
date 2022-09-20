from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('profile/<str:pk>',views.userProfile, name='profile'),
    path('edit-profile/',views.editProfile, name='edit-profile'),
    
    path('login', views.loginPage, name='login'),
    path('log-out', views.logoutPage, name='logout'),
    path('register', views.registerPage, name='register'),
]

