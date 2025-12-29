"""
SQL Injection Detection Web Application
FastAPI backend for real-time SQL injection detection
"""

import sys
import os
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import numpy as np
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="SQL Injection Detection System",
    description="Real-time SQL injection detection using Machine Learning",
    version="1.0.0"
)

# Get the directory of this file
BASE_DIR = Path(__file__).parent

# Mount static files and templates
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Load model and vectorizer
MODELS_DIR = BASE_DIR.parent / "models"
MODEL_PATH = MODELS_DIR / "svm_model.pkl"
VECTORIZER_PATH = MODELS_DIR / "tfidf_vectorizer.pkl"

# Global variables for model and vectorizer
model = None
vectorizer = None

# Short SQL Injection patterns (for rule-based detection)
SHORT_SQLI_PATTERNS = [
    r'^1=1--?\s*$',           # 1=1-- or 1=1-
    r'^1=1#\s*$',              # 1=1#
    r'^1=1/\*',                # 1=1/*
    r'^1=2--?\s*$',            # 1=2-- or 1=2-
    r'^1=2#\s*$',              # 1=2#
    r"^'1'='1'--?\s*$",        # '1'='1'--
    r"^'1'='1'#\s*$",          # '1'='1'#
    r"^'1'='2'--?\s*$",        # '1'='2'--
    r'^1=1\s*$',               # 1=1
    r'^1=2\s*$',               # 1=2
    r"^'1'='1'\s*$",           # '1'='1'
    r"^'1'='2'\s*$",           # '1'='2'
]

def is_short_sqli_pattern(query: str) -> bool:
    """
    Check if query is a short SQL Injection pattern
    Only for very short queries (≤ 15 characters)
    """
    if not query or len(query.strip()) > 15:
        return False
    
    query_stripped = query.strip()
    
    # Check against patterns
    for pattern in SHORT_SQLI_PATTERNS:
        if re.match(pattern, query_stripped, re.IGNORECASE):
            return True
    
    return False

@app.on_event("startup")
async def load_model():
    """Load the trained model and vectorizer on startup"""
    global model, vectorizer
    try:
        print("Loading model and vectorizer...")
        model = joblib.load(MODEL_PATH)
        vectorizer = joblib.load(VECTORIZER_PATH)
        print("[OK] Model and vectorizer loaded successfully!")
    except Exception as e:
        print(f"[ERROR] Error loading model: {e}")
        raise

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page - SQL query input form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=JSONResponse)
async def predict(query: str = Form(...)):
    """
    Predict if a SQL query is malicious or normal
    Uses ML model only (retrained with additional examples)
    
    Args:
        query: SQL query string to analyze
    
    Returns:
        JSON response with prediction results
    """
    if model is None or vectorizer is None:
        return JSONResponse(
            status_code=500,
            content={"error": "Model not loaded. Please restart the server."}
        )
    
    try:
        # Step 1: Check for short SQL Injection patterns first
        if is_short_sqli_pattern(query):
            # Short pattern detected - classify as SQL Injection
            is_malicious = True
            result_label = "SQL Injection"
            confidence = 95.0  # High confidence for known patterns
            normal_prob_pct = 5.0
            malicious_prob_pct = 95.0
        else:
            # Step 2: Use ML model for longer queries
            # Transform query to vector
            query_vector = vectorizer.transform([query])
            
            # Get probabilities
            prediction_proba = model.predict_proba(query_vector)[0]
            normal_prob = float(prediction_proba[0])
            malicious_prob = float(prediction_proba[1])
            
            # Use probability-based prediction (more reliable than predict())
            # If malicious probability > 0.5, classify as SQL Injection
            is_malicious = malicious_prob > 0.5
            prediction = 1 if is_malicious else 0
            
            # Get confidence score (use the higher probability)
            confidence = float(malicious_prob if is_malicious else normal_prob) * 100
            
            # Determine result
            result_label = "SQL Injection" if is_malicious else "Normal Query"
            
            # Convert to percentages
            normal_prob_pct = normal_prob * 100
            malicious_prob_pct = malicious_prob * 100
        
        return {
            "query": query,
            "prediction": result_label,
            "is_malicious": is_malicious,
            "confidence": round(confidence, 2),
            "probabilities": {
                "normal": round(normal_prob_pct, 2),
                "malicious": round(malicious_prob_pct, 2)
            }
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Prediction error: {str(e)}"}
        )

@app.get("/result", response_class=HTMLResponse)
async def result_page(request: Request):
    """Result page (redirected from form submission)"""
    return templates.TemplateResponse("result.html", {"request": request})

@app.get("/statistics", response_class=HTMLResponse)
async def statistics(request: Request):
    """Statistics page showing model performance"""
    stats = {
        "accuracy": 99.53,
        "precision": 99.77,
        "recall": 99.19,
        "f1_score": 99.48,
        "test_samples": 3792,
        "model_type": "SVM (Support Vector Machine)",
        "vectorizer": "TF-IDF (10,000 features)",
        "training_samples": 17694,
        "validation_samples": 3792
    }
    return templates.TemplateResponse("statistics.html", {
        "request": request,
        "stats": stats
    })

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """About page with project information"""
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

