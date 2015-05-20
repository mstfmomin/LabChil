from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

from timezone_field import TimeZoneField

from core.models import TimeStampedModel
from glucoses.models import Category, Unit


class UserSettings(TimeStampedModel):
    """
    Model to store additional user settings and preferences. Extends User
    model.
    """
    user = models.OneToOneField(User, related_name='settings')

    time_zone = TimeZoneField(default=settings.TIME_ZONE)

    glucose_unit = models.ForeignKey(Unit, null=False, blank=False, default=1)
    default_category = models.ForeignKey(Category, null=True)

    glucose_low = models.PositiveIntegerField(
        null=False, blank=False, default=60)
    glucose_high = models.PositiveIntegerField(
        null=False, blank=False, default=180)
    glucose_target_min = models.PositiveIntegerField(
        null=False,  blank=False, default=70)
    glucose_target_max = models.PositiveIntegerField(
        null=False, blank=False, default=120)

    def username(self):
        return self.user.username
    username.admin_order_field = 'user__username'

    class Meta:
        verbose_name_plural = 'User Settings'