from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from database import conn, cursor  # DB connection

app = FastAPI()

# Load pipeline model
model = joblib.load("model_pipeline.pkl")

# Input schema (Pydantic validation)
class CustomerData(BaseModel):
    age: int
    balance: float

# Prediction endpoint
@app.post("/predict")
def predict(data: CustomerData):

    # Convert input to DataFrame
    input_data = pd.DataFrame({
        "age": [data.age],
        "balance": [data.balance]
    })

    # Model prediction
    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    # Save result to SQLite DB
    cursor.execute(
        "INSERT INTO predictions (age, balance, prediction, probability) VALUES (?, ?, ?, ?)",
        (data.age, data.balance, int(prediction), float(probability))
    )
    conn.commit()

    # Return response
    return {
        "prediction": int(prediction),
        "churn_probability": float(probability)
    }