from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.schema import IrisInput
import numpy as np, joblib, logging

# Load the model
model = joblib.load("model/iris_model.pkl")

# Set up logging
logging.basicConfig(filename="api.log", level=logging.INFO,
                    format="%(asctime)s - %(message)s")

# Initialize FastAPI app
app = FastAPI()

@app.post("/predict")
def predict(input_data: IrisInput, background_tasks: BackgroundTasks):
    try:
        data = np.array([[input_data.sepal_length,
                          input_data.sepal_width,
                          input_data.petal_length,
                          input_data.petal_width]])
        
        # Run prediction
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0]
        species = ["setosa", "versicolor", "virginica"][pred]

        # Log in the background so it doesn’t block response
        background_tasks.add_task(log_request, input_data, species)

        # Return prediction and probabilities
        return {
            "prediction": species,
            "class_index": int(pred),
            "probabilities": {
                "setosa": float(proba[0]),
                "versicolor": float(proba[1]),
                "virginica": float(proba[2])
            }
        }

    except Exception as e:
        logging.exception("Prediction failed")
        raise HTTPException(status_code=500, detail="Internal error")
    
# Background logging task
def log_request(data: IrisInput, prediction: str):
    logging.info(f"Input: {data.model_dump()} | Prediction: {prediction}")