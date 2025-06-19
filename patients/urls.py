# patients/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientsTodayAPI, PatientDetailAPI, PatientDetailView, PatientViewSet
router = DefaultRouter()
# registra la lista y create en /api/patients/
router.register(r'', PatientViewSet, basename='patient')

urlpatterns = [
    path('', include(router.urls)),
    path('', PatientsTodayAPI.as_view(), name='api-patients-list'),
    path('<int:pk>/', PatientDetailAPI.as_view(), name='api-patient-detail'),
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
]