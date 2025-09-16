
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from api.models.DICOMData import DICOMData

# List all DICOM records
def dicom_list(request):
    data = DICOMData.objects.all().values(
        "id",  # include id for updating
        "patient_name",
        "patient_id",
        "age",
        "gender",
        "recived_on_db",
        "Modality",
        "study_id",
        "study_description",
        "isDone",
        "NonReportable",
        "Mlc",
        "urgent",
        "vip",
        "notes",
        "radiologist",
        "body_part_examined",
        "referring_doctor_name",
        "whatsapp_number",
        "marked_done_at",
        "contrast_used",
        "is_follow_up",
        "imaging_views",  # new field
        "inhouse_patient",
        "email"
    )
    return JsonResponse(list(data), safe=False)


# Update age and gender for a DICOM record
@csrf_exempt
@require_http_methods(["POST"])
def update_dicom(request, dicom_id):
    try:
        dicom = DICOMData.objects.get(id=dicom_id)
        data = json.loads(request.body)

        
        # Update all fields safely
        dicom.patient_name = data.get("patient_name", dicom.patient_name)
        dicom.patient_id = data.get("patient_id", dicom.patient_id)
        dicom.age = data.get("age", dicom.age)
        dicom.gender = data.get("gender", dicom.gender)
        dicom.study_description = data.get("study_description", dicom.study_description)
        dicom.body_part_examined = data.get("body_part_examined", dicom.body_part_examined)
        dicom.mlc = data.get("mlc", dicom.mlc)
        dicom.urgent = data.get("urgent", dicom.urgent)
        dicom.vip = data.get("vip", dicom.vip)
        dicom.notes = data.get("notes", dicom.notes)
        dicom.referring_doctor_name = data.get("referring_doctor_name", dicom.referring_doctor_name)
        dicom.whatsapp_number = data.get("whatsapp_number", dicom.whatsapp_number)
        dicom.contrast_used = data.get("contrast_used", dicom.contrast_used)
        dicom.is_follow_up = data.get("is_follow_up", dicom.is_follow_up)
        dicom.imaging_views = data.get("imaging_views", dicom.imaging_views)  # JSONField / CharField
        dicom.inhouse_patient = data.get("inhouse_patient", dicom.inhouse_patient)
        dicom.email = data.get("email", dicom.email)

        dicom.save()
        return JsonResponse({"success": True, "message": "Updated successfully"})
    except DICOMData.DoesNotExist:
        return JsonResponse({"success": False, "message": "DICOM record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
    



    
# Upload Patient History File
@csrf_exempt
@require_http_methods(["POST"])
def upload_history_file(request, dicom_id):
    try:
        dicom = DICOMData.objects.get(id=dicom_id)

        if "history_file" not in request.FILES:
            return JsonResponse({"success": False, "message": "No history_file provided"}, status=400)

        history_file = request.FILES["history_file"]

        history_instance = PatientHistoryFile.objects.create(
            dicom_data=dicom,
            history_file=history_file
        )

        return JsonResponse({
            "success": True,
            "message": "History file uploaded successfully",
            "file_url": history_instance.history_file.url if history_instance.history_file else None,
            "uploaded_at": history_instance.uploaded_at
        })

    except DICOMData.DoesNotExist:
        return JsonResponse({"success": False, "message": "DICOM record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


# Fetch all Patient Reports of a patient
@csrf_exempt
@require_http_methods(["GET"])
def fetch_patient_reports(request, dicom_id):
    try:
        dicom = DICOMData.objects.get(id=dicom_id)
        reports = dicom.patient_reports.all()

        data = [{
            "id": report.id,
            "title": report.report_title,
            "file_url": report.report_file.url if report.report_file else None,
            "uploaded_at": report.uploaded_at
        } for report in reports]

        return JsonResponse({"success": True, "reports": data}, safe=False)

    except DICOMData.DoesNotExist:
        return JsonResponse({"success": False, "message": "DICOM record not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

