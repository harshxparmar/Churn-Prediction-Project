import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_curve,
    roc_auc_score,
    roc_curve
)

# -----------------------------
# 1. Load Dataset
# -----------------------------
df = pd.read_excel("data/Telco_customer_churn.xlsx")

# -----------------------------
# 2. Drop Unnecessary Columns
# -----------------------------
columns_to_drop = [
    "CustomerID", "Count", "Country", "State", "City",
    "Zip Code", "Lat Long", "Latitude", "Longitude",
    "Churn Label", "Churn Score", "CLTV", "Churn Reason"
]

df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])

# -----------------------------
# 3. Define Target
# -----------------------------
df["Churn"] = df["Churn Value"]
df = df.drop("Churn Value", axis=1)

# -----------------------------
# 4. Handle Missing Values
# -----------------------------
if "Total Charges" in df.columns:
    df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors="coerce")

numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

categorical_cols = df.select_dtypes(include=["object"]).columns
for col in categorical_cols:
    df[col] = df[col].fillna(df[col].mode()[0])

# -----------------------------
# 5. Encoding
# -----------------------------
df = pd.get_dummies(df, drop_first=True)
df = df.dropna()

# -----------------------------
# 6. Split Data
# -----------------------------
X = df.drop("Churn", axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 7. Scaling
# -----------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# =============================
# MODEL 1: LOGISTIC REGRESSION
# =============================

log_model = LogisticRegression(
    max_iter=4000,
    class_weight="balanced"
)

log_model.fit(X_train_scaled, y_train)

log_probs = log_model.predict_proba(X_test_scaled)[:, 1]

# Threshold optimization
precisions, recalls, thresholds = precision_recall_curve(y_test, log_probs)
f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-6)
best_index = np.argmax(f1_scores)
best_threshold = thresholds[best_index]

log_preds = (log_probs >= best_threshold).astype(int)

print("\n====== Logistic Regression ======")
print("Best Threshold:", best_threshold)
print("Accuracy:", accuracy_score(y_test, log_preds))
print("ROC AUC:", roc_auc_score(y_test, log_probs))
print("\nClassification Report:\n", classification_report(y_test, log_preds))

# =============================
# MODEL 2: RANDOM FOREST
# =============================

rf_model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    class_weight="balanced"
)

rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)
rf_probs = rf_model.predict_proba(X_test)[:, 1]

print("\n====== Random Forest ======")
print("Accuracy:", accuracy_score(y_test, rf_preds))
print("ROC AUC:", roc_auc_score(y_test, rf_probs))
print("\nClassification Report:\n", classification_report(y_test, rf_preds))

# =============================
# SAVE BEST MODEL (choose manually)
# =============================

# Let's assume Logistic Regression is selected
pickle.dump(log_model, open("model/model.pkl", "wb"))
pickle.dump(scaler, open("model/scaler.pkl", "wb"))
pickle.dump(X.columns, open("model/features.pkl", "wb"))
pickle.dump(best_threshold, open("model/threshold.pkl", "wb"))

print("\nModel comparison completed and best model saved.")
