
from django.contrib import admin
from .models.personalinfo import PersonalInfo
from .models.qualificationdetails import QualificationDetails
from .models.bankinginfo import BankingInfo
from .models.reportingarea import ReportingArea
from .models.timeavailability import TimeAvailability
from .models.instpersonalinfo import InstPersonalInfo
from .models.institutionmodalities import InstitutionModalities
from .models.patientdata import PatientInfo
from .models.corporatecoordinator import CorporateCoordinator
from .models.corporatedoctor import CorporateDoctor
from .models.dentalpatientdetails import DentalPatientInfo
from .models.doctorpatientdetails import DoctorPatientInfo
from .models.patientdetails import PatientDetails
from .models.City import City
from .models.Client import Client, Institution,ServiceTATSetting, Service
from .models.Date import Date
from .models.Location import Location
from .models.workexp import WorkExp
from .models.serviceslist import ServicesList
from .models.audiopatientdata import audioPatientDetails
from .models.optometrydata import optopatientDetails
from .models.vitalpatientdata import vitalPatientDetails
from .models.DICOMData import DICOMData, DICOMFile, JPEGFile, PatientHistoryFile,PatientReport
from .models.Coordinator import Coordinator
from .models.EcgPdfReport import EcgReport
from .models.XrayPdfReport import XrayReport
from .models.Xray_Client import XClient
from .models.Xray_City import XCity
from .models.Xray_Location import XLocation
from .models.exportlist import ExportList
from .models.Total_cases import Total_Cases
from .models.VitalsPdfReport import VitalsReport
from .models.AudiometryPdfReport import AudiometryReport
from .models.DailyCount import SetCount
from .models.DailyCountECG import ECGSetCount

from .models .StudyReport import StudyReport
from .models .CKEditorTemplate import CKEditorTemplate



admin.site.register(PersonalInfo)
admin.site.register(CorporateCoordinator)
admin.site.register(CorporateDoctor)
admin.site.register(WorkExp)
admin.site.register(QualificationDetails)
admin.site.register(BankingInfo)
admin.site.register(ReportingArea)
admin.site.register(TimeAvailability)
admin.site.register(InstPersonalInfo)
admin.site.register(InstitutionModalities)
admin.site.register(PatientInfo)
admin.site.register(PatientDetails)
admin.site.register(audioPatientDetails)
admin.site.register(optopatientDetails)
admin.site.register(vitalPatientDetails)
admin.site.register(City)
admin.site.register(Client)
admin.site.register(Institution)
admin.site.register(Service)
admin.site.register( ServiceTATSetting)
admin.site.register(Date)
admin.site.register(Location)
admin.site.register(ServicesList)
admin.site.register(Coordinator)
admin.site.register(EcgReport)
admin.site.register(XrayReport)
admin.site.register(XClient)
admin.site.register(XCity)
admin.site.register(XLocation)
admin.site.register(Total_Cases)
admin.site.register(ExportList)
admin.site.register(AudiometryReport)
admin.site.register(VitalsReport)
admin.site.register(SetCount)
admin.site.register(ECGSetCount)
admin.site.register(StudyReport)
admin.site.register(DentalPatientInfo)
admin.site.register(DoctorPatientInfo)
admin.site.register(CKEditorTemplate)

# Register your models here.
class DICOMFileInline(admin.TabularInline):
    model = DICOMFile

class JPEGFileInline(admin.TabularInline):
    model = JPEGFile


class PatientHistoryFileInline(admin.TabularInline):
    model = PatientHistoryFile

class PatientReportInline(admin.TabularInline):
    model = PatientReport

@admin.register(DICOMData)
class DICOMDataAdmin(admin.ModelAdmin):
    inlines = [DICOMFileInline, JPEGFileInline, PatientHistoryFileInline, PatientReportInline]


# Register your models here.
