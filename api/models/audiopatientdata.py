from django.db import models


class audioPatientDetails(models.Model):
    PatientId = models.CharField(max_length=255)
    PatientName = models.CharField(max_length=255)
    age = models.CharField(max_length=30)
    gender = models.CharField(max_length=15)
    TestDate = models.CharField(max_length=20)
    ReportDate = models.CharField(max_length=20)
    rightEarDB = models.CharField(max_length=100, null=True, default=None, blank=True)
    leftEarDB = models.CharField(max_length=100, null=True, default=None, blank=True)
    rightEarBoneDB = models.CharField(max_length=100, null=True, default=None, blank=True)
    leftEarBoneDB = models.CharField(max_length=100, null=True, default=None, blank=True)
    rightEarLevel = models.CharField(max_length=100, null=True, default=None, blank=True)
    leftEarLevel = models.CharField(max_length=100, null=True, default=None, blank=True)


    def __str__(self):
        return self.PatientName
