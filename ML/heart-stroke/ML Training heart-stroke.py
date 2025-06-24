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
# 2) Definir columna objetivo
# ------------------------------
target_col = "heart_stroke"
if target_col not in df.columns:
    raise ValueError(f"No encuentro la columna objetivo '{target_col}' en {df.columns.tolist()}")

X_df = df.drop(columns=[target_col])
y_raw = df[target_col]

# Asegurar que los valores sean 0/1
if set(y_raw.unique()) <= {0, 1}:
    y = y_raw.astype(int)
else:
    y = (y_raw > 0).astype(int)

# ------------------------------
# 3) Selección explícita de columnas (ordenadas)
# ------------------------------
feature_cols = [
    'male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
    'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol',
    'sysBP', 'diaBP', 'BMI', 'heartRate', 'glucose'
]
X_df = X_df[feature_cols]

# ------------------------------
# 4) Preprocesamiento mixto
# ------------------------------
numeric_cols = X_df.select_dtypes(include=[np.number]).columns.tolist()
cat_cols = X_df.select_dtypes(exclude=[np.number]).columns.tolist()

numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
]) if cat_cols else None

transformers = [('num', numeric_pipeline, numeric_cols)]
if categorical_pipeline:
    transformers.append(('cat', categorical_pipeline, cat_cols))

preprocessor = ColumnTransformer(transformers)

# Aplicar transformaciones
X = preprocessor.fit_transform(X_df)

# ------------------------------
# 5) Train/Test Split
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# ------------------------------
# 6) Entrenamiento del modelo XGBoost
# ------------------------------
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest  = xgb.DMatrix(X_test, label=y_test)

params = {
    'objective': 'binary:logistic',
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
# 7) Evaluación del modelo
# ------------------------------
y_pred_prob = bst.predict(dtest)
auc = roc_auc_score(y_test, y_pred_prob)
print(f"✅ AUC en test: {auc:.3f}")

# ------------------------------
# 8) Importancia de características
# ------------------------------
fig, ax = plt.subplots()
xgb.plot_importance(bst, ax=ax)
ax.set_title("Importancia de características para Heart Stroke")
plt.tight_layout()
plt.show()

# ------------------------------
# 9) Guardado de modelo y preprocesador
# ------------------------------
bst.save_model("xgb_heart_stroke.json")
joblib.dump(preprocessor, "preprocessor_heart_stroke.joblib")

# Puedes recargarlo luego con:
# model = xgb.Booster()
# model.load_model("xgb_heart_stroke.json")
# preproc = joblib.load("preprocessor_heart_stroke.joblib")
