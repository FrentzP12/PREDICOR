from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from patients.views import (
    PatientDetailView,
    page_landing,         # nueva vista para landing
    login_view,           # vista para login
    registro,             # vista para registro
    IndexView                  # vista protegida
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # API REST
    path('api/patients/', include('patients.urls')),

    # Vista de detalle de paciente
    path('patients/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),

    # Página de inicio (landing pública)
    path('', page_landing, name='page-landing'),

    # Login y Registro
    path('login/', login_view, name='login'),
    path('register/', registro, name='register'),

    # Página principal protegida (solo usuarios logueados)
    path('home/', IndexView.as_view(), name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

