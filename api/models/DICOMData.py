from django.db import models
from .personalinfo import PersonalInfo
from .Xray_Location import XLocation
from .corporatecoordinator import CorporateCoordinator
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.timezone import now
import pytz
from django.db.models.signals import m2m_changed
from django.dispatch import receiver



class DICOMData(models.Model):
    patient_name = models.CharField(max_length=250, blank=True)
    patient_id = models.CharField(max_length=250, blank=True)
    age = models.CharField(max_length=250, blank=True)
    gender = models.CharField(max_length=250, blank=True)
    study_date = models.CharField(max_length=250, blank=True)
    study_time = models.TimeField(max_length=250, blank=True, null=True)
    recived_on_orthanc = models.TimeField(max_length=250, blank=True, null=True)
    recived_on_db = models.DateTimeField(blank=True, null=True)
    Modality = models.CharField(max_length=250, blank=True, null=True)
    study_id = models.CharField(max_length=100, blank=True)
    study_description = models.CharField(max_length=200, blank=True)
    isDone = models.BooleanField(default=False)
    NonReportable = models.BooleanField(default=False)
    Mlc = models.BooleanField(default=False)
    urgent = models.BooleanField(default=False)
    vip = models.BooleanField(default=False)
    twostepcheck = models.BooleanField(default=True)
    notes = models.TextField(max_length=50000, default=True)
    #location = models.ForeignKey(XLocation, on_delete=models.CASCADE, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    radiologist = models.ManyToManyField(PersonalInfo, blank=True)
    corporatecoordinator = models.ManyToManyField(CorporateCoordinator, blank=True)
    body_part_examined = models.CharField(max_length=200, blank=True, null=True)
    #accession_number = models.CharField(max_length=50, null=True, blank=True)
    institution_name = models.CharField(max_length=250, blank=True, null=True, default="None")
    referring_doctor_name = models.CharField(max_length=250, blank=True, null=True, default="None")
    whatsapp_number = models.CharField(max_length=10, blank=True, null=True)
    radiologist_assigned_at = models.DateTimeField(null=True, blank=True)
    marked_done_at = models.DateTimeField(null=True, blank=True)
    notes_modified_at = models.DateTimeField(null=True, blank=True)
    # ✅ New fields
    contrast_used = models.BooleanField(default=False)  # Was contrast used?
    is_follow_up = models.BooleanField(default=False)   # Follow-up / repeat case?
    imaging_views = models.CharField(max_length=500, blank=True, null=True) 
    inhouse_patient = models.BooleanField(default=False)  # In-house report?
    email = models.EmailField(max_length=254, blank=True, null=True)

    
    def save(self, *args, **kwargs):
        india_tz = pytz.timezone("Asia/Kolkata")
        now_ist = now().astimezone(india_tz)
        
        if not self.recived_on_db:
            self.recived_on_db = now_ist
    
        if self.pk:  # This means the object already exists, so we can compare changes
            old_instance = DICOMData.objects.get(pk=self.pk)
    
            # Check if radiologist is being assigned
            # if not old_instance.radiologist.exists() and self.radiologist.exists():
            #     self.radiologist_assigned_at = now().astimezone(india_tz)
    
            # Check if isDone is changing from False to True
            if not old_instance.isDone and self.isDone:
                self.marked_done_at = now_ist

            # notes updated
            if old_instance.notes != self.notes:
                self.notes_modified_at = now_ist
    
        super(DICOMData, self).save(*args, **kwargs)


    # def save(self, *args, **kwargs):
    #     if not self.recived_on_db:  # Set the timestamp only if it isn't already set
    #         india_tz = pytz.timezone("Asia/Kolkata")
    #         self.recived_on_db = now().astimezone(india_tz)
    #     super(DICOMData, self).save(*args, **kwargs)

    

    def __str__(self):
        return str(self.patient_name)
    

    @staticmethod
    def get_notes_by_study_id(study_id):
        try:
            dicom_data = DICOMData.objects.filter(study_id=study_id).first()
            if dicom_data:
                return dicom_data.notes
            return "No notes available for this study."
        except Exception as e:
            raise Exception(f"Error fetching notes: {str(e)}")
        

    # Signal to update `radiologist_assigned_at` when radiologist M2M field is changed
@receiver(m2m_changed, sender=DICOMData.radiologist.through)
def update_radiologist_assigned_at(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        if not instance.radiologist_assigned_at:
            india_tz = pytz.timezone("Asia/Kolkata")
            instance.radiologist_assigned_at = now().astimezone(india_tz)
            instance.save()    




class DICOMFile(models.Model):
    dicom_data = models.ForeignKey(DICOMData, related_name='dicom_files', on_delete=models.CASCADE)
    dicom_file = models.FileField(upload_to='dicom_files/', storage=S3Boto3Storage())
    #dicom_file = models.CharField(max_length=500)

class JPEGFile(models.Model):
    dicom_data = models.ForeignKey(DICOMData, related_name='jpeg_files', on_delete=models.CASCADE)
    jpeg_file = models.ImageField(upload_to='jpeg_files/', storage=S3Boto3Storage())
    #jpeg_file = models.CharField(max_length=500)


# class PatientHistoryFile(models.Model):
#     dicom_data = models.ForeignKey(DICOMData, related_name='history_files', on_delete=models.CASCADE)
#     history_file = models.FileField(upload_to='patient_history_files/',storage=S3Boto3Storage(), null=True)
#     # history_file = models.FileField(upload_to='patient_history_files/', null=True, default=None, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)   


class PatientHistoryFile(models.Model):
    dicom_data = models.ForeignKey(DICOMData, related_name='history_files', on_delete=models.CASCADE)
    history_file = models.FileField(upload_to='patient_history_files/', storage=S3Boto3Storage(), null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Store original file state when instance is loaded
        self._original_history_file = self.history_file

    def save(self, *args, **kwargs):
        india_tz = pytz.timezone("Asia/Kolkata")
        now_ist = now().astimezone(india_tz)
        
        # Always update uploaded_at for new instances
        if not self.pk:
            self.uploaded_at = now_ist
        else:
            # Compare current file with original file
            if self.history_file != self._original_history_file:
                self.uploaded_at = now_ist
        
        super().save(*args, **kwargs)
        # Update original file reference after save
        self._original_history_file = self.history_file





class PatientReport(models.Model):
    dicom_data = models.ForeignKey(DICOMData, related_name='patient_reports', on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='patient_reports/')
    report_title = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_title or 'Unnamed Report'} for {self.dicom_data.patient_name}"
