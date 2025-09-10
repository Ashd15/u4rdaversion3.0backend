from django.db import models
from django.contrib.auth.models import User



class TimeAvailability(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)
    saturday = models.BooleanField(default=False)
    sunday = models.BooleanField(default=False)
    monst = models.CharField(max_length=255, default="Individual")
    monend = models.CharField(max_length=255, default="Individual")
    tuest = models.CharField(max_length=255, default="Individual")
    tueend = models.CharField(max_length=255, default="Individual")
    wedst = models.CharField(max_length=255, default="Individual")
    wedend = models.CharField(max_length=255, default="Individual")
    thust = models.CharField(max_length=255, default="Individual")
    thuend = models.CharField(max_length=255, default="Individual")
    frist = models.CharField(max_length=255, default="Individual")
    friend = models.CharField(max_length=255, default="Individual")
    satst = models.CharField(max_length=255, default="Individual")
    satend = models.CharField(max_length=255, default="Individual")
    sunst = models.CharField(max_length=255, default="Individual")
    sunend = models.CharField(max_length=255, default="Individual")
