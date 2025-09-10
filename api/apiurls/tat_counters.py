from django.http import JsonResponse
from api.models.DICOMData import DICOMData
from api.models.Client import ServiceTATSetting, Institution
from datetime import datetime, timedelta
import pytz

def fetch_tat_counters(request):
    dicoms = DICOMData.objects.all()
    data = []
    now = datetime.now(pytz.utc)

    for dicom in dicoms:
        institution_name = dicom.institution_name  # Stored as string
        service_name = dicom.Modality
        upload_time = dicom.notes_modified_at
        is_urgent = dicom.urgent

        if not (institution_name and service_name and upload_time):
            continue  # Skip incomplete records

        # Fetch Institution object using the name string
        try:
            institution_obj = Institution.objects.get(name__iexact=institution_name)
        except Institution.DoesNotExist:
            institution_obj = None

        # Fetch TAT settings using the Institution object
        try:
            tat_setting = ServiceTATSetting.objects.get(
                institution=institution_obj,
                service__name__iexact=service_name
            )
        except ServiceTATSetting.DoesNotExist:
            tat_setting = None

        # Determine TAT hours
        hour = upload_time.astimezone(pytz.utc).hour

        if is_urgent:
            tat_hours = tat_setting.urgent_tat_hours if tat_setting else 0
        elif 0 <= hour <= 6:
            tat_hours = tat_setting.night_tat_hours if tat_setting else 0
        else:
            tat_hours = tat_setting.normal_tat_hours if tat_setting else 0

        

  
        deadline = upload_time + timedelta(hours=tat_hours)
        time_remaining_seconds = int((deadline - now).total_seconds())

        if time_remaining_seconds > 0:
            overdue_seconds = 0
        else:
            overdue_seconds = abs(time_remaining_seconds)

        print(f"[{dicom.patient_id}] Overdue Seconds: {overdue_seconds}")
        

        data.append({
            'patient_name': dicom.patient_name or "Unknown",
            'patient_id': dicom.patient_id or "Unknown",
            'modality': dicom.Modality or "Unknown",
            'institution_name': institution_name or "None",
            # 'tat_breached': tat_breached,
            'overdue_seconds': overdue_seconds,   # ✅ SEND TO FRONTEND
            'tat_breached': time_remaining_seconds <= 0,
            'time_remaining': time_remaining_seconds,
            'age': dicom.age or "Unknown",
            'gender':dicom.gender or "Unknown",
            'received_on_db': dicom.recived_on_db.isoformat() if dicom.recived_on_db else None,
            'clinical_notes': dicom.notes or "No notes",
            'study_description': dicom.study_description or "No description",
             'is_done': dicom.isDone,   # ✅ Add this line
             'Mlc': dicom.Mlc,   # ✅ Add this line
             'urgent': dicom.urgent,   # ✅ Add this line   
                'vip': dicom.vip,   # ✅ Add this line
              # Add history files URLs here:
    'history_files': [
        request.build_absolute_uri(history_file.history_file.url)
        for history_file in dicom.history_files.all()
        if history_file.history_file  # Ensure file exists
    ],
    'patient_reports': [
    {
        'title': report.report_title or "Unnamed Report",
        'url': request.build_absolute_uri(report.report_file.url)
    }
    for report in dicom.patient_reports.all()
    if report.report_file
]

            

        })



    return JsonResponse(data, safe=False)
