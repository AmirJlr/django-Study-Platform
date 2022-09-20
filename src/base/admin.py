from django.contrib import admin
from .models import Topic, Room, Message

# Register your models here.

admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)