
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from api.models.DICOMData import DICOMData, PatientHistoryFile

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




@csrf_exempt
@require_http_methods(["POST"])
def update_dicom(request, dicom_id):
    try:
        dicom = DICOMData.objects.get(id=dicom_id)
        data = json.loads(request.body)

        # List of allowed editable fields
        editable_fields = [
            "patient_name", "patient_id", "age", "gender",
            "study_description", "body_part_examined", "mlc",
            "urgent", "vip", "notes", "referring_doctor_name",
            "whatsapp_number", "contrast_used", "is_follow_up",
            "imaging_views", "inhouse_patient", "email"
        ]

        # Update only the fields present in request
        for field in editable_fields:
            if field in data:
                setattr(dicom, field, data[field])

        dicom.save()
        return JsonResponse({"success": True, "message": "Updated successfully"})

    except DICOMData.DoesNotExist:
        return JsonResponse({"success": False, "message": "DICOM record not found"}, status=404)
    except Exception as e:
        print("Update error:", e)  # debug
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

