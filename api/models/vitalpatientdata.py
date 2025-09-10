from django.db import models


class vitalPatientDetails(models.Model):
    PatientId = models.CharField(max_length=250)
    PatientName = models.CharField(max_length=270)
    age = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    TestDate = models.CharField(max_length=250)
    ReportDate = models.CharField(max_length=250)
    height = models.CharField(max_length=250, null=True, default=None, blank=True)
    weight = models.CharField(max_length=250, null=True, default=None, blank=True)
    blood = models.CharField(max_length=250, null=True, default=None, blank=True)
    pulse = models.CharField(max_length=250, null=True, default=None, blank=True)
    chest_inhale = models.CharField(max_length=250, null=True, default=None, blank=True)
    chest_exhale = models.CharField(max_length=250, null=True, default=None, blank=True)
    abdomen = models.CharField(max_length=250, null=True, default=None, blank=True)

    def __str__(self):
        return self.PatientId
