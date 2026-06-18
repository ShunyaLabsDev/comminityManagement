from django.db import models
from django.utils import timezone


CATEGORY_CHOICES = [
    ('samuh_lagan', 'સમૂહ લગ્ન / Samuh Lagan'),
    ('sneh_milan', 'સ્નેહ મિલન / Sneh Milan'),
    ('yuva', 'યુવા મિલન / Yuva Milan'),
    ('community', 'સામુદાયિક / Community'),
    ('other', 'અન્ય / Other'),
]


class GalleryImage(models.Model):
    title = models.CharField(max_length=200, verbose_name='શીર્ષક / Title')
    image = models.ImageField(upload_to='gallery/', verbose_name='ફોટો / Photo')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='community', verbose_name='શ્રેણી / Category')
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Gallery Image / ગેલેરી ફોટો'
        verbose_name_plural = 'Gallery Images / ગેલેરી ફોટા'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
