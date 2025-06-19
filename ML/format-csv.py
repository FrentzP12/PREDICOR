import pandas as pd

# --- Archivos ---
INPUT_CSV  = r'C:/Users/frent/OneDrive/Desktop/Project_HC/ML/heart_disease.csv'  
OUTPUT_CSV = r'C:/Users/frent/OneDrive/Desktop/Project_HC/ML/heart_stroke3.csv'

# --- Diccionarios de mapeo ---
gender_map = {'Male': 1, 'Female': 0}
education_map = {
    'uneducated': 1,
    'primaryschool': 2,
    'graduate': 3,
    'postgraduate': 4
}
yesno_map = {'yes': 1, 'no': 0, 'Yes': 1, 'No': 0}

# --- Leer CSV con separador ';' ---
df = pd.read_csv(INPUT_CSV, sep=';')

# --- Limpiar nombres de columnas ---
df.columns = [col.strip().lower().replace(' ', '').replace('-', '') for col in df.columns]

# --- Transformaciones ---
df['male'] = df['gender'].map(gender_map)
df['education'] = df['education'].str.lower().map(education_map)

# Mapear prevalentStroke solo si es texto
if df['prevalentstroke'].dtype == object:
    df['prevalentstroke'] = df['prevalentstroke'].map(yesno_map)

# Mapear prevalentHyp solo si es texto
if df['prevalenthyp'].dtype == object:
    df['prevalenthyp'] = df['prevalenthyp'].map(yesno_map)

# Mapear heart_stroke
df['heart_stroke'] = df['heart_stroke'].map(yesno_map)

# Eliminar columna original gender
df = df.drop(columns=['gender'])

# Renombrar columnas a formato final
df = df.rename(columns={
    'currentsmoker':   'currentSmoker',
    'cigsperday':      'cigsPerDay',
    'bpmeds':          'BPMeds',
    'prevalentstroke': 'prevalentStroke',
    'prevalenthyp':    'prevalentHyp',
    'totchol':         'totChol',
    'sysbp':           'sysBP',
    'diabp':           'diaBP',
    'bmi':             'BMI',
    'heartrate':       'heartRate',
    'glucose':         'glucose'
})

# Orden de columnas final
column_order = [
    'male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
    'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol',
    'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose', 'heart_stroke'
]
df = df[column_order]

# Guardar CSV reemplazando NaN con "NA"
df.to_csv(OUTPUT_CSV, index=False, na_rep='NA')

print("✅ Transformación completa. Archivo exportado correctamente con valores NA visibles.")
