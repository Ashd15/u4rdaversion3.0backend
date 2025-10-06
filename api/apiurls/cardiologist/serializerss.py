from rest_framework import serializers
from api.models.patientdetails import PatientDetails, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'technician_name', 'city']

class PatientDetailsSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    image = serializers.ImageField(use_url=True, required=False)
    reportimage = serializers.FileField(use_url=True, required=False)

    class Meta:
        model = PatientDetails
        fields = [
            'id', 'PatientId', 'PatientName', 'age', 'gender', 'HeartRate',
            'PRInterval', 'TestDate', 'ReportDate', 'urgent', 'NonReportable',
            'isDone', 'status', 'location', 'image', 'reportimage'
        ]
