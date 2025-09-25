from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from api.models.patientdetails import PatientDetails
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

# ---------------- Fetch ECG Patients ----------------
def get_ecg_patients(request):
    patients = PatientDetails.objects.all().order_by('-id')

    # Pagination
    paginator = Paginator(patients, 50)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    patients_data = []
    for p in page_obj:
        test_date = p.TestDate if p.TestDate else None
        report_date = p.ReportDate if p.ReportDate else None

        # Fix Allocated field
        allocated_name = None
        if getattr(p, 'cardiologist', None):
            allocated_name = p.cardiologist.user.get_full_name() or p.cardiologist.user.username

        patients_data.append({
            "id": p.id,
            "PatientId": p.PatientId,
            "PatientName": p.PatientName,
            "Age": p.age,
            "Gender": p.gender,
            "HeartRate": p.HeartRate,
            "Date": test_date,
            "ReportDate": report_date,
            "Allocated": allocated_name,
            "City": p.location.city.name if getattr(p, 'location', None) and getattr(p.location, 'city', None) else None,
            "Location": p.location.name if getattr(p, 'location', None) else None,
            "MarkAsUrgent": p.urgent,
            "MarkForNonReported": p.NonReportable,
            "isDone": p.isDone,
            "Action": "view"
        })

    return JsonResponse({
        "patients": patients_data,
        "total": paginator.count,
        "page": int(page_number),
        "num_pages": paginator.num_pages
    }, safe=False)



# ---------------- Update Patient Status (Urgent / Non-Reported) ----------------
@csrf_exempt
@require_http_methods(["POST"])
def update_patient_status(request, patient_id):
    try:
        data = json.loads(request.body.decode('utf-8'))
        action = data.get("action")

        patient = PatientDetails.objects.get(id=patient_id)

        if action == "mark_urgent":
            patient.urgent = True
            patient.save()
            return JsonResponse({"success": True, "message": "Patient marked as urgent"})

        elif action == "unmark_urgent":
            patient.urgent = False
            patient.save()
            return JsonResponse({"success": True, "message": "Patient unmarked as urgent"})

        elif action == "mark_non_reported":
            patient.NonReportable = True
            patient.save()
            return JsonResponse({"success": True, "message": "Patient marked as non-reported"})

        elif action == "unmark_non_reported":
            patient.NonReportable = False
            patient.save()
            return JsonResponse({"success": True, "message": "Patient unmarked as non-reported"})

        else:
            return JsonResponse({"success": False, "message": "Invalid action"}, status=400)

    except PatientDetails.DoesNotExist:
        return JsonResponse({"success": False, "message": "Patient not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)
