from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import logging
from database import conn, cursor

# ------------------ Logging Setup ------------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ------------------ App ------------------
app = FastAPI()

# Load model safely
try:
    model = joblib.load("model_pipeline.pkl")
    logging.info("Model loaded successfully")
except Exception as e:
    logging.error(f"Error loading model: {e}")
    raise e

# ------------------ Input Schema ------------------
class CustomerData(BaseModel):
    age: int
    balance: float

# ------------------ Endpoint ------------------
@app.post("/predict")
def predict(data: CustomerData):
    try:
        logging.info(f"Received input: age={data.age}, balance={data.balance}")

        # Convert input
        input_data = pd.DataFrame({
            "age": [data.age],
            "balance": [data.balance]
        })

        # Prediction
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1]

        logging.info(f"Prediction: {prediction}, Probability: {probability}")

        # Save to DB
        cursor.execute(
            "INSERT INTO predictions (age, balance, prediction, probability) VALUES (?, ?, ?, ?)",
            (data.age, data.balance, int(prediction), float(probability))
        )
        conn.commit()

        return {
            "prediction": int(prediction),
            "churn_probability": float(probability)
        }

    except Exception as e:
        logging.error(f"Error during prediction: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong")