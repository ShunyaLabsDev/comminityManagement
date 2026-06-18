from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(max_length=15, blank=True, verbose_name='મોબાઈલ / Mobile')
    role = models.CharField(
        max_length=30,
        choices=[
            ('committee_member', 'Committee Member'),
            ('data_entry_operator', 'Data Entry Operator'),
            ('member', 'Community Member'),
        ],
        default='member',
        verbose_name='ભૂમિકા / Role'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"
