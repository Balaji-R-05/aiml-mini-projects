# House Price Prediction

This project uses **Simple Linear Regression** to predict house prices based on the square footage (area) of the property.

## 📊 Dataset

The project uses `house_dataset.csv`, which contains:
- `area`: The area of the house in square feet.
- `price`: The price of the house (target variable).

## 🛠️ Implementation Details

- **Model**: Linear Regression from `scikit-learn`.
- **Visualization**: Plotting the regression line using `matplotlib`.
- **Workflow**:
  - Data loading with `pandas`.
  - Train-test split.
  - Model training.
  - Prediction and performance evaluation.

## 🚀 How to Run

1. Ensure you have the [main requirements](../requirements.txt) installed.
2. Open the `main.ipynb` file in Jupyter Notebook or VS Code.
3. Run all cells to see the data analysis and model performance.

## 📈 Future Scope

- Expanding the model to **Multiple Linear Regression** by adding features like number of bedrooms, age of the house, etc.
- Implementing feature scaling.