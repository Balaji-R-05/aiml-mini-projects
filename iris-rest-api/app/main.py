from fastapi import FastAPI, HTTPException, BackgroundTasks
from schema import IrisInput
import numpy as np
import joblib
import logging

# ---------------- LOGGING ----------------
logger = logging.getLogger("iris_api")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler("api.log")
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(file_handler)

# ---------------- APP ----------------
app = FastAPI()
model = None

CLASS_NAMES = ["setosa", "versicolor", "virginica"]
MODEL_PATH = "model/iris_model.pkl"

@app.on_event("startup")
def load_model():
    global model
    try:
        model = joblib.load(MODEL_PATH)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.exception("Failed to load model")
        raise RuntimeError("Model loading failed") from e

@app.post("/predict")
def predict(input_data: IrisInput, background_tasks: BackgroundTasks):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    try:
        data = np.array([[input_data.sepal_length,
                          input_data.sepal_width,
                          input_data.petal_length,
                          input_data.petal_width]])

        pred = model.predict(data)[0]
        species = CLASS_NAMES[int(pred)]

        response = {
            "prediction": species,
            "class_index": int(pred)
        }

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(data)[0]
            response["probabilities"] = dict(
                zip(CLASS_NAMES, map(float, proba))
            )

        background_tasks.add_task(log_request, input_data, species)
        return response

    except Exception:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Internal error")


# ---------------- BACKGROUND TASK ----------------
def log_request(data: IrisInput, prediction: str):
    payload = data.dict() if hasattr(data, "dict") else data.model_dump()
    logger.info(f"Input: {payload} | Prediction: {prediction}")


@app.get("/health")
def health_check():
    status:dict = {
        "status": "ok",
        "model_loaded": model is not None,
        "service": "iris-classifier-api"
    }

    logger.info(
        "Health check called | model_loaded=%s",
        status["model_loaded"]
    )

    return status