from django.db import models

class xrayPatientDetails(models.Model):
    PatientId = models.CharField(max_length=50, null=True)
    PatientName = models.CharField(max_length=70, null=True)
    age = models.CharField(max_length=50, null=True)
    gender = models.CharField(max_length=50, null=True)
    testdate = models.CharField(max_length=50, null=True)
    reportdate = models.CharField(max_length=50, null=True)
    impressions = models.CharField(max_length=100, null=True)
    findings = models.CharField(max_length=200, null=True)
    jpeg_file = models.ImageField(upload_to='jpeg_files/')

    def _str_(self):
        return self.PatientId + "_" + self.PatientName