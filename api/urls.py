from django.urls import path
from .views import fetch_tat_counters,server_data,dicom_list,update_dicom,upload_history_file,fetch_patient_reports,get_all_coordinators,fetch_radiologists,assign_radiologist,replace_radiologist
from .views import fetch_body_parts


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

]
