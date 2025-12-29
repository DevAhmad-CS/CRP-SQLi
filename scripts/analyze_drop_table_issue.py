"""
تحليل مشكلة DROP TABLE detection
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
import pandas as pd
from pathlib import Path

print("=" * 80)
print("تحليل مشكلة DROP TABLE detection")
print("=" * 80)

# Load model and vectorizer
base_dir = Path(__file__).parent.parent
models_dir = base_dir / 'models'
dataset_dir = base_dir / 'dataset' / 'final'

print("\n1. Loading model and vectorizer...")
try:
    model = joblib.load(models_dir / 'svm_model.pkl')
    vectorizer = joblib.load(models_dir / 'tfidf_vectorizer.pkl')
    print("   [OK] Model loaded!")
except Exception as e:
    print(f"   [ERROR] Failed: {e}")
    sys.exit(1)

# Test the problematic query
test_query = "1'; DROP TABLE users--"

print(f"\n2. Testing query: {test_query}")

query_vec = vectorizer.transform([test_query])
prediction = model.predict(query_vec)[0]
prediction_proba = model.predict_proba(query_vec)[0]

print(f"\n   Results:")
print(f"      - Prediction (class): {prediction} ({'SQL Injection' if prediction == 1 else 'Normal Query'})")
print(f"      - Probability [Normal]: {prediction_proba[0]:.4f} ({prediction_proba[0]*100:.2f}%)")
print(f"      - Probability [Malicious]: {prediction_proba[1]:.4f} ({prediction_proba[1]*100:.2f}%)")
print(f"      - Confidence (chosen class): {prediction_proba[prediction]*100:.2f}%")

# Check if similar queries exist in training data
print("\n3. Checking training data for similar queries...")
train_df = pd.read_csv(dataset_dir / 'train_final.csv')

# Search for DROP TABLE queries
drop_queries = train_df[train_df['Query'].str.contains('DROP TABLE', case=False, na=False)]
print(f"   [OK] Found {len(drop_queries)} queries with 'DROP TABLE' in training data")

if len(drop_queries) > 0:
    print(f"\n   Examples:")
    for idx, row in drop_queries.head(5).iterrows():
        print(f"      - Label {row['Label']}: {row['Query'][:70]}...")

# Search for queries starting with "1'"
queries_start_1 = train_df[train_df['Query'].str.startswith("1'", na=False)]
print(f"\n   [OK] Found {len(queries_start_1)} queries starting with '1'' in training data")

if len(queries_start_1) > 0:
    sqli_1 = queries_start_1[queries_start_1['Label'] == 1]
    normal_1 = queries_start_1[queries_start_1['Label'] == 0]
    print(f"      - SQL Injection: {len(sqli_1)}")
    print(f"      - Normal: {len(normal_1)}")

# Check exact match
exact_match = train_df[train_df['Query'] == test_query]
print(f"\n   [OK] Exact match found: {len(exact_match)}")

if len(exact_match) > 0:
    for idx, row in exact_match.iterrows():
        print(f"      - Label {row['Label']}: {row['Query']}")

# Test variations
print("\n4. Testing variations...")
variations = [
    "1'; DROP TABLE users--",
    "1' ; DROP TABLE users--",
    "1';DROP TABLE users--",
    "SELECT * FROM users WHERE id=1; DROP TABLE users--",
    "1'; DELETE FROM users--",
    "1'; UPDATE users SET password='hacked'--",
]

for var_query in variations:
    var_vec = vectorizer.transform([var_query])
    var_pred = model.predict(var_vec)[0]
    var_proba = model.predict_proba(var_vec)[0]
    status = "✅" if var_pred == 1 else "❌"
    print(f"   {status} '{var_query[:50]}...' -> {'SQL Injection' if var_pred == 1 else 'Normal'} ({var_proba[1]*100:.2f}%)")

print("\n" + "=" * 80)
print("الخلاصة:")
print("=" * 80)
print(f"   - Query: {test_query}")
print(f"   - Prediction: {'SQL Injection' if prediction == 1 else 'Normal Query'}")
print(f"   - Malicious Probability: {prediction_proba[1]*100:.2f}%")
print(f"   - Normal Probability: {prediction_proba[0]*100:.2f}%")
print(f"   - Problem: {'Malicious probability > 50% but predicted as Normal' if prediction == 0 and prediction_proba[1] > 0.5 else 'OK'}")

