from django.contrib import admin
from .models import Event, User


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
