from rest_framework import serializers
from api.models.Client import Client, Institution 
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group
from django.utils.timezone import localtime, timezone
from api.models.DICOMData import DICOMData, PatientHistoryFile  
from api.models.Client import ServiceTATSetting, Service, Institution

import pytz

IST = pytz.timezone('Asia/Kolkata')

def to_ist(dt):
    return localtime(dt, IST) if dt else None

class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name'] 


class ClientSerializer(serializers.ModelSerializer):
    institutions = InstitutionSerializer(many=True, read_only=True)

    institution_names = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'location': {'required': False, 'allow_null': True},
            'upload_header': {'required': False, 'allow_null': True},
            'upload_footer': {'required': False, 'allow_null': True},
        }

    def _extract_institution_names(self, validated_data):
        inst_names = validated_data.pop('institution_names', None)
        if inst_names is None:
            inst_names = validated_data.pop('institutions', None)
        return inst_names

    def create(self, validated_data):
        inst_names = self._extract_institution_names(validated_data)
        client = super().create(validated_data)
        if inst_names:
            institutions = [Institution.objects.get_or_create(name=n.strip())[0] for n in inst_names]
            client.institutions.set(institutions)
        return client

    def update(self, instance, validated_data):
        inst_names = self._extract_institution_names(validated_data)
        client = super().update(instance, validated_data)
        if inst_names is not None:
            institutions = [Institution.objects.get_or_create(name=n.strip())[0] for n in inst_names]
            client.institutions.set(institutions)
        return client


class PatientHistoryFileSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.SerializerMethodField()

    class Meta:
        model = PatientHistoryFile
        fields = ['id', 'history_file', 'uploaded_at']

    def get_uploaded_at(self, obj):
        return localtime(obj.uploaded_at).strftime('%Y-%m-%d %H:%M:%S') if obj.uploaded_at else None


class DICOMDataSerializer(serializers.ModelSerializer):
    recived_on_db = serializers.SerializerMethodField()
    study_time = serializers.SerializerMethodField()
    notes_modified_at = serializers.SerializerMethodField()
    radiologist_assigned_at = serializers.SerializerMethodField()
    marked_done_at = serializers.SerializerMethodField()
    history_files = PatientHistoryFileSerializer(many=True, read_only=True)
    radiologists = serializers.SerializerMethodField()

    class Meta:
        model = DICOMData
        fields = [
            'id', 'patient_name', 'patient_id', 'age', 'gender',
            'study_date', 'study_time', 'recived_on_db', 'Modality',
            'urgent', 'isDone', 'location', 'institution_name',
            'study_description', 'notes', 'notes_modified_at',
            'history_files', 'radiologist_assigned_at', 'marked_done_at', 
            'radiologists'
        ]

    def _to_ist(self, value):
        return localtime(value, IST).strftime('%Y-%m-%d %H:%M:%S') if value else None

    def get_study_time(self, obj):
 
       if not obj.study_time:
            return None

       t = obj.study_time
       total_seconds = t.hour * 3600 + t.minute * 60 + t.second + (5 * 3600 + 30 * 60)
       total_seconds %= 24 * 3600  

       hour = total_seconds // 3600
       minute = (total_seconds % 3600) // 60
       second = total_seconds % 60

       return f"{hour:02}:{minute:02}:{second:02}"


    def get_recived_on_db(self, obj):
        return self._to_ist(obj.recived_on_db)

    def get_notes_modified_at(self, obj):
        return self._to_ist(obj.notes_modified_at)

    def get_radiologist_assigned_at(self, obj):
        return self._to_ist(obj.radiologist_assigned_at)

    def get_marked_done_at(self, obj):
        return self._to_ist(obj.marked_done_at)

    def get_radiologists(self, obj):
        return [str(r) for r in obj.radiologist.all()]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name']



class ServiceTATSettingSerializer(serializers.ModelSerializer):
    institution_name = serializers.CharField(write_only=True)
    service_name = serializers.CharField(write_only=True)
    institution = InstitutionSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceTATSetting
        fields = [
            'id',
            'institution', 'institution_name',  
            'service', 'service_name',           
            'night_tat_hours', 'normal_tat_hours', 'urgent_tat_hours'
        ]

    def create(self, validated_data):
        institution_name = validated_data.pop('institution_name')
        service_name = validated_data.pop('service_name')

        institution = Institution.objects.get(name=institution_name)
        service = Service.objects.get(name=service_name)

        return ServiceTATSetting.objects.create(
            institution=institution,
            service=service,
            **validated_data
        )

    def update(self, instance, validated_data):
        if 'institution_name' in validated_data:
            institution_name = validated_data.pop('institution_name')
            instance.institution = Institution.objects.get(name=institution_name)

        if 'service_name' in validated_data:
            service_name = validated_data.pop('service_name')
            instance.service = Service.objects.get(name=service_name)

        return super().update(instance, validated_data)
