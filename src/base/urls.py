from django.urls import path
from . import views

app_name = 'room'

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMsg, name="delete-message"),

    path('topics/', views.topics, name="topics"),
    path('activities/', views.activity, name="activity"),

]