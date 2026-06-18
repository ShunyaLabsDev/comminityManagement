from django.db import models
from django.utils import timezone


class Announcement(models.Model):
    title = models.CharField(max_length=300, verbose_name='શીર્ષક / Title')
    description = models.TextField(verbose_name='વિગત / Description')
    publish_date = models.DateField(default=timezone.now, verbose_name='પ્રકાશન તારીખ / Publish Date')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Announcement / જાહેરાત'
        verbose_name_plural = 'Announcements / જાહેરાતો'
        ordering = ['-publish_date']

    def __str__(self):
        return self.title
