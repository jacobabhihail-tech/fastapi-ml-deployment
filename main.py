from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"messge": "API is working"}

@app.get("/predict")
def predict(age: int, balance: float):
    return{
        "age":age,
        "balance": balance,
        "prediction":"churn" if balance < 5000 else "no churn"
    }