from django.urls import path
from .views import fetch_tat_counters,server_data,dicom_list,update_dicom,upload_history_file,fetch_patient_reports
from .views import get_all_coordinators,fetch_radiologists,assign_radiologist,replace_radiologist,fetch_body_parts
from .views import upload_ecg_api,update_patient,ecg_stats_api, get_locations,get_ecg_patients,update_patient_status,manage_cardiologist,get_cardiologists,upload_patient_ecg_api
from django.conf import settings


urlpatterns = [
    path('fetch-tat-counters/', fetch_tat_counters),
    path('serverdata/', server_data),
    path('dicom-list/', dicom_list),
     path("update-dicom/<int:dicom_id>/", update_dicom, name="update-dicom"),
     # Patient History Files
    path("upload-historyfile/<int:dicom_id>/", upload_history_file, name="upload-historyfile"),

    # Patient Reports
    path("fetch-reports/<int:dicom_id>/", fetch_patient_reports, name="fetch-reports"),
    path('coordinators/', get_all_coordinators, name='get_all_coordinators'),
    path('radiologists/', fetch_radiologists, name='fetch_radiologists'),
    path('assign-radiologist/', assign_radiologist, name='assign_radiologist'),
    path('replace-radiologist/', replace_radiologist, name='replace_radiologist'),
    path("body-parts/", fetch_body_parts, name="fetch_body_parts"),

    # add ecg upload path
     path("upload-ecg/", upload_ecg_api, name="upload_ecg_api"),
     path("ecg_patients/", get_ecg_patients, name="get_ecg_patients"),
     path("ecg_patients/<int:patient_id>/update-status/", update_patient_status, name="update_patient_status"),
     path('get-locations/', get_locations, name='get_locations'),
     path('manage-cardiologist/', manage_cardiologist, name='manage_cardiologist'),
     path('cardiologists/', get_cardiologists, name='get_cardiologists'),
     path("ecg_patients/<int:patient_id>/", update_patient, name="update_patient"),
     path('ecg_stats/', ecg_stats_api, name='ecg_stats_api'),
     path('upload-patient-ecgs/', upload_patient_ecg_api, name='upload_patient_ecg_api'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
