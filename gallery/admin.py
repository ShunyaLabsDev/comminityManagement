from django.contrib import admin
from .models import GalleryImage
@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'is_active')
    list_filter = ('category', 'is_active')
