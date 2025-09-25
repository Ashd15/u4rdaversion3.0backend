from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.timezone import now
from api.models.patientdetails import PatientDetails
from api.models.Date import Date
from api.models.ecg_client import ECGClient

@csrf_exempt
def upload_patient_ecg_api(request):
    user = request.user
    query = request.GET.get("q", "")

    # GET: fetch patients
    if request.method == "GET":
        try:
            ecg_client = ECGClient.objects.get(user=user)
            patients = PatientDetails.objects.filter(location=ecg_client.location)
        except ECGClient.DoesNotExist:
            patients = PatientDetails.objects.none()

        if query:
            patients = patients.filter(
                Q(PatientId__icontains=query) | Q(PatientName__icontains=query)
            )

        patients = patients.order_by("-id")

        paginator = Paginator(patients, 10)
        page_number = request.GET.get("page", 1)
        page_obj = paginator.get_page(page_number)

        patients_list = [
            {
                "id": p.id,
                "PatientId": p.PatientId,
                "PatientName": p.PatientName,
                "age": p.age,
                "gender": p.gender,
                "HeartRate": p.HeartRate,
                "PRInterval": p.PRInterval,
                "TestDate": p.TestDate,
                "ReportDate": p.ReportDate,
                "location": p.location.name if p.location else None,
                "image": p.image.url if p.image else None,
            }
            for p in page_obj
        ]

        return JsonResponse({
            "patients": patients_list,
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
            "total_patients": paginator.count
        })

    # POST: create patient (with file uploads)
    elif request.method == "POST":
        patient_id = request.POST.get("PatientId")
        patient_name = request.POST.get("PatientName")
        age = request.POST.get("age", "")
        gender = request.POST.get("gender", "")

        if not patient_id or not patient_name:
            return JsonResponse({"error": "PatientId and PatientName are required"}, status=400)

        patient = PatientDetails(
            PatientId=patient_id,
            PatientName=patient_name,
            age=age,
            gender=gender,
            HeartRate=request.POST.get("HeartRate"),
            PRInterval=request.POST.get("PRInterval")
        )

        today_str = now().strftime("%d-%m-%Y")
        patient.TestDate = today_str
        patient.ReportDate = today_str

        try:
            ecg_client = ECGClient.objects.get(user=user)
            patient.location = ecg_client.location
        except ECGClient.DoesNotExist:
            patient.location = None

        date_obj, created = Date.objects.get_or_create(date_field=now().date(), location=patient.location)
        patient.date = date_obj

        if "image" in request.FILES:
            patient.image = request.FILES["image"]

        patient.save()

        return JsonResponse({
            "id": patient.id,
            "PatientId": patient.PatientId,
            "PatientName": patient.PatientName,
            "age": patient.age,
            "gender": patient.gender,
            "HeartRate": patient.HeartRate,
            "PRInterval": patient.PRInterval,
            "TestDate": patient.TestDate,
            "ReportDate": patient.ReportDate,
            "location": patient.location.name if patient.location else None,
            "image": patient.image.url if patient.image else None
        }, status=201)
