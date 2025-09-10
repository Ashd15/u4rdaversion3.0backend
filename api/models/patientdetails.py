from django.db import models
from .Date import Date
from .personalinfo import PersonalInfo
from .Location import Location
from storages.backends.s3boto3 import S3Boto3Storage


class PatientDetails(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    PatientId = models.CharField(max_length=255)
    PatientName = models.CharField(max_length=255)
    age = models.CharField(max_length=230)
    gender = models.CharField(max_length=215)
    HeartRate = models.CharField(max_length=230, null=True, blank=True)
    TestDate = models.CharField(max_length=220)
    ReportDate = models.CharField(max_length=220)
    PRInterval = models.CharField(max_length=230, null=True, blank=True)
    date = models.ForeignKey(Date, on_delete=models.CASCADE, default=None)
    image = models.ImageField(upload_to='ecg_jpgs/', storage=S3Boto3Storage(), null=True, blank=True)
    reportimage = models.FileField(upload_to='ecg_graphs/', storage=S3Boto3Storage(), null=True, blank=True)
    cardiologist = models.ForeignKey(PersonalInfo, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    isDone = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    # New field for urgency, non-reportable status
    urgent = models.BooleanField(default=False)  # Default: Not urgent
    NonReportable = models.BooleanField(default=False) # Default: Not reportable

    def __str__(self):
        return str(self.PatientName)
