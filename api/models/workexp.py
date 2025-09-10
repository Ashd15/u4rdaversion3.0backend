from django.contrib.auth.models import User
from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class WorkExp(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    exinstitution = models.CharField(max_length=30, null=True, default=None, blank=True)
    exstdate = models.DateField(null=True, default=None, blank=True)
    exenddate = models.DateField(null=True, default=None, blank=True)
    designation = models.CharField(max_length=255, null=True, default=None, blank=True)
    exinstitution1 = models.CharField(max_length=30, null=True, default=None, blank=True)
    exstdate1 = models.DateField(null=True, default=None, blank=True)
    exenddate1 = models.DateField(null=True, default=None, blank=True)
    designation1 = models.CharField(max_length=15, null=True, default=None, blank=True)
    prexst = models.DateField(null=True, default=None, blank=True)
    prexend = models.DateField(null=True, default=None, blank=True)
    pii = models.CharField(max_length=15, null=True, default=None, blank=True)
    msname = models.CharField(max_length=15, null=True, default=None, blank=True)
    mcirgno = models.CharField(max_length=15, null=True, default=None, blank=True)
    regcecr = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), null=True, blank=True)

    def __str__(self):
        return str(self.user)