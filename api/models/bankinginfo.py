from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage


class BankingInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bankname = models.CharField(max_length=25, blank=True, null=True)
    acnumber = models.CharField(max_length=15, blank=True, null=True)
    ifsc = models.CharField(max_length=15, blank=True, null=True)
    pancardno = models.CharField(max_length=15, blank=True, null=True)
    pandcard = models.FileField(upload_to='uploads/', storage=S3Boto3Storage())
    cheque = models.FileField(upload_to='uploads/', storage=S3Boto3Storage())
    pictureproof = models.FileField(upload_to='uploads/', storage=S3Boto3Storage())
