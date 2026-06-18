from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=300, verbose_name='કાર્યક્રમ નામ / Event Title')
    description = models.TextField(verbose_name='વિગત / Description')
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name='ફોટો / Photo')
    event_date = models.DateField(verbose_name='તારીખ / Date')
    event_time = models.TimeField(null=True, blank=True, verbose_name='સમય / Time')
    location = models.CharField(max_length=300, verbose_name='સ્થળ / Location')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Event / કાર્યક્રમ'
        verbose_name_plural = 'Events / કાર્યક્રમો'
        ordering = ['-event_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.event_date >= timezone.now().date()
