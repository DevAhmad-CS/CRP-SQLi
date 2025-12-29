"""
اختبار النموذج على استعلامات صعبة ومخادعة
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
print("اختبار النموذج على استعلامات صعبة ومخادعة")
print("=" * 80)

# Load model and vectorizer
base_dir = Path(__file__).parent.parent
models_dir = base_dir / 'models'

print("\n1. Loading model and vectorizer...")
try:
    model = joblib.load(models_dir / 'svm_model.pkl')
    vectorizer = joblib.load(models_dir / 'tfidf_vectorizer.pkl')
    print("   [OK] Model and vectorizer loaded successfully!")
except Exception as e:
    print(f"   [ERROR] Failed to load: {e}")
    sys.exit(1)

# ============================================
# SQL Injection صعبة (Advanced / Tricky)
# ============================================
print("\n" + "=" * 80)
print("📊 اختبار SQL Injection صعبة (Advanced / Tricky)")
print("=" * 80)

sqli_tricky = [
    # 1. Boolean-based لكن بدون كلمات مشهورة
    ("SELECT * FROM users WHERE id = 10 AND 1=1--", 1, "Boolean-based (AND 1=1)"),
    ("SELECT * FROM users WHERE id = 10 AND 1=2--", 1, "Boolean-based (AND 1=2)"),
    
    # 2. Comment Obfuscation
    ("SELECT * FROM users WHERE username = 'admin'/**/OR/**/'1'='1'", 1, "Comment Obfuscation"),
    
    # 3. Case Manipulation
    ("SeLeCt * FrOm users WhErE username='admin' Or '1'='1'", 1, "Case Manipulation"),
    
    # 4. Inline UNION مخفي
    ("SELECT name FROM products WHERE id = 5 UNION/**/SELECT username FROM users--", 1, "Inline UNION hidden"),
    
    # 5. Time-based Blind SQLi
    ("SELECT * FROM users WHERE id = 1 AND IF(1=1, SLEEP(5), 0)", 1, "Time-based (IF + SLEEP)"),
    ("SELECT * FROM users WHERE id = 1 AND BENCHMARK(5000000,MD5(1))", 1, "Time-based (BENCHMARK)"),
    
    # 6. Encoding / Char-based
    ("SELECT * FROM users WHERE username = CHAR(97,100,109,105,110)", 1, "CHAR() encoding"),
    
    # 7. Nested Query Injection
    ("SELECT * FROM orders WHERE user_id = (SELECT id FROM users WHERE username='admin' LIMIT 1)", 1, "Nested Query Injection"),
    
    # 8. Logical Confusion
    ("SELECT * FROM users WHERE (id=1 OR id=2) AND id=1", 0, "Logical Confusion (Normal!)"),
    
    # 9. Whitespace Tricks
    ("SELECT*FROM users WHERE username='admin'OR'1'='1'", 1, "Whitespace Tricks"),
    
    # 10. Super Sneaky
    ("SELECT * FROM users WHERE username='admin' OR 'x'='x' /*' AND password=''*/", 1, "Super Sneaky"),
]

print("\n   Testing SQL Injection queries:")
sqli_correct = 0
for query, expected, description in sqli_tricky:
    query_vec = vectorizer.transform([query])
    prediction = model.predict(query_vec)[0]
    proba = model.predict_proba(query_vec)[0]
    is_correct = (prediction == expected)
    if is_correct:
        sqli_correct += 1
    
    status = "✅" if is_correct else "❌"
    label = "SQL Injection" if prediction == 1 else "Normal Query"
    confidence = proba[prediction] * 100
    
    print(f"\n   {status} {description}")
    print(f"      Query: {query[:70]}...")
    print(f"      Prediction: {label} ({confidence:.2f}%)")
    print(f"      Expected: {'SQL Injection' if expected == 1 else 'Normal Query'}")

print(f"\n   [RESULTS] SQL Injection: {sqli_correct}/{len(sqli_tricky)} correct ({sqli_correct/len(sqli_tricky)*100:.1f}%)")

# ============================================
# Queries عادية لكنها تشبه الهجوم (False Positive Killers)
# ============================================
print("\n" + "=" * 80)
print("📊 اختبار Queries عادية لكنها تشبه الهجوم (False Positive Killers)")
print("=" * 80)

normal_tricky = [
    # 1. OR لكن طبيعي
    ("SELECT * FROM products WHERE category='phones' OR category='laptops'", 0, "Legitimate OR"),
    
    # 2. Subquery نظيف
    ("SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE active = 1)", 0, "Clean Subquery"),
    
    # 3. UNION مشروع
    ("SELECT name FROM local_customers UNION SELECT name FROM international_customers", 0, "Legitimate UNION"),
    
    # 4. Functions طبيعية
    ("SELECT COUNT(*) FROM users WHERE created_at > NOW() - INTERVAL 7 DAY", 0, "Normal Functions"),
    
    # 5. شرط معقد بس آمن
    ("SELECT * FROM employees WHERE (salary > 500 AND department = 'IT') OR role = 'Manager'", 0, "Complex but Safe"),
    
    # 6. Case + Formatting
    ("SeLeCt id, name FrOm students WhErE grade >= 90", 0, "Case + Formatting"),
    
    # 7. View Creation
    ("CREATE OR REPLACE VIEW active_users AS SELECT id, username FROM users WHERE status = 'active'", 0, "View Creation"),
    
    # 8. Parameter-like Query
    ("SELECT * FROM users WHERE email = ?", 0, "Parameter-like Query"),
]

print("\n   Testing Normal queries (False Positive Killers):")
normal_correct = 0
for query, expected, description in normal_tricky:
    query_vec = vectorizer.transform([query])
    prediction = model.predict(query_vec)[0]
    proba = model.predict_proba(query_vec)[0]
    is_correct = (prediction == expected)
    if is_correct:
        normal_correct += 1
    
    status = "✅" if is_correct else "❌"
    label = "SQL Injection" if prediction == 1 else "Normal Query"
    confidence = proba[prediction] * 100
    
    print(f"\n   {status} {description}")
    print(f"      Query: {query[:70]}...")
    print(f"      Prediction: {label} ({confidence:.2f}%)")
    print(f"      Expected: Normal Query")

print(f"\n   [RESULTS] Normal Queries: {normal_correct}/{len(normal_tricky)} correct ({normal_correct/len(normal_tricky)*100:.1f}%)")

# ============================================
# Summary
# ============================================
print("\n" + "=" * 80)
print("📊 ملخص النتائج")
print("=" * 80)

total_correct = sqli_correct + normal_correct
total_queries = len(sqli_tricky) + len(normal_tricky)
overall_accuracy = (total_correct / total_queries) * 100

print(f"\n   SQL Injection Detection: {sqli_correct}/{len(sqli_tricky)} ({sqli_correct/len(sqli_tricky)*100:.1f}%)")
print(f"   False Positive Prevention: {normal_correct}/{len(normal_tricky)} ({normal_correct/len(normal_tricky)*100:.1f}%)")
print(f"   Overall Accuracy: {total_correct}/{total_queries} ({overall_accuracy:.1f}%)")

# Identify problematic queries
print("\n   ⚠️  استعلامات تحتاج تحسين:")
for query, expected, description in sqli_tricky + normal_tricky:
    query_vec = vectorizer.transform([query])
    prediction = model.predict(query_vec)[0]
    if prediction != expected:
        print(f"      - {description}: Expected {'SQL Injection' if expected == 1 else 'Normal'}, Got {'SQL Injection' if prediction == 1 else 'Normal'}")

print("\n" + "=" * 80)

