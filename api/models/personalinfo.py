from django.contrib.auth.models import User
from django.db import models
from .serviceslist import ServicesList
from .exportlist import ExportList
from storages.backends.s3boto3 import S3Boto3Storage


class PersonalInfo(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    serviceslist = models.ManyToManyField(ServicesList)
    exportlist = models.ManyToManyField(ExportList)
    cnfpassword = models.CharField(max_length=212, null=True, default=None, blank=True)
    phone = models.CharField(max_length=210, null=True, default=None, blank=True)
    altphone = models.CharField(max_length=210, null=True, default=None, blank=True)
    reference = models.CharField(max_length=250, null=True, default=None, blank=True)
    resume = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), null=True, default=None, blank=True)
    uploadpicture = models.FileField(upload_to='uploads/', storage=S3Boto3Storage(), null=True, default=None, blank=True)
    signature = models.FileField(upload_to='static/signatures/', null=True, default=None, blank=True)
    companylogo = models.FileField(upload_to='static/companylogos/', null=True, default=None, blank=True)
    total_reported = models.IntegerField(default=0)
    uploadpicture = models.ImageField(
    upload_to='static/profile_pictures/', null=True, blank=True)


    def __str__(self):
        return str(self.user)
