# Iris REST API

A simple FastAPI-based REST API for predicting Iris flower species using a trained **RandomForest** model.

## Project Structure

```
ml-api/
│
├── model/
│   └── train_model.py      # Script to train and save the model
│   └── iris_model.pkl      # Trained model file
├── app/
│   └── main.py             # FastAPI app
│   └── schema.py           # Input data schema using Pydantic
├── requirements.txt        # All dependencies
└── README.md               # Optional documentation
```

### POST `/predict`

Predict the species of an Iris flower.

**Request Body (JSON):**
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
    "setosa": 0.98,
    "versicolor": 0.01,
    "virginica": 0.01
  }
}
```

## Logging

All prediction requests are logged asynchronously to `api.log`.