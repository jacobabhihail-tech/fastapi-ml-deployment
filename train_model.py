import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import joblib

# Simple dataset
data = {
    "age": [25, 30, 45, 35, 50],
    "balance": [20000, 50000, 100000, 75000, 120000],
    "churn": [0, 0, 1, 0, 1]
}

df = pd.DataFrame(data)

X = df[["age", "balance"]]
y = df["churn"]

# Create pipeline
pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", LogisticRegression())
])

# Train
pipeline.fit(X, y)

# Save pipeline (IMPORTANT change)
joblib.dump(pipeline, "model_pipeline.pkl")

print("✅ Pipeline model saved")