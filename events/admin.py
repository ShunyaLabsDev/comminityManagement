from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'location', 'is_upcoming', 'is_published')
    list_filter = ('is_published', 'event_date')
    search_fields = ('title', 'location')
