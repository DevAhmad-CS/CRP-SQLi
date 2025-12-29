"""
اختبار الاستعلام 1=1--
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
print("اختبار الاستعلام: 1=1--")
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

# Test queries
test_queries = [
    ("1=1--", "جزء من SQL Injection (Boolean-based)"),
    ("1=1", "جزء من SQL Injection"),
    ("1=1#", "جزء من SQL Injection"),
    ("OR 1=1--", "SQL Injection pattern"),
    ("OR 1=1", "SQL Injection pattern"),
    ("' OR 1=1--", "SQL Injection pattern"),
    ("1' OR 1=1--", "SQL Injection pattern"),
    ("admin' OR 1=1--", "SQL Injection pattern"),
]

print("\n2. Testing queries...")
print("\n   تحليل:")
print("   - '1=1--' لوحده ليس استعلام SQL كامل")
print("   - لكنه جزء من هجوم SQL Injection (Boolean-based)")
print("   - عادة يكون في سياق: SELECT * FROM users WHERE id = 1 OR 1=1--")
print("   - يجب تصنيفه كـ SQL Injection لأنه نمط هجومي واضح\n")

for query, description in test_queries:
    query_vec = vectorizer.transform([query])
    prediction_proba = model.predict_proba(query_vec)[0]
    normal_prob = prediction_proba[0]
    malicious_prob = prediction_proba[1]
    
    # Use probability-based prediction
    is_malicious = malicious_prob > 0.5
    confidence = malicious_prob * 100 if is_malicious else normal_prob * 100
    
    status = "✅" if is_malicious else "❌"
    label = "SQL Injection" if is_malicious else "Normal Query"
    
    print(f"   {status} '{query}'")
    print(f"      -> {label} ({confidence:.2f}% confidence)")
    print(f"      -> Normal: {normal_prob*100:.2f}%, Malicious: {malicious_prob*100:.2f}%")
    print(f"      -> {description}")
    print()

print("=" * 80)
print("الخلاصة:")
print("=" * 80)
print("   - '1=1--' هو جزء من SQL Injection (Boolean-based)")
print("   - يجب تصنيفه كـ SQL Injection")
print("   - إذا النموذج يعطيه Normal → يجب إضافته للتدريب")

