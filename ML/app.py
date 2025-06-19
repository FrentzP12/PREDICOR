import streamlit as st
import pandas as pd
import xgboost as xgb
import joblib
from pathlib import Path
import random
import matplotlib.pyplot as plt 
import plotly.graph_objects as go


# Cargar modelo y preprocesador
BASE_DIR = Path(__file__).resolve().parent
model = xgb.Booster()
model.load_model(str(BASE_DIR / "modelo_xgb.json"))
preprocessor = joblib.load(str(BASE_DIR / "preprocessor.joblib"))

st.set_page_config(page_title="Detección de Cardiopatía", layout="wide")
st.title("Predicción de Riesgo de Cardiopatía")

# Pestañas para Individual y Batch
tab1, tab2 = st.tabs(["Predicción Individual", "Predicción Batch (CSV)"])

# Función de predicción caché
def predict_df(df: pd.DataFrame) -> pd.DataFrame:
    X = preprocessor.transform(df)
    dmat = xgb.DMatrix(X)
    probs = model.predict(dmat)
    df["risk_prob"] = probs
    df["risk_pred"] = (probs > 0.5).astype(int)
    return df

with tab1:
    st.header("Paciente Individual")
    cols = st.columns(4)

    # Inicializar valores en session_state si no existen
    if "inputs" not in st.session_state:
        st.session_state.inputs = {
            "male": 1,
            "age": 50.0,
            "education": 3,
            "currentSmoker": 0,
            "cigsPerDay": 0.0,
            "BPMeds": 0,
            "prevalentStroke": 0,
            "prevalentHyp": 0,
            "diabetes": 0,
            "totChol": 200.0,
            "sysBP": 120.0,
            "diaBP": 80.0,
            "BMI": 25.0,
            "heartRate": 70.0,
            "glucose": 90.0
        }

    def generar_valores_random():
        return {
            "male": random.randint(0, 1),
            "age": random.uniform(40, 60),
            "education": random.randint(1, 4),
            "currentSmoker": random.randint(0, 1),
            "cigsPerDay": random.uniform(0, 30),
            "BPMeds": random.randint(0, 1),
            "prevalentStroke": random.randint(0, 1),
            "prevalentHyp": random.randint(0, 1),
            "diabetes": random.randint(0, 1),
            "totChol": random.uniform(150, 300),
            "sysBP": random.uniform(100, 180),
            "diaBP": random.uniform(60, 110),
            "BMI": random.uniform(18, 35),
            "heartRate": random.uniform(55, 100),
            "glucose": random.uniform(70, 130)
        }

    if st.button("Valores Aleatorios"):
        st.session_state.inputs = generar_valores_random()

    if st.button("Limpiar"):
        st.session_state.inputs = {
            k: (0 if isinstance(v, int) else 0.0) for k, v in st.session_state.inputs.items()
        }

    # Widgets con valores desde session_state
    male = cols[0].selectbox("Sexo (male)", options=[0, 1], format_func=lambda x: "Mujer" if x == 0 else "Hombre", index=st.session_state.inputs["male"])
    age = cols[0].number_input("Edad (age)", min_value=0.0, max_value=120.0, value=st.session_state.inputs["age"])
    education = cols[0].selectbox("Educación (education)", options=[1, 2, 3, 4, 5], index=st.session_state.inputs["education"] - 1)
    currentSmoker = cols[1].selectbox("Fumador actual (currentSmoker)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí", index=st.session_state.inputs["currentSmoker"])
    cigsPerDay = cols[1].number_input("Cigarros por día (cigsPerDay)", min_value=0.0, value=st.session_state.inputs["cigsPerDay"])
    BPMeds = cols[1].selectbox("Medicamentos para presión (BPMeds)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí", index=st.session_state.inputs["BPMeds"])
    prevalentStroke = cols[2].selectbox("Stroke previo (prevalentStroke)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí", index=st.session_state.inputs["prevalentStroke"])
    prevalentHyp = cols[2].selectbox("Hipertensión previa (prevalentHyp)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí", index=st.session_state.inputs["prevalentHyp"])
    diabetes = cols[2].selectbox("Diabetes (diabetes)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Sí", index=st.session_state.inputs["diabetes"])
    totChol = cols[3].number_input("Colesterol total (totChol)", value=st.session_state.inputs["totChol"])
    sysBP = cols[3].number_input("Presión sistólica (sysBP)", value=st.session_state.inputs["sysBP"])
    diaBP = cols[3].number_input("Presión diastólica (diaBP)", value=st.session_state.inputs["diaBP"])
    BMI = cols[0].number_input("BMI", value=st.session_state.inputs["BMI"])
    heartRate = cols[1].number_input("Frecuencia cardiaca (heartRate)", value=st.session_state.inputs["heartRate"])
    glucose = cols[2].number_input("Glucosa sérica (glucose)", value=st.session_state.inputs["glucose"])

    if st.button("Predecir Individual"):
        df = pd.DataFrame([{
            "male": male,
            "age": age,
            "education": education,
            "currentSmoker": currentSmoker,
            "cigsPerDay": cigsPerDay,
            "BPMeds": BPMeds,
            "prevalentStroke": prevalentStroke,
            "prevalentHyp": prevalentHyp,
            "diabetes": diabetes,
            "totChol": totChol,
            "sysBP": sysBP,
            "diaBP": diaBP,
            "BMI": BMI,
            "heartRate": heartRate,
            "glucose": glucose
        }])
        result = predict_df(df.copy())
        prob = result.at[0, "risk_prob"]
        pred = result.at[0, "risk_pred"]
        st.metric("Probabilidad de enfermedad (%)", f"{prob*100:.1f}%")
        st.write("**Predicción:**", "Enfermedad" if pred == 1 else "Sano")
 # --------------------------------------------------
        # Gráfico de rueda compacto y fondo transparente
        labels = ['Riesgo', 'Sin riesgo']
        values = [prob, 1-prob]

        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='percent',
            marker=dict(line=dict(color='white', width=2))
        )])
        fig.update_layout(
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0),
            width=150,
            height=150,
            paper_bgcolor='rgba(0,0,0,0)',
        )

        st.plotly_chart(fig, use_container_width=False)

with tab2:
    st.header("Batch desde CSV")
    uploaded_file = st.file_uploader(
        "Sube CSV con columnas: male,age,education,currentSmoker,cigsPerDay,BPMeds,prevalentStroke,prevalentHyp,diabetes,totChol,sysBP,diaBP,BMI,heartRate,glucose",
        type=["csv"]
    )
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            result = predict_df(df.copy())
            st.success("Predicciones generadas")
            st.dataframe(result)
            csv = result.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Descargar resultados CSV",
                data=csv,
                file_name="predicciones_riesgo.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error al procesar: {e}")
