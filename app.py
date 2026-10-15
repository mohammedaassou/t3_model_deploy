import os
import joblib
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris inference")
model = joblib.load(MODEL_PATH)

class Flower(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(f: Flower):
    x = [[f.sepal_length, f.sepal_width, f.petal_length, f.petal_width]]
    return {"class": CLASSES[int(model.predict(x)[0])]}
