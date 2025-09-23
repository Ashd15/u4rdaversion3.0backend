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
        institution_name = dicom.institution_name
        service_name = dicom.Modality
        upload_time = dicom.notes_modified_at
        is_urgent = dicom.urgent

        if not (institution_name and service_name and upload_time):
            continue  # Skip incomplete records

        # Fetch Institution object
        try:
            institution_obj = Institution.objects.get(name__iexact=institution_name)
        except Institution.DoesNotExist:
            institution_obj = None

        # Fetch TAT settings
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

        # Calculate deadline
        deadline = upload_time + timedelta(hours=tat_hours)

        if dicom.isDone and dicom.marked_done_at:
            # Use marked_done_at to calculate remaining or overdue time
            actual_done_time = dicom.marked_done_at
            time_remaining_seconds = int((deadline - actual_done_time).total_seconds())
        else:
            # Use current time if not done
            time_remaining_seconds = int((deadline - now).total_seconds())

        if time_remaining_seconds > 0:
            overdue_seconds = 0
        else:
            overdue_seconds = abs(time_remaining_seconds)

        tat_breached = time_remaining_seconds <= 0


        data.append({
    "id": dicom.id,
    "patient_name": dicom.patient_name or "Unknown",
    "patient_id": dicom.patient_id or "Unknown",
    "age": dicom.age or "Unknown",
    "gender": dicom.gender or "Unknown",
    "study_date": dicom.study_date or "Unknown",
    "study_time": dicom.study_time.isoformat() if dicom.study_time else None,
    "recived_on_orthanc": dicom.recived_on_orthanc.isoformat() if dicom.recived_on_orthanc else None,
    "recived_on_db": dicom.recived_on_db.isoformat() if dicom.recived_on_db else None,
    "modality": dicom.Modality or "Unknown",
    "study_id": dicom.study_id or "Unknown",
    "study_description": dicom.study_description or "No description",
    "is_done": dicom.isDone,
    "NonReportable": dicom.NonReportable,
    "Mlc": dicom.Mlc,
    "urgent": dicom.urgent,
    "vip": dicom.vip,
    "twostepcheck": dicom.twostepcheck,
    "notes": dicom.notes or "No notes",
    "location": dicom.location or "Unknown",
    "radiologist": [r.name for r in dicom.radiologist.all()],
    "corporatecoordinator": [c.name for c in dicom.corporatecoordinator.all()],
    "body_part_examined": dicom.body_part_examined or "Unknown",
    "institution_name": dicom.institution_name or "None",
    "referring_doctor_name": dicom.referring_doctor_name or "None",
    "whatsapp_number": dicom.whatsapp_number or "Unknown",
    "radiologist_assigned_at": dicom.radiologist_assigned_at.isoformat() if dicom.radiologist_assigned_at else None,
    "marked_done_at": dicom.marked_done_at.isoformat() if dicom.marked_done_at else None,
    "notes_modified_at": dicom.notes_modified_at.isoformat() if dicom.notes_modified_at else None,
    "contrast_used": dicom.contrast_used,
    "is_follow_up": dicom.is_follow_up,
    "imaging_views": dicom.imaging_views or "None",
    "inhouse_patient": dicom.inhouse_patient,
    "email": dicom.email or "Unknown",
    
    # Extra calculated fields you already had
    "overdue_seconds": overdue_seconds,
    "tat_breached": tat_breached,
    "time_remaining": time_remaining_seconds,

    # Related files
    "history_files": [
        request.build_absolute_uri(f.history_file.url)
        for f in dicom.history_files.all() if f.history_file
    ],
    "patient_reports": [
        {
            "title": r.report_title or "Unnamed Report",
            "url": request.build_absolute_uri(r.report_file.url)
        }
        for r in dicom.patient_reports.all() if r.report_file
    ]
})


    return JsonResponse(data, safe=False)