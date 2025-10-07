from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from api.models.patientdetails import PatientDetails, Location
from .serializerss import PatientDetailsSerializer, LocationSerializer
from api.models.personalinfo import PersonalInfo  
from datetime import datetime
import pytz  
from rest_framework.permissions import AllowAny

class LocationListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response({
            "success": True,
            "locations": serializer.data
        }, status=status.HTTP_200_OK)


class PatientListAPIView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        username = request.query_params.get('username')

        if username:
            cardiologist = PersonalInfo.objects.filter(user__username=username).first()
        else:
            cardiologist = PersonalInfo.objects.filter(user=request.user).first()

        if not cardiologist:
            return Response({"detail": "Invalid or missing cardiologist"}, status=status.HTTP_404_NOT_FOUND)


        patients = PatientDetails.objects.filter(
            cardiologist=cardiologist,
            isDone=False,
            NonReportable=False
        )


        location_name = request.query_params.get('location')
        test_date = request.query_params.get('test_date')
        search = request.query_params.get('search')

        if location_name:
            patients = patients.filter(location__name__icontains=location_name)
        if test_date:
            patients = patients.filter(TestDate=test_date)
        if search:
            patients = patients.filter(
                Q(PatientName__icontains=search) |
                Q(PatientId__icontains=search) |
                Q(TestDate__icontains=search)
            )

        serializer = PatientDetailsSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDetailAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        username = request.query_params.get('username')

        if username:
            cardiologist = PersonalInfo.objects.filter(user__username=username).first()
        else:
            cardiologist = PersonalInfo.objects.filter(user=request.user).first()

        if not cardiologist:
            return Response({"detail": "Invalid or missing cardiologist"}, status=status.HTTP_404_NOT_FOUND)

        try:
            patient = PatientDetails.objects.get(pk=pk, cardiologist=cardiologist)
        except PatientDetails.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = PatientDetailsSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GreetingAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        ist = pytz.timezone('Asia/Kolkata')
        current_hour = datetime.now(ist).hour

        if 0 <= current_hour < 12:
            greeting = "Good morning"
        elif 12 <= current_hour < 16:
            greeting = "Good afternoon"
        else:
            greeting = "Good evening"

        return Response({"greeting": greeting, "hour": current_hour})
