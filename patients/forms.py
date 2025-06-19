# patients/forms.py

from django import forms
from django.conf import settings
from .models import PatientUser
from django.contrib.auth.forms import AuthenticationForm

ALLOWED_DNI = '72965812'

class LoginDNIForm(AuthenticationForm):
    username = forms.CharField(label="DNI", max_length=8)
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class RegistroForm(forms.ModelForm):
    password  = forms.CharField(label="Contraseña", widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label="Repetir Contraseña", widget=forms.PasswordInput, min_length=6)

    class Meta:
        model  = PatientUser
        fields = ['first_name','last_name','email','dni']

    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni != ALLOWED_DNI:
            raise forms.ValidationError("No estás autorizado para registrarte.")
        return dni

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
