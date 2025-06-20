from rest_framework import generics, viewsets, filters
from django.utils import timezone
from .models import Patient
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import PatientSerializer
from rest_framework.pagination import PageNumberPagination
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.core.paginator import Paginator
import pandas as pd
import joblib, xgboost as xgb
from pathlib import Path
from django.views.generic import DetailView
from django.shortcuts      import render, redirect
from django.contrib.auth   import login as auth_login, logout as auth_logout
from django.contrib        import messages
from .forms                import RegistroForm, LoginDNIForm


BASE_DIR = Path(__file__).resolve().parent.parent


# Modelo CHD
MODEL_CHD    = xgb.Booster(); MODEL_CHD.load_model(str(BASE_DIR / "ML/modelo_xgb.json"))
PREPROC_CHD  = joblib.load(str(BASE_DIR / "ML/preprocessor.joblib"))

# Modelo Heart‐Stroke
MODEL_STROKE   = xgb.Booster(); MODEL_STROKE.load_model(str(BASE_DIR / "ML/heart-stroke/xgb_heart_stroke.json"))
PREPROC_STROKE = joblib.load(str(BASE_DIR / "ML/heart-stroke/preprocessor_heart_stroke.joblib"))



class IndexView(ListView):
    model = Patient
    template_name = 'home.html'
    context_object_name = 'pacientes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Patient.objects.all().order_by('-id')  # Orden descendente
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(first_name__icontains=q)  # Buscar por nombre
        return queryset

class PatientsTodayAPI(generics.ListCreateAPIView):
    """
    Permite listar pacientes (GET) y crear nuevos pacientes (POST).
    """
    serializer_class = PatientSerializer
    queryset = Patient.objects.all().order_by('id')
class TenPerPagePagination(PageNumberPagination):
    page_size = 10

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('-id')
    serializer_class = PatientSerializer
    pagination_class = TenPerPagePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

class PatientDetailAPI(generics.RetrieveAPIView):
    """
    Detalle de un paciente por su ID.
    """
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()

class PatientDetailView(DetailView):
    model = Patient
    template_name = "patient_detail.html"
    context_object_name = "paciente"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        p = ctx["paciente"]

        # Si viene ?predict=1, generamos ambas predicciones
        if self.request.GET.get("predict") == "1":
            # 1) Armamos el DataFrame base
            base = [{
                "male": int(p.male),
                "age": p.age,
                "education": p.education,
                "currentSmoker": int(p.currentSmoker),
                "cigsPerDay": p.cigsPerDay,
                "BPMeds": int(p.BPMeds),
                "prevalentStroke": int(p.prevalentStroke),
                "prevalentHyp": int(p.prevalentHyp),
                "diabetes": int(p.diabetes),
                "totChol": p.totChol,
                "sysBP": p.sysBP,
                "diaBP": p.diaBP,
                "BMI": p.BMI,
                "heartRate": p.heartRate,
                "glucose": p.glucose,
            }]
            df = pd.DataFrame(base)

            # 2) Predicción CHD
            X_chd = PREPROC_CHD.transform(df)
            prob_chd = float(MODEL_CHD.predict(xgb.DMatrix(X_chd))[0])
            ctx["risk_chd"]     = round(prob_chd * 100, 1)
            ctx["risk_no_chd"]  = round(100 - ctx["risk_chd"], 1)

            # 3) Predicción Stroke
            X_st = PREPROC_STROKE.transform(df)
            prob_stroke = float(MODEL_STROKE.predict(xgb.DMatrix(X_st))[0])
            ctx["risk_stroke"]      = round(prob_stroke * 100, 1)
            ctx["risk_no_stroke"]   = round(100 - ctx["risk_stroke"], 1)

            # 1️⃣ RANGOS IDEALES
            ctx["ideal_ranges"] = {
            "totChol": 200,         # mg/dL
            "triglycerides": 150,   # mg/dL
            "glucose": 100,         # mg/dL
            "sysBP": 120,           # mmHg
            "heartRate": 70,        # bpm
            }

        return ctx

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro exitoso. Ya puedes iniciar sesión.")
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginDNIForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = LoginDNIForm()
    return render(request, 'login.html', {'form': form})

# Home protegida
class IndexView(TemplateView):
    template_name = 'home.html'
# Landing pública
def page_landing(request):
    return render(request, 'page-landing.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')