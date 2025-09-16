from django.urls import path
from .views import fetch_tat_counters,server_data,dicom_list,update_dicom,upload_history_file,fetch_patient_reports


urlpatterns = [
    path('fetch-tat-counters/', fetch_tat_counters),
    path('serverdata/', server_data),
    path('dicom-list/', dicom_list),
     path("update-dicom/<int:dicom_id>/", update_dicom, name="update-dicom"),
     # Patient History Files
    path("upload-historyfile/<int:dicom_id>/", upload_history_file, name="upload-historyfile"),

    # Patient Reports
    path("fetch-reports/<int:dicom_id>/", fetch_patient_reports, name="fetch-reports"),

]
