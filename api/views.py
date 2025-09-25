from api.apiurls.doctor.tat_counters import fetch_tat_counters
# from pyorthanc import Orthanc
from api.apiurls.client.clientdata import dicom_list,update_dicom,upload_history_file,fetch_patient_reports
from api.apiurls.doctor.serverdata import server_data
from api.apiurls.coordinator.coordinator import get_all_coordinators
from api.apiurls.coordinator.radiologistlist import fetch_radiologists
from api.apiurls.coordinator.assigncase import assign_radiologist,replace_radiologist
from api.apiurls.bodypart.bodypart import fetch_body_parts
from api.apiurls.ECG.client_ecg import upload_patient_ecg_api
from api.apiurls.ECG.Manage_Cardiologist import manage_cardiologist,get_cardiologists
from api.apiurls.ECG.ecg_upload import upload_ecg_api,update_patient,ecg_stats_api, get_locations
from api.apiurls.ECG.ecg_get_views import get_ecg_patients,update_patient_status

