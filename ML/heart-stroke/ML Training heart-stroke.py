import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import xgboost as xgb
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt
import joblib

# ------------------------------
# 1) Cargar dataset
# ------------------------------
data_path = Path("C:/Users/frent/OneDrive/Desktop/Project_HC/ML/heart-stroke/heart_stroke.csv")
df = pd.read_csv(data_path)

# ------------------------------
# 2) Definir objetivo: 'heart_stroke'
# ------------------------------
target_col = "heart_stroke"
if target_col not in df.columns:
    raise ValueError(f"No encuentro la columna objetivo '{target_col}' en {df.columns.tolist()}")

# Separar X e y
X_df = df.drop(columns=[target_col])
y_raw = df[target_col]

# Asegurar 0/1 en y
y = y_raw.astype(int)

# ------------------------------
# 3) Preprocesamiento mixto
# ------------------------------
# Tus columnas de entrada (todas deberían ser numéricas tras la transformación previa)
feature_cols = [
    'male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
    'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol',
    'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'
]
X_df = X_df[feature_cols]

# Identificar numéricas y categóricas
numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = X_df.select_dtypes(exclude=[np.number]).columns.tolist()

# Pipeline numérico: imputar mediana + escalar
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline categórico: imputar moda + one-hot (si hubiera)
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot',   OneHotEncoder(handle_unknown='ignore', sparse_output=False))
]) if len(cat_cols) > 0 else None

# ColumnTransformer
transformers = [('num', numeric_pipeline, numeric_cols)]
if categorical_pipeline:
    transformers.append(('cat', categorical_pipeline, cat_cols))

preprocessor = ColumnTransformer(transformers)

# Aplicar
X = preprocessor.fit_transform(X_df)

# ------------------------------
# 4) Train/test split
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------
# 5) Entrenar XGBoost
# ------------------------------
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest  = xgb.DMatrix(X_test,  label=y_test)

params = {
    'objective':   'binary:logistic',
    'eval_metric': 'auc'
}

bst = xgb.train(
    params,
    dtrain,
    num_boost_round=100,
    evals=[(dtest, 'test')],
    early_stopping_rounds=10,
    verbose_eval=True
)

# ------------------------------
# 6) Evaluación
# ------------------------------
y_pred_prob = bst.predict(dtest)
auc = roc_auc_score(y_test, y_pred_prob)
print(f"AUC en test: {auc:.3f}")

# ------------------------------
# 7) Importancia de características
# ------------------------------
fig, ax = plt.subplots()
xgb.plot_importance(bst, ax=ax)
ax.set_title("Importancia de características para heart_stroke")
plt.tight_layout()
plt.show()

# ------------------------------
# 8) Guardar modelo y preprocesador
# ------------------------------
bst.save_model("xgb_heart_stroke.json")
joblib.dump(preprocessor, "preprocessor_heart_stroke.joblib")

# Para recargar luego:
# from pathlib import Path
# import joblib
# import xgboost as xgb
# preprocessor = joblib.load("preprocessor_heart_stroke.joblib")
# bst = xgb.Booster()
# bst.load_model("xgb_heart_stroke.json")