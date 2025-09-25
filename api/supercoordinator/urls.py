from django.urls import path
from .views_api import PatientListView, RadiologistListView, InstitutionListView, ClientListView, ClientListCreateView, ClientRetrieveUpdateDestroyView, ServiceListView, modality_list, ServiceTATSettingListCreateView, ServiceTATSettingRetrieveUpdateDestroyView

urlpatterns = [
    
    path('clients/', ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroyView.as_view(), name='client-detail'),

    path('patients/', PatientListView.as_view(), name='api-patients'),
    path('radiologists/', RadiologistListView.as_view(), name='api-radiologists'),
    path('institutions/', InstitutionListView.as_view(), name='api-institutions'),
    path('clientss/', ClientListView.as_view(), name='api-clients'),
    path('modalities/', modality_list, name='api-modalities'),

    path('services/', ServiceListView.as_view(), name='service-list'),
    path('service-tat-settings/', ServiceTATSettingListCreateView.as_view(), name='service-tat-list-create'),
    path('service-tat-settings/<int:pk>/', ServiceTATSettingRetrieveUpdateDestroyView.as_view(), name='service-tat-rud'),
    
]
