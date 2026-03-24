from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()

# Load pipeline (not just model)
model = joblib.load("model_pipeline.pkl")

class CustomerData(BaseModel):
    age: int
    balance: float

@app.post("/predict")
def predict(data: CustomerData):

    input_data = pd.DataFrame({
        "age": [data.age],
        "balance": [data.balance]
    })

    prediction = model.predict(input_data)[0]
    probability = model.predict_proba(input_data)[0][1]

    return {
        "prediction": int(prediction),
        "churn_probability": float(probability)
    }