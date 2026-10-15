import os
import joblib
import redis
from fastapi import FastAPI
from pydantic import BaseModel

MODEL_PATH = os.getenv("MODEL_PATH", "/models/model.joblib")
CLASSES = ["setosa", "versicolor", "virginica"]

app = FastAPI(title="Iris inference")
model = joblib.load(MODEL_PATH)
counter = redis.Redis(host=os.getenv("REDIS_HOST", "base"), port=6379, decode_responses=True)

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
    predicted_class = CLASSES[int(model.predict(x)[0])]
    counter.incr("predictions")
    return {"class": predicted_class}

@app.get("/stats")
def stats():
    return {"predictions": int(counter.get("predictions") or 0)}
