from pyorthanc import Orthanc
import json
from django.http import JsonResponse   
from django.views.decorators.csrf import csrf_exempt
import sys

@csrf_exempt  # temporary for testing, can remove later with proper CSRF
def server_data(request):
    # Always log method
    print(f"📡 server_data called with method: {request.method}", file=sys.stderr)

    if request.method != 'POST':
        print("⚠️ GET method not allowed", file=sys.stderr)
        return JsonResponse({'error': 'GET method not allowed'}, status=405)

    print("✅ POST request received", file=sys.stderr)

    # Get studyid from POST body
    study_id = request.POST.get("studyid")
    if not study_id:
        print("❌ No studyid received in POST request", file=sys.stderr)
        return JsonResponse({'error': 'No studyid received'}, status=400)

    print(f"📥 Received study_id: {study_id}", file=sys.stderr)

    # Connect to Orthanc
    try:
        server = Orthanc('https://pacs.reportingbot.in/', username='admin', password='u4rad')
        study = server.get_studies_id(study_id)
        print(f"📑 Study Info: {study}", file=sys.stderr)
    except Exception as e:
        print(f"❌ Error fetching study: {e}", file=sys.stderr)
        return JsonResponse({'error': 'Invalid studyid or PACS issue'}, status=500)

    series_ids = study.get('Series', [])
    print(f"🔗 Series IDs: {series_ids}", file=sys.stderr)

    series = []
    studyUID = ''
    name = ''
    patient_id = ''
    studyDate = ''
    studyTime = ''

    for i in series_ids:
        try:
            instances = server.get_series_id(i).get('Instances', [])
            if not instances:
                continue
            sampleInstance = instances[0]
            tags = server.get_instances_id_tags(sampleInstance)

            name = tags.get('0010,0010', {}).get('Value', '')
            studyUID = tags.get('0020,000d', {}).get('Value', '')
            studyDate = tags.get('0008,0020', {}).get('Value', '')
            studyTime = tags.get('0008,0030', {}).get('Value', '')
            seriesUID = tags.get('0020,000e', {}).get('Value', '')
            seriesModality = tags.get('0008,0060', {}).get('Value', '')
            patient_id = tags.get('0010,0020', {}).get('Value', '')
            seriesDescription = tags.get('0008,103e', {}).get('Value', '')
            seriesPreview = f'https://pacs.reportingbot.in/instances/{sampleInstance}/preview'

            print(f"📂 Series UID: {seriesUID}, Modality: {seriesModality}, Desc: {seriesDescription}", file=sys.stderr)

            series.append([seriesUID, seriesModality, seriesDescription, seriesPreview])
        except Exception as e:
            print(f"⚠️ Error processing series {i}: {e}", file=sys.stderr)

    response_data = {
        'study_uid': studyUID,
        'series': series,
        'name': name,
        'id': patient_id,
        'date': studyDate,
        'time': studyTime
    }

    print("✅ Returning response:", response_data, file=sys.stderr)
    return JsonResponse(response_data)
