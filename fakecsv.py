import csv
import random
from faker import Faker

fake = Faker('en_US')  # Puedes cambiar a 'es_ES' o 'en_US' si prefieres

def generate_patient():
    male = random.choice([True, False])
    first_name = fake.first_name_male() if male else fake.first_name_female()
    last_name = fake.last_name()

    age = random.randint(40, 60)
    education = random.randint(1, 4)
    currentSmoker = random.choice([True, False])
    cigsPerDay = random.randint(0, 40) if currentSmoker else 0
    BPMeds = random.choice([True, False])
    prevalentStroke = random.choice([True, False])
    prevalentHyp = random.choice([True, False])
    diabetes = random.choice([True, False])
    totChol = round(random.uniform(150, 300), 1)
    sysBP = round(random.uniform(90, 200), 1)
    diaBP = round(random.uniform(60, 120), 1)
    BMI = round(random.uniform(18.5, 40.0), 1)
    heartRate = random.randint(50, 110)
    glucose = round(random.uniform(70, 250), 1)

    return [
        first_name,
        last_name,
        int(male),
        age,
        education,
        int(currentSmoker),
        cigsPerDay,
        int(BPMeds),
        int(prevalentStroke),
        int(prevalentHyp),
        int(diabetes),
        totChol,
        sysBP,
        diaBP,
        BMI,
        heartRate,
        glucose,
    ]

# Encabezados
headers = [
    "first_name",
    "last_name",
    "male",
    "age",
    "education",
    "currentSmoker",
    "cigsPerDay",
    "BPMeds",
    "prevalentStroke",
    "prevalentHyp",
    "diabetes",
    "totChol",
    "sysBP",
    "diaBP",
    "BMI",
    "heartRate",
    "glucose",
]

# Generar archivo CSV
with open("fake_patients.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    for _ in range(50):
        writer.writerow(generate_patient())

print("✅ CSV generado como 'fake_patients1.csv'")
