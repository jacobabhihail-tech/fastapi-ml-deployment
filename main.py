from fastapi import FastAPI
import pandas as pd
import joblib

app = FastAPI()

# Load new churn pipeline
model = joblib.load("churn_pipeline.pkl")

@app.get("/")
def home():
    return {"message": "Churn API running"}

@app.post("/predict")
def predict(data: dict):
    input_df = pd.DataFrame([data])

    prediction = model.predict(input_df)[0]
    probability = model.predict_proba(input_df)[0][1]

    return {
        "prediction": int(prediction),
        "churn_probability": float(probability)
    }