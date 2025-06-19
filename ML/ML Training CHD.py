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
# Cargar dataset
# ------------------------------
# Ajusta la ruta a tu CSV local
data_path = Path("C:/Users/frent/Desktop/Project_HC/heart_disease_uci.csv")
df = pd.read_csv(data_path)

# ------------------------------
# Detectar columna objetivo y binarizar
# ------------------------------
# Nuestro CSV usa 'TenYearCHD' como variable objetivo
if "TenYearCHD" in df.columns:
    target_col = "TenYearCHD"
elif "target" in df.columns:
    target_col = "target"
elif "num" in df.columns:
    target_col = "num"
else:
    raise ValueError(f"No encuentro columna objetivo esperada en {df.columns.tolist()}")

# Separar características y objetivo
define_features = df.drop(target_col, axis=1)
X_df = df.drop(target_col, axis=1)
y_raw = df[target_col]

# Binarizar etiquetas: ya vienen 0/1 en TenYearCHD
if set(y_raw.unique()) <= {0,1}:
    y = y_raw.astype(int)
else:
    y = (y_raw > 0).astype(int)

X_df = df.drop(target_col, axis=1)
y_raw = df[target_col]

# Binarizar etiquetas: 0 = sano, 1 = enfermedad (num>0)
y = (y_raw > 0).astype(int)

# ------------------------------
# Preprocesamiento mixto
# ------------------------------
# Identificar columnas numéricas y categóricas
numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = X_df.select_dtypes(exclude=[np.number]).columns.tolist()

# Pipeline para numéricos: imputar con mediana + escalar
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Pipeline para categóricos: imputar con moda + one-hot encoding
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Componer transformador
preprocessor = ColumnTransformer([
    ('num', numeric_pipeline, numeric_cols),
    ('cat', categorical_pipeline, cat_cols)
])

# Aplicar preprocesamiento
X = preprocessor.fit_transform(X_df)

# División en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------
# Entrenamiento XGBoost
# ------------------------------
# Convertir a DMatrix de XGBoost
# Aseguramos que labels estén en [0,1]
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Parámetros básicos
params = {
    'objective': 'binary:logistic',
    'eval_metric': 'auc'
}

# Entrenar con early stopping
bst = xgb.train(
    params,
    dtrain,
    num_boost_round=100,
    evals=[(dtest, 'test')],
    early_stopping_rounds=10,
    verbose_eval=True
)

# Evaluación
y_pred_prob = bst.predict(dtest)
auc = roc_auc_score(y_test, y_pred_prob)
print(f"AUC en test: {auc:.3f}")

# ------------------------------
# Importancia de características
# ------------------------------
fig, ax = plt.subplots()
xgb.plot_importance(bst, ax=ax)
ax.set_title("Importancia de características")
plt.tight_layout()
plt.show()

# ------------------------------
# Guardar modelo y preprocesador
# ------------------------------
bst.save_model("modelo_xgb.json")
joblib.dump(preprocessor, "preprocessor.joblib")

# Para recargar:
# modelo = xgb.Booster()
# modelo.load_model("modelo_xgb.json")
# preprocessor = joblib.load("preprocessor.joblib")
