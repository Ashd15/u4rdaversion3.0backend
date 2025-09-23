from django.http import JsonResponse
from api.models import BodyPart

def fetch_body_parts(request):
    if request.method == "GET":
        body_parts = BodyPart.objects.all().values("id", "name")
        return JsonResponse(list(body_parts), safe=False)
