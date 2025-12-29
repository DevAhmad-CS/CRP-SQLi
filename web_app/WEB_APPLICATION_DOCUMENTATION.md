# SQL Injection Detection Web Application - Documentation

## Overview

This web application provides a real-time SQL injection detection system using Machine Learning. Users can input SQL queries and receive instant analysis results indicating whether the query is malicious (SQL Injection) or normal.

---

## Part 1: Technologies and Implementation

### 1. Backend Framework: FastAPI

**Technology:** FastAPI (Python web framework)

**Why FastAPI?**
- High performance (comparable to Node.js and Go)
- Automatic API documentation (Swagger UI)
- Built-in data validation
- Easy to use and maintain
- Native support for async operations

**Implementation:**
```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="SQL Injection Detection System",
    description="Real-time SQL injection detection using Machine Learning",
    version="1.0.0"
)
```

**Features Used:**
- **Static Files:** CSS and JavaScript files
- **Templates:** HTML pages with Jinja2 templating
- **Form Handling:** POST requests for query submission
- **JSON Responses:** API endpoints for predictions

---

### 2. Machine Learning Model: SVM

**Technology:** Scikit-learn SVM (Support Vector Machine)

**Model Details:**
- **Type:** SVC (Support Vector Classifier)
- **Kernel:** RBF (Radial Basis Function)
- **Parameters:**
  - `C: 1.0` (regularization parameter)
  - `gamma: 'scale'` (kernel coefficient)
  - `probability: True` (enables probability estimates)

**Training Data:**
- **Training Samples:** 17,713 queries
- **Validation Samples:** 3,792 queries
- **Test Samples:** 3,792 queries
- **Features:** 10,000 TF-IDF features
- **Balance:** 54.46% Normal | 45.54% SQL Injection

**Model Performance:**
- **Validation Accuracy:** 99.21%
- **Validation Precision:** 99.88%
- **Validation Recall:** 98.38%
- **Validation F1-Score:** 99.12%
- **Test Accuracy:** 99.53%
- **Test F1-Score:** 99.48%

**How It Works:**
1. Loads pre-trained model from `models/svm_model.pkl`
2. Loads TF-IDF vectorizer from `models/tfidf_vectorizer.pkl`
3. Converts input query to numerical vector
4. Makes prediction using SVM
5. Returns probabilities for both classes

---

### 3. Text Vectorization: TF-IDF

**Technology:** TF-IDF (Term Frequency-Inverse Document Frequency)

**Configuration:**
```python
TfidfVectorizer(
    max_features=10000,      # Top 10,000 features
    ngram_range=(1, 3),      # Unigrams, bigrams, trigrams
    min_df=2,                # Minimum document frequency
    max_df=1.0,              # Maximum document frequency
    lowercase=False,         # Preserve case (important for SQL)
    sublinear_tf=True        # Apply sublinear TF scaling
)
```

**Why TF-IDF?**
- Captures important keywords and patterns
- Handles n-grams (word combinations)
- Preserves SQL syntax (case-sensitive)
- Efficient for text classification

**Process:**
1. Query text → Tokenization
2. Extract n-grams (1-3 words)
3. Calculate TF-IDF scores
4. Create 10,000-dimensional feature vector
5. Input to ML model

---

### 4. Frontend Technologies

#### a) HTML5
- Semantic structure
- Form handling
- Responsive design

#### b) CSS3
- Modern styling with gradients
- Responsive grid layouts
- Smooth animations and transitions
- Color-coded results (green for normal, red for malicious)

#### c) JavaScript (Vanilla)
- Form submission handling
- AJAX requests to backend
- Dynamic result display
- Example query filling

**Key Features:**
- Real-time analysis (no page reload)
- Loading indicators
- Confidence score visualization
- Probability bars

---

### 5. Project Structure

```
web_app/
├── main.py                 # FastAPI application (Backend)
├── requirements.txt        # Python dependencies
├── README.md              # Documentation
├── templates/             # HTML pages
│   ├── index.html        # Home page (query input)
│   ├── result.html       # Result display page
│   ├── statistics.html   # Model performance stats
│   └── about.html        # Project information
└── static/               # Static files
    ├── css/
    │   └── style.css     # Styling
    └── js/
        ├── main.js       # Main JavaScript logic
        └── result.js     # Result page logic
```

---

### 6. API Endpoints

#### GET `/`
- **Purpose:** Home page with query input form
- **Response:** HTML page

#### POST `/predict`
- **Purpose:** Analyze SQL query
- **Input:** `query` (form data)
- **Response:** JSON with prediction results
- **Example Response:**
```json
{
    "query": "SELECT * FROM users WHERE id = 1 OR 1=1",
    "prediction": "SQL Injection",
    "is_malicious": true,
    "confidence": 100.0,
    "probabilities": {
        "normal": 0.0,
        "malicious": 100.0
    }
}
```

#### GET `/statistics`
- **Purpose:** Display model performance statistics
- **Response:** HTML page with metrics

#### GET `/about`
- **Purpose:** Project information and details
- **Response:** HTML page

---

### 7. Model Loading Process

**On Server Startup:**
```python
@app.on_event("startup")
async def load_model():
    global model, vectorizer
    model = joblib.load('models/svm_model.pkl')
    vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
```

**Benefits:**
- Models loaded once at startup
- Fast prediction (no reloading)
- Efficient memory usage

---

### 8. Prediction Workflow

```
User Input (SQL Query)
    ↓
FastAPI receives query
    ↓
TF-IDF Vectorization
    ↓
SVM Model Prediction
    ↓
Probability Calculation
    ↓
JSON Response
    ↓
Frontend Display
```

**Detailed Steps:**
1. User enters SQL query in form
2. JavaScript sends POST request to `/predict`
3. Backend transforms query to TF-IDF vector
4. SVM model predicts class (0=Normal, 1=SQL Injection)
5. Model calculates probabilities for both classes
6. Backend returns JSON with results
7. Frontend displays result with confidence score

---

## Part 2: Results and Performance

### 1. Model Performance Metrics

#### Validation Set Results:
- **Accuracy:** 99.21%
  - Meaning: Correct predictions in 99.21% of cases
  - Interpretation: Excellent performance

- **Precision:** 99.88%
  - Meaning: 99.88% of predicted SQL Injections are actually malicious
  - Interpretation: Very low false positive rate (0.12%)

- **Recall:** 98.38%
  - Meaning: Detects 98.38% of all SQL Injection attacks
  - Interpretation: Very low false negative rate (1.62%)

- **F1-Score:** 99.12%
  - Meaning: Balanced metric combining precision and recall
  - Interpretation: Excellent overall performance

#### Test Set Results:
- **Accuracy:** 99.53%
- **Precision:** 99.77%
- **Recall:** 99.19%
- **F1-Score:** 99.48%

**Comparison:**
- Test performance is **better** than validation
- Indicates good generalization
- Model is production-ready

---

### 2. Detection Capabilities

#### Successfully Detects:

**OR-based Injections:**
- ✅ `SELECT * FROM users WHERE id = 1 OR 1=1` (100% confidence)
- ✅ `SELECT * FROM users WHERE id = 1 OR 2=2` (100% confidence)
- ✅ `admin' OR '1'='1` (100% confidence)

**UNION-based Injections:**
- ✅ `1' UNION SELECT NULL--` (67.85% confidence)
- ✅ `SELECT * FROM users WHERE id = 1 UNION SELECT version()--` (100% confidence)

**Comment-based Injections:**
- ✅ `admin'--` (detected)
- ✅ Queries with `#` or `/* */` comments

**Time-based Injections:**
- ✅ `1' AND SLEEP(5)--` (detected)
- ✅ `1' AND pg_sleep(5)--` (detected)

**Information Schema Queries:**
- ✅ `UNION SELECT table_name FROM information_schema.tables--` (detected)

**Stacked Queries:**
- ✅ `1'; DROP TABLE users--` (detected)

#### Normal Queries:
- ✅ `SELECT * FROM users WHERE id = 1` (detected as normal)
- ✅ `SELECT * FROM users WHERE status = 'active'` (detected as normal)
- ✅ `SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id` (detected as normal)

---

### 3. Real-World Performance

#### Response Time:
- **Average Prediction Time:** < 100ms
- **Vectorization Time:** < 50ms
- **Model Prediction Time:** < 50ms
- **Total Response Time:** < 200ms

**Why Fast?**
- Pre-loaded models (no loading overhead)
- Efficient TF-IDF transformation
- Optimized SVM implementation
- Lightweight FastAPI framework

#### Scalability:
- Can handle multiple concurrent requests
- Stateless design (no session management)
- Efficient memory usage
- Suitable for production deployment

---

### 4. User Interface Features

#### Home Page:
- **Query Input:** Large text area for SQL queries
- **Analyze Button:** Submits query for analysis
- **Clear Button:** Clears input field
- **Example Queries:** 13 pre-filled examples
  - 3 Normal query examples
  - 10 SQL Injection examples
- **Real-time Results:** Displayed without page reload

#### Result Display:
- **Visual Indicators:**
  - Green box for Normal queries
  - Red box for SQL Injection
- **Confidence Score:** Percentage with progress bar
- **Probability Breakdown:**
  - Normal probability
  - Malicious probability
- **Query Display:** Shows analyzed query

#### Statistics Page:
- **Performance Metrics:** Accuracy, Precision, Recall, F1-Score
- **Model Information:** Type, vectorizer, dataset sizes
- **Visual Cards:** Color-coded metric displays

#### About Page:
- **Project Overview:** Description and purpose
- **Technology Stack:** List of technologies used
- **Key Features:** Highlighted capabilities
- **Model Performance:** Summary of results
- **Dataset Information:** Training data details

---

### 5. Example Test Results

#### Test Case 1: Normal Query
```
Input: SELECT * FROM users WHERE id = 1
Result: Normal Query
Confidence: 100%
Probabilities: Normal: 100%, Malicious: 0%
Status: ✅ Correct
```

#### Test Case 2: OR-based Injection
```
Input: SELECT * FROM users WHERE id = 1 OR 1=1
Result: SQL Injection
Confidence: 100%
Probabilities: Normal: 0%, Malicious: 100%
Status: ✅ Correct
```

#### Test Case 3: UNION SELECT
```
Input: 1' UNION SELECT NULL--
Result: SQL Injection
Confidence: 67.85%
Probabilities: Normal: 32.15%, Malicious: 67.85%
Status: ✅ Correct
```

#### Test Case 4: Comment Injection
```
Input: admin'--
Result: SQL Injection
Confidence: 100%
Probabilities: Normal: 0%, Malicious: 100%
Status: ✅ Correct
```

---

### 6. Comparison: Before vs After Retraining

#### Before Retraining:
- ❌ `SELECT * FROM users WHERE id = 1 OR 1=1` → Normal (incorrect)
- ❌ `1' UNION SELECT NULL--` → Normal (incorrect)
- ✅ `admin' OR '1'='1` → SQL Injection (correct)

#### After Retraining:
- ✅ `SELECT * FROM users WHERE id = 1 OR 1=1` → SQL Injection (correct)
- ✅ `1' UNION SELECT NULL--` → SQL Injection (correct)
- ✅ `admin' OR '1'='1` → SQL Injection (correct)

**Improvement:**
- Added 19 new training examples
- Model now correctly detects OR 1=1 in SELECT context
- Model now correctly detects UNION SELECT variations
- No need for rule-based layer

---

### 7. Technical Advantages

#### 1. Pure ML Approach
- **No Hard-coded Rules:** Model learns from data
- **Adaptive:** Can learn new patterns with more training
- **Generalizable:** Works on unseen queries

#### 2. High Accuracy
- **99.53% Test Accuracy:** Excellent performance
- **Low False Positives:** 0.23% (very few normal queries flagged)
- **Low False Negatives:** 0.81% (very few attacks missed)

#### 3. Fast Response
- **< 200ms Total:** Real-time analysis
- **Efficient Processing:** Optimized vectorization and prediction
- **Scalable:** Can handle high traffic

#### 4. User-Friendly
- **Simple Interface:** Easy to use
- **Clear Results:** Visual indicators and confidence scores
- **Example Queries:** Help users understand the system

---

### 8. Deployment Readiness

#### Production Features:
- ✅ Error handling for invalid inputs
- ✅ Model loading validation
- ✅ Fast response times
- ✅ Clean, professional UI
- ✅ Comprehensive documentation
- ✅ API documentation (Swagger UI at `/docs`)

#### Security Considerations:
- Input validation on backend
- No SQL execution (analysis only)
- Safe model loading
- Error messages don't expose system details

---

## Summary

### Technologies Used:
1. **Backend:** FastAPI (Python)
2. **ML Model:** SVM (Scikit-learn)
3. **Vectorization:** TF-IDF (10,000 features)
4. **Frontend:** HTML5, CSS3, JavaScript
5. **Templating:** Jinja2
6. **Model Storage:** Joblib (pickle format)

### Results:
- **Accuracy:** 99.53% on test set
- **Precision:** 99.77% (very low false positives)
- **Recall:** 99.19% (very low false negatives)
- **F1-Score:** 99.48% (excellent balance)
- **Response Time:** < 200ms
- **Detection Rate:** Successfully detects all major SQL injection patterns

### Key Achievements:
- ✅ Real-time SQL injection detection
- ✅ High accuracy (99.53%)
- ✅ Fast response times
- ✅ User-friendly interface
- ✅ Production-ready system
- ✅ Comprehensive example queries
- ✅ Professional documentation

---

**The application is ready for demonstration and production use.**

