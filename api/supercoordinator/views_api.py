from django.db.models import Q
from datetime import datetime, time as dt_time
from pyparsing import Group
import pytz
from django.utils import timezone

from . import serializers  
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from .serializers import ClientSerializer, DICOMDataSerializer, ServiceTATSettingSerializer, ServiceSerializer, InstitutionSerializer
from api.models.DICOMData import DICOMData
from api.models.Client import Client, Institution, ServiceTATSetting, Service
import pandas as pd
from io import BytesIO
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework.views import APIView

IST = pytz.timezone('Asia/Kolkata')

def apply_filters_from_body(qs, data):
    name = data.get('name', '').strip()
    start_date = data.get('start_date', '').strip()
    end_date = data.get('end_date', '').strip()
    received_start_date = data.get('received_start_date', '').strip()
    received_end_date = data.get('received_end_date', '').strip()

    radiologist_names = data.get('radiologist', [])
    if isinstance(radiologist_names, str):
        radiologist_names = [radiologist_names]

    try:
        radiologist_names = list(map(int, radiologist_names))
    except Exception:
        radiologist_names = []

    institutions = data.get('institution', [])
    if isinstance(institutions, str):
        institutions = [institutions]

    status = data.get('status', '').strip()
    selected_modalities = data.get('Modality', [])
    if isinstance(selected_modalities, str):
        selected_modalities = [selected_modalities]

    filters = Q()

    if name:
        filters &= Q(patient_name__iexact=name)

    if start_date and end_date:
        try:
            sd = datetime.strptime(start_date, "%Y-%m-%d").date()
            ed = datetime.strptime(end_date, "%Y-%m-%d").date()
            start_yyyymmdd = sd.strftime("%Y%m%d")
            end_yyyymmdd = ed.strftime("%Y%m%d")

            qs = qs.extra(
                where=[
                    "SUBSTR(study_date, 7, 4) || SUBSTR(study_date, 4, 2) || SUBSTR(study_date, 1, 2) BETWEEN %s AND %s"
                ],
                params=[start_yyyymmdd, end_yyyymmdd]
            )
        except ValueError:
            pass

    if received_start_date and received_end_date:
        try:
            rstart = datetime.strptime(received_start_date, "%Y-%m-%d").date()
            rend = datetime.strptime(received_end_date, "%Y-%m-%d").date()
            start_dt_ist = IST.localize(datetime.combine(rstart, dt_time.min))
            end_dt_ist = IST.localize(datetime.combine(rend, dt_time(23, 59, 59)))
            start_dt_utc = start_dt_ist.astimezone(pytz.UTC)
            end_dt_utc = end_dt_ist.astimezone(pytz.UTC)
            filters &= Q(recived_on_db__range=(start_dt_utc, end_dt_utc))
        except ValueError:
            pass


    if radiologist_names:
        filters &= Q(radiologist__user__id__in=radiologist_names)   


    if institutions:
        filters &= Q(institution_name__in=institutions)

    if status:
        filters &= Q(isDone=(status.lower() == 'reported'))

    if selected_modalities:
        mod_q = Q()
        for m in selected_modalities:
            mod_q |= Q(Modality__exact=m)
        filters &= mod_q

    return qs.filter(filters).distinct()



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 500


class PatientListView(APIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = DICOMDataSerializer

    def get_queryset(self, data):
        qs = DICOMData.objects.all().order_by('-id').prefetch_related('history_files', 'radiologist')
        qs = apply_filters_from_body(qs, data)
        return qs

    def get(self, request, *args, **kwargs):
        data = request.query_params
        export = data.get('export', '0')
        qs = self.get_queryset(data)

        if export == '1':
            return export_patient_qs_to_excel_response(qs)

        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(qs, request, view=self)
        serializer = self.serializer_class(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        export = data.get('export', 0)
        qs = self.get_queryset(data)

        if str(export) == '1':
            return export_patient_qs_to_excel_response(qs)

        paginator = self.pagination_class()
        paginated_qs = paginator.paginate_queryset(qs, request, view=self)
        serializer = self.serializer_class(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)


    def list(self, request, *args, **kwargs):
        if request.GET.get('export') == '1':
            qs = self.get_queryset()
            return export_patient_qs_to_excel_response(qs)
        return super().list(request, *args, **kwargs)


def export_patient_qs_to_excel_response(qs):
    rows = []
    for p in qs:
        history_file = p.history_files.first()
        if p.marked_done_at and p.notes_modified_at:
            tat_diff = p.marked_done_at - p.notes_modified_at
            days = tat_diff.days
            hours, remainder = divmod(tat_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            if days > 0:
                tat_str = f"{days}d {hours}h {minutes}m"
            else:
                tat_str = f"{hours}h {minutes}m"
        else:
            tat_str = "N/A"

        rows.append({
            "Patient Name": p.patient_name,
            "Patient ID": p.patient_id,
            "Age": p.age,
            "Gender": p.gender,
            "Study Date": p.study_date,
            "Study Time": p.study_time.strftime('%H:%M:%S') if p.study_time else None,
            "Received on DB": timezone.localtime(p.recived_on_db, IST).strftime('%Y-%m-%d %H:%M:%S') if p.recived_on_db else None,
            "Modality": p.Modality,
            "Urgent": "Yes" if p.urgent else "No",
            "Status": "Reported" if p.isDone else "Unreported",
            "Location": p.location,
            "Institution Name": p.institution_name,
            "Radiologists": ", ".join([str(r) for r in p.radiologist.all()]),
            "Study Description": p.study_description,
            "Notes": p.notes,
            "Notes modified at": timezone.localtime(p.notes_modified_at, IST).strftime('%Y-%m-%d %H:%M:%S') if p.notes_modified_at else None,
            "History Upload Time": timezone.localtime(history_file.uploaded_at, IST).strftime('%Y-%m-%d %H:%M:%S') if history_file and history_file.uploaded_at else None,
            "Radiologist assigned at": timezone.localtime(p.radiologist_assigned_at, IST).strftime('%Y-%m-%d %H:%M:%S') if p.radiologist_assigned_at else None,
            "Report created at": timezone.localtime(p.marked_done_at, IST).strftime('%Y-%m-%d %H:%M:%S') if p.marked_done_at else None,
            "TAT Counter": tat_str
        })

    df = pd.DataFrame(rows)
    buff = BytesIO()
    with pd.ExcelWriter(buff, engine='xlsxwriter', datetime_format='yyyy-mm-dd hh:mm:ss') as writer:
        df.to_excel(writer, index=False, sheet_name='Patients')
        worksheet = writer.sheets['Patients']
        for i, col in enumerate(df.columns):
            col_width = max(df[col].astype(str).map(len).max(), len(col)) + 2
            worksheet.set_column(i, i, col_width)
    buff.seek(0)
    response = HttpResponse(buff.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=patients.xlsx'
    return response


class RadiologistListView(generics.ListAPIView):
    serializer_class = DICOMDataSerializer  

    def get_queryset(self):
        radiologist_group = Group.objects.filter(name='radiologist').first()
        if not radiologist_group:
            return User.objects.none()  
        return User.objects.filter(groups=radiologist_group).distinct()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email
            }
            for user in queryset
        ]
        return Response(data)


class InstitutionListView(generics.ListAPIView):

    def list(self, request, *args, **kwargs):
        names = Client.objects.exclude(institutions__isnull=True)\
                              .values_list('institutions__name', flat=True)\
                              .distinct()
        data = [{'name': n} for n in names]
        return Response(data)


class ClientListView(generics.ListCreateAPIView):
    def get(self, request):
        names = Client.objects.order_by('-id').values_list('name', flat=True)
        return Response(list(names))
    

class ClientListCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all().select_related('user').prefetch_related('institutions')
    serializer_class = ClientSerializer

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        password = self.request.data.get('password') or "U4rad@2025"
        name = self.request.data.get('name') or ''
        first_name = name.split()[0] if name else ''
        last_name = name.split()[1] if len(name.split()) > 1 else ''

        user, created = User.objects.get_or_create(
            username=email,
            defaults={'email': email, 'first_name': first_name, 'last_name': last_name}
        )
        if created:
            user.set_password(password)
            user.save()
            client_group, _ = Group.objects.get_or_create(name='client')
            user.groups.add(client_group)

        client_instance = serializer.save(user=user, password=password)


    
class ClientRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
   
    queryset = Client.objects.all().select_related('user')
    serializer_class = ClientSerializer


@api_view(['GET'])
def modality_list(request):
    modalities = DICOMData.objects.exclude(Modality__isnull=True).values_list('Modality', flat=True).distinct()
    return Response(list(modalities))

class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceTATSettingListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceTATSettingSerializer

    def get_queryset(self):
        qs = ServiceTATSetting.objects.all()
        institution_name = self.request.query_params.get('institution_name')
        if institution_name:
            qs = qs.filter(institution__name=institution_name)
        return qs

class ServiceTATSettingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceTATSetting.objects.all()
    serializer_class = ServiceTATSettingSerializer
