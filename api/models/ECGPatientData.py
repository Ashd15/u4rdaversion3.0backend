from django.db import models

class ecgPatientDetails(models.Model):
    PatientId = models.CharField(max_length=50, null=True)
    PatientName = models.CharField(max_length=70, null=True)
    age = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    testdate = models.CharField(max_length=50, null=True)
    reportdate = models.CharField(max_length=50, null=True)
    heartrate = models.CharField(max_length=50, null=True)
    findings = models.CharField(max_length=100, null=True)
    

    def _str_(self):
        return self.PatientId + "_" + self.PatientName