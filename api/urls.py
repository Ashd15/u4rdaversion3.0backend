from django.urls import path
from .views import fetch_tat_counters,server_data


urlpatterns = [
    path('fetch-tat-counters/', fetch_tat_counters),
    path('serverdata/', server_data),
    

]
