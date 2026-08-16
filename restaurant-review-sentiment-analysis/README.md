# Restaurant Review Sentiment Analysis

Classifies restaurant reviews as positive or negative using text preprocessing (regex cleaning, stopword removal, stemming), a bag-of-words model (`CountVectorizer`), and a `MultinomialNB` classifier.

## Tech Stack
- Python, NLTK, Scikit-learn, Seaborn/Matplotlib

## Files
- `main.ipynb` — preprocessing, training, and evaluation (accuracy, precision, recall, F1, confusion matrix)
- `data/` — review dataset
- `future_scope.png` — notes/ideas for extending the project

## Run

```bash
jupyter notebook main.ipynb
```

Note: first run will need `nltk.download('stopwords')`.
