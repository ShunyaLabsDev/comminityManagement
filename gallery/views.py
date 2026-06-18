from django.shortcuts import render
from .models import GalleryImage, CATEGORY_CHOICES

def gallery(request):
    category = request.GET.get('category', '')
    images = GalleryImage.objects.filter(is_active=True)
    if category:
        images = images.filter(category=category)
    return render(request, 'public/gallery.html', {
        'images': images, 'category': category,
        'categories': CATEGORY_CHOICES
    })
