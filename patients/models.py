from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class PatientUserManager(BaseUserManager):
    def create_user(self, dni, password=None, **extra_fields):
        if not dni:
            raise ValueError("El DNI es obligatorio")
        user = self.model(dni=dni, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, dni, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser debe tener is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser debe tener is_superuser=True.')
        return self.create_user(dni, password, **extra_fields)

class PatientUser(AbstractBaseUser, PermissionsMixin):
    dni         = models.CharField(max_length=8, unique=True)
    first_name  = models.CharField(max_length=150, blank=True)
    last_name   = models.CharField(max_length=150, blank=True)
    email       = models.EmailField(blank=True)
    is_active   = models.BooleanField('Activo', default=True)
    is_staff    = models.BooleanField('Staff',  default=False)
    # … otros campos que necesites (e.g. fecha nacimiento, especialidad…)

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = []

    objects = PatientUserManager()

    def __str__(self):
        return self.dni

class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    male = models.BooleanField()
    age = models.PositiveIntegerField()
    education = models.PositiveSmallIntegerField()
    currentSmoker = models.BooleanField()
    cigsPerDay = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    BPMeds = models.BooleanField()
    prevalentStroke = models.BooleanField()
    prevalentHyp = models.BooleanField()
    diabetes = models.BooleanField()
    totChol = models.FloatField()
    sysBP = models.FloatField()
    diaBP = models.FloatField()
    BMI = models.FloatField()
    heartRate = models.PositiveSmallIntegerField()
    glucose = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({'M' if self.male else 'F'}) | {self.age} años "
