from django.db import models
from django.contrib.auth.models import User
from .Xray_Location import XLocation

class Institution(models.Model):
    name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class ServiceTATSetting(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)  # Dropdown

    night_tat_hours = models.PositiveIntegerField(help_text="TAT in hours for Night", default=0)
    normal_tat_hours = models.PositiveIntegerField(help_text="TAT in hours for Normal", default=0)
    urgent_tat_hours = models.PositiveIntegerField(help_text="TAT in hours for Urgent", default=0)

    def __str__(self):
        return f"{self.institution.name} | {self.service.name}"

class Client(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    location = models.ForeignKey(XLocation, on_delete=models.CASCADE, null=True, blank=True)
    institutions = models.ManyToManyField(Institution, blank=True)
    tbclient = models.BooleanField(default=False)

    # Field-level permissions for editable fields
    can_edit_patient_name = models.BooleanField(default=False)
    can_edit_patient_id = models.BooleanField(default=False)
    can_edit_age = models.BooleanField(default=False)
    can_edit_gender = models.BooleanField(default=False)
    can_edit_study_date = models.BooleanField(default=False)
    can_edit_study_description = models.BooleanField(default=False)
    can_edit_notes = models.BooleanField(default=False)
    can_edit_body_part_examined = models.BooleanField(default=False)
    can_edit_referring_doctor_name = models.BooleanField(default=False)
    can_edit_whatsapp_number = models.BooleanField(default=False)
    can_edit_email = models.BooleanField(default=False)
    can_edit_contrast_used = models.BooleanField(default=False)
    can_edit_is_follow_up = models.BooleanField(default=False)
    can_edit_inhouse_patient = models.BooleanField(default=False)


    upload_header = models.FileField(upload_to='headers/', null=True, blank=True)
    upload_footer = models.FileField(upload_to='footers/', null=True, blank=True)

    def __str__(self):
        return self.name


