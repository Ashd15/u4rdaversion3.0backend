import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group, User
from api.models.patientdetails import PatientDetails
from api.models.personalinfo import PersonalInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def manage_cardiologist(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "POST method required"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "Invalid JSON"}, status=400)

    patient_ids = data.get("patient_ids", [])
    cardiologist_email = data.get("cardiologist_email")
    action = data.get("action")  # "assign" or "replace"

    if not patient_ids or not cardiologist_email or action not in ["assign", "replace"]:
        return JsonResponse({"success": False, "error": "Missing or invalid data"}, status=400)

    # Get cardiologist user
    try:
        group = Group.objects.get(name='cardiologist')
        user = group.user_set.get(email=cardiologist_email)
        cardiologist = PersonalInfo.objects.get(user=user)
    except (Group.DoesNotExist, User.DoesNotExist, PersonalInfo.DoesNotExist):
        return JsonResponse({"success": False, "error": "Invalid cardiologist"}, status=400)

    # Get patients
    patients = PatientDetails.objects.filter(id__in=patient_ids)
    if not patients.exists():
        return JsonResponse({"success": False, "error": "No valid patients found"}, status=404)

    updated_patients = []
    for patient in patients:
        if action == "assign" and patient.cardiologist is None:
            patient.cardiologist = cardiologist
            patient.save()
            updated_patients.append(patient.id)
        elif action == "replace":
            patient.cardiologist = cardiologist
            patient.save()
            updated_patients.append(patient.id)

    return JsonResponse({
        "success": True,
        "action": action,
        "updated_patients": updated_patients
    })

@csrf_exempt
def get_cardiologists(request):
    if request.method != "GET":
        return JsonResponse({"success": False, "error": "GET method required"}, status=405)

    try:
        group = Group.objects.get(name='cardiologist')
        users = group.user_set.all()
        doctors = []
        for user in users:
            try:
                info = PersonalInfo.objects.get(user=user)
                doctors.append({
                    "id": info.id,
                    "name": user.get_full_name() or user.username,
                    "email": user.email,
                    "specialization": getattr(info, "specialization", "")
                })
            except PersonalInfo.DoesNotExist:
                continue
        return JsonResponse({"success": True, "cardiologists": doctors})
    except Group.DoesNotExist:
        return JsonResponse({"success": False, "cardiologists": []})