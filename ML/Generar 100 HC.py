import pandas as pd
import numpy as np

# Fijar semilla para reproducibilidad
np.random.seed(42)

n = 100  # número de filas

# Generar variables
male = np.random.binomial(1, 0.5, n)
age = np.random.randint(40, 60, n)  # edades entre 30 y 80 años
education = np.random.choice([1, 2, 3, 4], size=n, p=[0.2, 0.3, 0.3, 0.2])
currentSmoker = np.random.binomial(1, 0.2, n)
cigsPerDay = np.where(currentSmoker == 1, np.random.poisson(10, n), 0)
BPMeds = np.random.binomial(1, 0.1, n)
prevalentStroke = np.random.binomial(1, 0.05, n)
prevalentHyp = np.random.binomial(1, 0.3, n)
diabetes = np.random.binomial(1, 0.1, n)
totChol = np.random.normal(200, 30, n).round(1)  # mg/dL, media ≈200 citeturn0search0
sysBP = np.random.normal(130, 15, n).round(1)    # mm Hg, media ≈130 citeturn0search1
diaBP = np.random.normal(80, 10, n).round(1)     # mm Hg, media ≈80 citeturn0search1
BMI = np.random.normal(27, 4, n).round(1)        # IMC, media ≈27
heartRate = np.random.normal(75, 10, n).round(1) # pulsaciones por minuto
glucose = np.random.normal(100, 15, n).round(1)  # mg/dL, media ≈100

# Ensayar rangos válidos
totChol = np.clip(totChol, 100, 350)
sysBP = np.clip(sysBP, 90, 200)
diaBP = np.clip(diaBP, 60, 120)
BMI = np.clip(BMI, 15, 45)
heartRate = np.clip(heartRate, 40, 120)
glucose = np.clip(glucose, 50, 250)

# Crear DataFrame
df_synthetic = pd.DataFrame({
    'male': male,
    'age': age,
    'education': education,
    'currentSmoker': currentSmoker,
    'cigsPerDay': cigsPerDay,
    'BPMeds': BPMeds,
    'prevalentStroke': prevalentStroke,
    'prevalentHyp': prevalentHyp,
    'diabetes': diabetes,
    'totChol': totChol,
    'sysBP': sysBP,
    'diaBP': diaBP,
    'BMI': BMI,
    'heartRate': heartRate,
    'glucose': glucose
})

# Mostrar primeras filas
df_synthetic.head()
# Para guardar como CSV:
df_synthetic.to_csv("synthetic_heart_data1.csv", index=False)
