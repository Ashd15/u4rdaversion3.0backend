# api/views/user_views.py

from django.contrib.auth.models import User
from django.http import JsonResponse

def fetch_radiologists(request):
    # Filter users who belong to the "radiologist" group
    users = User.objects.filter(groups__name="radiologist").values(
        "id", "username", "first_name", "last_name", "email", "is_active"
    )

    return JsonResponse(list(users), safe=False)
