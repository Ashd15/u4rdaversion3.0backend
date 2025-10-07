import base64
import io
import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from api.models.patientdetails import PatientDetails
from api.models.personalinfo import PersonalInfo

from reportlab.lib import colors
from reportlab.lib.units import mm

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from django.core.files.base import ContentFile
from api.models.EcgPdfReport import EcgReport
import datetime


ECG_REPLACEMENTS = {
    "Normal ECG": "Normal Sinus Rhythm.",
    "Sinus rhythm with incomplete RBBB": "Sinus rhythm with incomplete RBBB.",
    "Sinus Tachycardia with incomplete RBBB": "Sinus Tachycardia with incomplete RBBB.",
    "Sinus Bradycardia with incomplete RBBB": "Sinus Bradycardia with incomplete RBBB.",
    "Sinus Bradycardia": "Sinus Bradycardia.",
    "Sinus Tachycardia": "Sinus Tachycardia.",
    "Normal sinus rhythm with t inversion in lead III": "Normal sinus rhythm with t inversion in lead III"
}


def generate_report_text(patient, ecg_finding, additional):

    heart_rate = getattr(patient, 'HeartRate', None)

    lines = [
        f"Heart rate is {heart_rate} BPM.",
        "Normal Sinus Rhythm.",
        "No significant ST-T changes seen."
    ]

    if ecg_finding in ECG_REPLACEMENTS:
        if ecg_finding == "Normal sinus rhythm with t inversion in lead III":
            lines[1] = ECG_REPLACEMENTS[ecg_finding]
            lines[2] = ""
        else:
            lines[1] = ECG_REPLACEMENTS[ecg_finding]

    report_text = "\n".join([l for l in lines if l])
    if additional:
        report_text += f"\n\nAdditional Findings: {additional}"
    return report_text


def generate_pdf_base64(patient, doctor, report_text):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=15*mm, leftMargin=15*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    elements = []
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    table_style_font = ParagraphStyle('TableFont', parent=normal_style, fontName='Helvetica-Bold', fontSize=12)
    title_style = ParagraphStyle('Title', parent=normal_style, fontName='Helvetica-Bold', fontSize=16, spaceAfter=10)
    subtitle_style = ParagraphStyle('Subtitle', parent=normal_style, fontName='Helvetica-Bold', fontSize=14, spaceAfter=8)
    content_style = ParagraphStyle('Content', parent=normal_style, fontName='Helvetica-Bold', fontSize=12, spaceAfter=5)

    patient_data = [
        ["Name:", patient.PatientName, "Patient ID:", str(patient.id), "Age:", str(patient.age)],
        ["Gender:", patient.gender, "Test Date:", str(patient.TestDate), "Report Date:", str(patient.ReportDate)]
    ]
    table = Table(patient_data, colWidths=[60, 100, 70, 80, 90, 90], rowHeights=30, hAlign='CENTER')
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('FONTSIZE', (0,0), (-1,-1), 13),
    ]))
    elements.append(Spacer(1, 20))
    elements.append(table)
    elements.append(Spacer(1, 25))

    elements.append(Paragraph("<b><u>ECG</u></b>", subtitle_style))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("<b><u>Observation</u></b>", subtitle_style))
    elements.append(Spacer(1, 12))

    for line in report_text.split("\n"):
        elements.append(Paragraph(f"<b>{line}</b>", subtitle_style))
        elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 220))  

   
    if doctor.signature and doctor.signature.path and os.path.exists(doctor.signature.path):
     try: 
        sig_img = Image(doctor.signature.path, width=120, height=50)

        sig_table = Table([[sig_img]], colWidths=[120])
        sig_table.setStyle(TableStyle([
            ('LEFTPADDING', (0,0), (-1,-1), -200),  
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(sig_table)
     except:
        pass

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(f"<b>Dr. {doctor.user.first_name} {doctor.user.last_name}</b>", subtitle_style))
    elements.append(Paragraph("Consultant", subtitle_style))
    elements.append(Paragraph("Non Invasive Cardiology", subtitle_style))

    elements.append(PageBreak())
    if patient.image and patient.image.path and os.path.exists(patient.image.path):
        try:
            img = Image(patient.image.path, width=450, height=270)  # adjust width/height as needed
            elements.append(img)
        except:
            pass

    doc.build(elements)

    pdf_data = buffer.getvalue()
    buffer.close()
    return base64.b64encode(pdf_data).decode("utf-8")


@api_view(['POST'])
@permission_classes([AllowAny])
def report_preview(request):
    """
    Preview report for a doctor before confirming
    """
    try:
        patient_id = request.data.get("patient_id")
        username = request.data.get("doctor_username")
        ecg_finding = request.data.get("ecg_findings")
        additional = request.data.get("additional_findings", "")

        doctor = PersonalInfo.objects.filter(user__username=username).first()
        if not doctor:
            return Response({"error": "Doctor not found"}, status=404)

        patient = PatientDetails.objects.get(id=patient_id)

        report_text = generate_report_text(patient, ecg_finding, additional)

        ecg_image_base64 = None
        if patient.image and patient.image.path and os.path.exists(patient.image.path):
            with open(patient.image.path, "rb") as img:
                ecg_image_base64 = "data:image/jpeg;base64," + base64.b64encode(img.read()).decode("utf-8")

        return Response({
            "patient": {
                "name": patient.PatientName,
                "age": patient.age,
                "gender": patient.gender,
                "test_date": patient.TestDate,
                "report_date": patient.ReportDate
            },
            "report_text": report_text,
            "doctor": {
                "name": f"Dr. {doctor.user.first_name} {doctor.user.last_name}",
                "signature": doctor.signature.url if doctor.signature else None
            },
            "ecg_image_base64": ecg_image_base64
        })

    except PatientDetails.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def report_finalize(request):
    """
    Finalize report — mark done, generate and save PDF in EcgReport model.
    """
    try:
        patient_id = request.data.get("patient_id")
        username = request.data.get("doctor_username")
        ecg_finding = request.data.get("ecg_findings")
        additional = request.data.get("additional_findings", "")

        doctor = PersonalInfo.objects.filter(user__username=username).first()
        if not doctor:
            return Response({"error": "Doctor not found"}, status=404)

        patient = PatientDetails.objects.get(id=patient_id)

        report_text = generate_report_text(patient, ecg_finding, additional)

        pdf_base64 = generate_pdf_base64(patient, doctor, report_text)
        pdf_bytes = base64.b64decode(pdf_base64)

        report_instance = EcgReport(
            name=patient.PatientName,
            patient_id=str(patient.id),
            test_date=patient.TestDate,
            report_date=datetime.date.today(),
            location=patient.Location if hasattr(patient, "Location") else None
        )

        filename = f"ECG_Report_{patient.PatientName}_{datetime.date.today()}.pdf"
        report_instance.pdf_file.save(filename, ContentFile(pdf_bytes))
        report_instance.save()

        patient.isDone = True
        patient.status = True
        patient.save()

        return Response({
            "message": "Report finalized and saved successfully.",
            "pdf_url": report_instance.get_pdf_url(),  
            "pdf_base64": pdf_base64  
        })

    except PatientDetails.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['POST'])
@permission_classes([AllowAny])
def report_reject(request):
    """
    Doctor rejects ECG report with reason.
    """
    try:
        patient_id = request.data.get("patient_id")
        username = request.data.get("doctor_username")
        reason = request.data.get("reason", "No reason provided")

        doctor = PersonalInfo.objects.filter(user__username=username).first()
        if not doctor:
            return Response({"error": "Doctor not found"}, status=404)

        patient = PatientDetails.objects.get(id=patient_id)

        patient.NonReportable = True
        patient.status = False
        patient.save()

        return Response({
            "message": f"ECG for patient {patient.PatientName} rejected.",
            "reason": reason
        })

    except PatientDetails.DoesNotExist:
        return Response({"error": "Patient not found"}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([AllowAny])
def ecg_stat(request):
    """
    Returns ECG statistics for a doctor.
    """
    try:
        username = request.GET.get("doctor_username")
        doctor = PersonalInfo.objects.filter(user__username=username).first()
        if not doctor:
            return Response({"error": "Doctor not found"}, status=404)

        total_reported = PatientDetails.objects.filter(isDone=True, status=True).count()
        current_allocated = PatientDetails.objects.filter(isDone=False, status=False).count()
        current_reported = PatientDetails.objects.filter(isDone=True).count()

        return Response({
            "total_reported": total_reported,
            "current_allocated": current_allocated,
            "current_reported": current_reported
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)