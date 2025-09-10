from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage
from django.contrib.auth.models import User


class QualificationDetails(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    tensname = models.CharField(max_length=30, blank=True, null=True)
    tengrade = models.CharField(max_length=10, blank=True, null=True)
    tenpsyr = models.CharField(max_length=15, blank=True, null=True)
    tencertificate = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), blank=True, null=True)
    twelvesname = models.CharField(max_length=30, blank=True, null=True)
    twelvegrade = models.CharField(max_length=10, blank=True, null=True)
    twelvepsyr = models.CharField(max_length=15, blank=True, null=True)
    twelvecertificate = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), blank=True, null=True)
    mbbsinstitution = models.CharField(max_length=25, blank=True, null=True)
    mbbsgrade = models.CharField(max_length=10, blank=True, null=True)
    mbbspsyr = models.CharField(max_length=10, blank=True, null=True)
    mbbsmarksheet = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), blank=True, null=True)
    mbbsdegree = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), blank=True, null=True)
    mdinstitution = models.CharField(max_length=25, blank=True, null=True)
    mdgrade = models.CharField(max_length=10, blank=True, null=True)
    mdpsyr = models.CharField(max_length=10, blank=True, null=True)
    mddegree = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), blank=True, null=True)
