"""
اختبار إصلاح DROP TABLE
"""

import sys
import os

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

import joblib
from pathlib import Path

print("=" * 80)
print("اختبار إصلاح DROP TABLE")
print("=" * 80)

# Load model and vectorizer
base_dir = Path(__file__).parent.parent
models_dir = base_dir / 'models'

print("\n1. Loading model and vectorizer...")
try:
    model = joblib.load(models_dir / 'svm_model.pkl')
    vectorizer = joblib.load(models_dir / 'tfidf_vectorizer.pkl')
    print("   [OK] Model loaded!")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")
    sys.exit(1)

# Test the problematic query
test_queries = [
    "1'; DROP TABLE users--",
    "1' ; DROP TABLE users--",
    "1';DROP TABLE users--",
    "1'; DELETE FROM users--",
    "1'; UPDATE users SET password='hacked'--",
    "SELECT * FROM users WHERE id=1; DROP TABLE users--",
]

print("\n2. Testing DROP TABLE queries...")
for query in test_queries:
    query_vec = vectorizer.transform([query])
    prediction_proba = model.predict_proba(query_vec)[0]
    normal_prob = prediction_proba[0]
    malicious_prob = prediction_proba[1]
    
    # Use probability-based prediction (same as in main.py)
    is_malicious = malicious_prob > 0.5
    confidence = malicious_prob * 100 if is_malicious else normal_prob * 100
    
    status = "✅" if is_malicious else "❌"
    label = "SQL Injection" if is_malicious else "Normal Query"
    
    print(f"\n   {status} '{query[:50]}...'")
    print(f"      -> {label} ({confidence:.2f}% confidence)")
    print(f"      -> Normal: {normal_prob*100:.2f}%, Malicious: {malicious_prob*100:.2f}%")

print("\n" + "=" * 80)
print("[SUCCESS] Test completed!")
print("=" * 80)

