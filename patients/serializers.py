from rest_framework import serializers
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            'id',
            'first_name',
            'last_name',
            'male',
            'age',
            'education',
            'currentSmoker',
            'cigsPerDay',
            'BPMeds',
            'prevalentStroke',
            'prevalentHyp',
            'diabetes',
            'totChol',
            'sysBP',
            'diaBP',
            'BMI',
            'heartRate',
            'glucose',
            'weight',
            'height',
            'triglycerides',
        ]
