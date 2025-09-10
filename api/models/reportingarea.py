from django.db import models
from django.contrib.auth.models import User



class ReportingArea(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    mriopt = models.CharField(max_length=100, blank=True, null=True)
    mriothers = models.CharField(max_length=100, blank=True, null=True)
    ctopt = models.CharField(max_length=100, blank=True, null=True)
    ctothers = models.CharField(max_length=100, blank=True, null=True)
    xray = models.BooleanField(default=False)
    others = models.BooleanField(default=False)
