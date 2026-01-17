# Iris Species Prediction API

A FastAPI-based REST API that predicts Iris flower species using a RandomForest classifier. This application is fully dockerized for easy deployment.

## Project Structure

- `app/`: Contains the application code (main.py, schema.py, Dockerfile).
- `app/model/`: Contains the trained model file.
- `app/requirements.txt`: Python dependencies.

## Setup

1. Navigate to the `app` directory:
   ```bash
   cd app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Train the model:
   ```bash
   python train_model.py
   ```

## Running the Application

### Locally
Run the following command in the `app/` directory:
```bash
fastapi dev main.py
```
The API will be available at `http://127.0.0.1:8000`.

### With Docker
Build and run the container from the `app/` directory:
```bash
docker build -t iris-rest-api .
docker run -p 8000:8000 iris-rest-api
```

## API Endpoints

### POST /predict
Predicts the species based on sepal and petal measurements.

**Request Body:**
```json
{
  "sepal_length": 5.1,
  "sepal_width": 3.5,
  "petal_length": 1.4,
  "petal_width": 0.2
}
```

**Response:**
```json
{
  "prediction": "setosa",
  "class_index": 0,
  "probabilities": {
    "setosa": 1.0,
    "versicolor": 0.0,
    "virginica": 0.0
  }
}
```

### GET /health
Checks the health of the service.

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "service": "iris-classifier-api"
}
```

## Logging
Prediction requests are logged to `api.log` in the application directory.