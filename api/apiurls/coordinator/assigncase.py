# api/views/dicom_views.py

from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json

from api.models.DICOMData import DICOMData
from api.models.personalinfo import PersonalInfo

@csrf_exempt
def assign_radiologist(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dicom_id = body.get("dicom_id")
            radiologist_user_id = body.get("radiologist_user_id")  # <-- frontend sends user_id now

            if not dicom_id or not radiologist_user_id:
                return JsonResponse({"error": "dicom_id and radiologist_user_id are required"}, status=400)

            # Fetch DICOMData
            dicom = DICOMData.objects.get(id=dicom_id)

            # Fetch PersonalInfo corresponding to the user_id
            radiologist = PersonalInfo.objects.get(user_id=radiologist_user_id)

            # Assign radiologist (ManyToMany → keep old ones)
            dicom.radiologist.add(radiologist)
            dicom.radiologist_assigned_at = now()
            dicom.save()

            # Get all assigned radiologists with linked User info
            all_radiologists = dicom.radiologist.all().values(
                "id",
                "user__first_name",
                "user__last_name",
                "user__email"
            )

            return JsonResponse({
                "message": "Radiologist assigned successfully",
                "dicom_id": dicom.id,
                "patient_name": dicom.patient_name,
                "assigned_radiologists": list(all_radiologists),
                "last_assigned_at": dicom.radiologist_assigned_at
            }, status=200)

        except DICOMData.DoesNotExist:
            return JsonResponse({"error": "DICOMData not found"}, status=404)
        except PersonalInfo.DoesNotExist:
            return JsonResponse({"error": "Radiologist not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)





@csrf_exempt
def replace_radiologist(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)

            dicom_id = body.get("dicom_id")
            radiologist_user_id = body.get("radiologist_user_id")  # <-- frontend sends user_id now

            if not dicom_id or not radiologist_user_id:
                return JsonResponse({"error": "dicom_id and radiologist_user_id are required"}, status=400)

            # Fetch DICOMData
            dicom = DICOMData.objects.get(id=dicom_id)

            # Fetch PersonalInfo corresponding to the user_id
            radiologist = PersonalInfo.objects.get(user_id=radiologist_user_id)

            # Assign radiologist (ManyToMany → keep old ones)
            dicom.radiologist.clear()   # remove previous assignments
            dicom.radiologist.add(radiologist)

            dicom.radiologist_assigned_at = now()
            dicom.save()

            # Get all assigned radiologists with linked User info
            all_radiologists = dicom.radiologist.all().values(
                "id",
                "user__first_name",
                "user__last_name",
                "user__email"
            )

            return JsonResponse({
                "message": "Radiologist assigned successfully",
                "dicom_id": dicom.id,
                "patient_name": dicom.patient_name,
                "assigned_radiologists": list(all_radiologists),
                "last_assigned_at": dicom.radiologist_assigned_at
            }, status=200)

        except DICOMData.DoesNotExist:
            return JsonResponse({"error": "DICOMData not found"}, status=404)
        except PersonalInfo.DoesNotExist:
            return JsonResponse({"error": "Radiologist not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)
