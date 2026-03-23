import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

# Create simple dataset
data = {
    "age": [25, 40, 35, 50, 23, 60, 48, 33],
    "balance": [1000, 2000, 1500, 3000, 800, 4000, 2500, 1200],
    "churn": [0, 1, 0, 1, 0, 1, 1, 0]
}

df = pd.DataFrame(data)

# Features & target
X = df[["age", "balance"]]
y = df["churn"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "simple_model.pkl")

print("✅ Model trained and saved")