from django.contrib import admin

# Register your models here.

from .models import Session, Presence

admin.site.register(Session)
admin.site.register(Presence)