
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from api.models.Coordinator import Coordinator


def get_all_coordinators(request):
    coordinators = Coordinator.objects.all().values(
        'id', 'first_name', 'last_name', 'email', 'about', 'profile_pic',
        'tat_completed', 'tat_breached'
    )
    # Convert QuerySet to list
    data = list(coordinators)
    # For profile_pic, make sure to return full URL
    for item in data:
        if item['profile_pic']:
            item['profile_pic'] = request.build_absolute_uri(item['profile_pic'])
    return JsonResponse(data, safe=False)

