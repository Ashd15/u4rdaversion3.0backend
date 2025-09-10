from django.db import models
class Total_Cases(models.Model):
    total_uploaded_xray = models.IntegerField(default=0)
    total_uploaded_ecg = models.IntegerField(default=0)
    total_nonreported_xray = models.IntegerField(default=0)
    total_reported_xray = models.IntegerField(default=0)
    total_reported_ecg = models.IntegerField(default=0)

