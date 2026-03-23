import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

# Load data
df = pd.read_excel("Telco_churn.xlsx")

# Basic cleaning (same as your notebook)
df = df.drop(columns=[
    "CustomerID", "Lat Long", "Latitude", "Longitude",
    "Zip Code", "Churn Reason", "Churn Label",
    "Churn Score", "CLTV", "Country", "State", "City"
])

df["Total Charges"] = pd.to_numeric(df["Total Charges"], errors="coerce")
df = df.dropna(subset=["Total Charges"])

# Split features/target
X = df.drop("Churn Value", axis=1)
y = df["Churn Value"]

# Column types
categorical_cols = X.select_dtypes(include=["object"]).columns
numeric_cols = X.select_dtypes(exclude=["object"]).columns

# Preprocessing
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols)
])

# Full pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000))
])

# Train
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model.fit(X_train, y_train)

# Save pipeline
joblib.dump(model, "churn_pipeline.pkl")

print("✅ Churn pipeline saved successfully")