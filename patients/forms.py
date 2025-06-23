# patients/forms.py

from django import forms
from django.conf import settings
from .models import PatientUser
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
import re

ALLOWED_DNI = '72965812'

class LoginDNIForm(AuthenticationForm):
    username = forms.CharField(label="DNI", max_length=8,
            error_messages={
            'required': _('Por favor ingresa tu DNI.'),
            'max_length': _('El DNI debe tener como máximo 8 dígitos.'),
            'min_length': _('El DNI debe tener al menos 8 dígitos.'),
        })
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput,         
            error_messages={
            'required': _('Por favor ingresa tu contraseña.')
        })
    
    def clean_username(self):
        dni = self.cleaned_data.get('username')
        if not dni.isdigit():
            raise forms.ValidationError(_("El DNI sólo puede contener números."))
        if len(dni) != 8:
            # Aunque maxlength/min_length ya lo controlan, por si acaso
            raise forms.ValidationError(_("El DNI debe tener 8 dígitos."))
        return dni

DOMINIOS_VALIDOS = ("hotmail.com", "gmail.com")

class RegistroForm(forms.ModelForm):
    first_name = forms.CharField(
        label=_("Nombre"),
        max_length=40,
        error_messages={
            "required": _("El nombre es obligatorio."),
            "max_length": _("El nombre no puede exceder 40 caracteres."),
        },
    )
    last_name = forms.CharField(
        label=_("Apellidos"),
        max_length=40,
        error_messages={
            "required": _("Los apellidos son obligatorios."),
            "max_length": _("Los apellidos no pueden exceder 40 caracteres."),
        },
    )
    email = forms.EmailField(
        label=_("Correo"),
        max_length=30,
        error_messages={
            "required": _("El correo es obligatorio."),
            "invalid": _("Introduce una dirección de correo válida."),
            "max_length": _("El correo no puede exceder 30 caracteres."),
        },
    )
    dni = forms.CharField(
        label=_("DNI"),
        max_length=8,
        min_length=8,
        error_messages={
            "required": _("El DNI es obligatorio."),
            "max_length": _("El DNI debe tener 8 dígitos."),
            "min_length": _("El DNI debe tener 8 dígitos."),
        },
    )
    password = forms.CharField(
        label=_("Contraseña"),
        widget=forms.PasswordInput,
        min_length=6,
        max_length=10,
        error_messages={
            "required": _("La contraseña es obligatoria."),
            "min_length": _("La contraseña debe tener al menos 6 caracteres."),
            "max_length": _("La contraseña no puede exceder 10 caracteres."),
        },
    )
    password2 = forms.CharField(
        label=_("Repetir Contraseña"),
        widget=forms.PasswordInput,
        min_length=6,
        max_length=10,
        error_messages={
            "required": _("Debes repetir la contraseña."),
            "min_length": _("La contraseña debe tener al menos 6 caracteres."),
            "max_length": _("La contraseña no puede exceder 10 caracteres."),
        },
    )

    class Meta:
        model = PatientUser
        fields = ['first_name', 'last_name', 'email', 'dni']

    def clean_first_name(self):
        nombre = self.cleaned_data['first_name'].strip()
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', nombre):
            raise forms.ValidationError(_("El nombre sólo puede contener letras y espacios."))
        return nombre

    def clean_last_name(self):
        apellidos = self.cleaned_data['last_name'].strip()
        if not re.match(r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$', apellidos):
            raise forms.ValidationError(_("Los apellidos sólo pueden contener letras y espacios."))
        return apellidos

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        dominio = email.split('@')[-1]
        if dominio not in DOMINIOS_VALIDOS:
            raise forms.ValidationError(
                _("El dominio debe ser hotmail.com o gmail.com.")
            )
        return email

    def clean_dni(self):
        dni = self.cleaned_data['dni']
        if not dni.isdigit():
            raise forms.ValidationError(_("El DNI sólo puede contener dígitos."))
        return dni

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 != p2:
            raise forms.ValidationError(_("Las contraseñas no coinciden."))
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

