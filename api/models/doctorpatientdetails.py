from django.db import models

class DoctorPatientInfo(models.Model):
    PatientId = models.CharField(max_length=250)
    PatientName = models.CharField(max_length=270)
    age = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    date = models.CharField(max_length=250, null=True, blank=True)
    history = models.TextField(null=True, blank=True)
    findings = models.TextField(null=True, blank=True)
    advice = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.PatientName
