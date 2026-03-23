from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return{"messge": "API is working"}