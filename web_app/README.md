# SQL Injection Detection Web Application

A real-time web application for detecting SQL injection attacks using Machine Learning.

## Features

- ✅ Real-time SQL query analysis
- ✅ High accuracy (99.53% on test set)
- ✅ Confidence scores for predictions
- ✅ Example queries for testing
- ✅ Model performance statistics
- ✅ Modern, responsive UI

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Make sure the trained model files are in the parent `models/` directory:
   - `models/svm_model.pkl`
   - `models/tfidf_vectorizer.pkl`

## Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Project Structure

```
web_app/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── index.html      # Home page
│   ├── result.html     # Result page
│   ├── statistics.html # Statistics page
│   └── about.html      # About page
└── static/             # Static files
    ├── css/
    │   └── style.css   # Stylesheet
    └── js/
        ├── main.js     # Main JavaScript
        └── result.js   # Result page JavaScript
```

## API Endpoints

- `GET /` - Home page with query input form
- `POST /predict` - Analyze SQL query (returns JSON)
- `GET /statistics` - Model performance statistics
- `GET /about` - About page

## Usage

1. Enter a SQL query in the input field
2. Click "Analyze Query"
3. View the prediction result with confidence score
4. Try example queries from the examples section

## Model Information

- **Model Type:** SVM (Support Vector Machine)
- **Vectorizer:** TF-IDF (10,000 features)
- **Accuracy:** 99.53%
- **Precision:** 99.77%
- **Recall:** 99.19%
- **F1-Score:** 99.48%

## Notes

- The application loads the model on startup
- Make sure model files are accessible from the parent directory
- The application runs on port 8000 by default

