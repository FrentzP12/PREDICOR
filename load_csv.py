#!/usr/bin/env python
import os
import django
import csv

# 1) Indica dónde está tu settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from patients.models import Patient

def run():
    path = "C:/Users/frent/OneDrive/Desktop/Project_HC/fake_patients1.csv"
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            Patient.objects.create(
                first_name     = row['first_name'],
                last_name      = row['last_name'],
                male           = bool(int(row['male'])),
                age            = int(row['age']),
                education      = int(row['education']),
                currentSmoker  = bool(int(row['currentSmoker'])),
                cigsPerDay     = int(row['cigsPerDay']),
                BPMeds         = bool(int(row['BPMeds'])),
                prevalentStroke= bool(int(row['prevalentStroke'])),
                prevalentHyp   = bool(int(row['prevalentHyp'])),
                diabetes       = bool(int(row['diabetes'])),
                totChol        = float(row['totChol']),
                sysBP          = float(row['sysBP']),
                diaBP          = float(row['diaBP']),
                BMI            = float(row['BMI']),
                heartRate      = int(row['heartRate']),
                glucose        = float(row['glucose']),
            )
            count += 1
    print(f"✔ Se han cargado {count} pacientes desde {path}")

if __name__ == "__main__":
    run()
