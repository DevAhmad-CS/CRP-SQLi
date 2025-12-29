"""
إضافة الاستعلامات الجديدة من المستخدم مع فلترة المكررات
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

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
import joblib
from datetime import datetime

print("=" * 80)
print("إضافة الاستعلامات الجديدة من المستخدم")
print("=" * 80)

# Get script directory and project root
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)

models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
vectorization_dir = os.path.join(results_dir, 'vectorization')
training_dir = os.path.join(results_dir, 'training')
evaluation_dir = os.path.join(results_dir, 'evaluation')
dataset_dir = os.path.join(base_dir, 'dataset', 'final')

for directory in [models_dir, results_dir, vectorization_dir, training_dir, evaluation_dir]:
    os.makedirs(directory, exist_ok=True)

# ============================================
# 1. Load Existing Data
# ============================================
print("\n1. Loading existing data...")
train_df = pd.read_csv(os.path.join(dataset_dir, 'train_final.csv'))
val_df = pd.read_csv(os.path.join(dataset_dir, 'validation_final.csv'))
test_df = pd.read_csv(os.path.join(dataset_dir, 'test_final.csv'))

print(f"   [OK] Train: {len(train_df):,} samples")
print(f"   [OK] Validation: {len(val_df):,} samples")
print(f"   [OK] Test: {len(test_df):,} samples")

# ============================================
# 2. Load New Queries from User
# ============================================
print("\n2. Loading new queries from user...")

# Normal queries (150)
new_normal_queries = [
    "SELECT * FROM users WHERE id = 1",
    "SELECT * FROM users WHERE id = 2",
    "SELECT * FROM users WHERE id = 3",
    "SELECT * FROM users WHERE id = 10",
    "SELECT * FROM users WHERE id = 100",
    "SELECT name FROM products WHERE price > 50",
    "SELECT name,price FROM products WHERE category='phones'",
    "SELECT * FROM orders WHERE user_id = 10",
    "SELECT * FROM orders WHERE status='shipped'",
    "SELECT COUNT(*) FROM users",
    "SELECT COUNT(*) FROM users WHERE active=1",
    "SELECT * FROM employees WHERE department='IT'",
    "SELECT * FROM employees WHERE salary > 700",
    "SELECT * FROM students WHERE grade >= 90",
    "SELECT * FROM students WHERE grade BETWEEN 70 AND 90",
    "SELECT id,username FROM users WHERE status='active'",
    "SELECT id,email FROM users WHERE verified=1",
    "SELECT * FROM logs WHERE created_at > NOW() - INTERVAL 1 DAY",
    "SELECT * FROM logs WHERE level='error'",
    "SELECT * FROM payments WHERE status IN ('paid','pending')",
    "SELECT * FROM payments WHERE amount > 100",
    "SELECT * FROM products WHERE category='phones' OR category='laptops'",
    "SELECT * FROM products WHERE stock > 0 AND active=1",
    "SELECT SUM(total) FROM sales WHERE year=2024",
    "SELECT AVG(price) FROM products",
    "SELECT * FROM users WHERE email = ?",
    "SELECT * FROM users WHERE username = ?",
    "SELECT * FROM sessions WHERE expires_at > NOW()",
    "SELECT * FROM sessions WHERE user_id=5",
    "SELECT * FROM reviews WHERE rating >= 4",
    "SELECT * FROM reviews WHERE product_id=3",
    "SELECT * FROM users ORDER BY created_at DESC LIMIT 5",
    "SELECT * FROM users ORDER BY username ASC",
    "SELECT department,COUNT(*) FROM employees GROUP BY department",
    "SELECT role,COUNT(*) FROM users GROUP BY role",
    "SELECT * FROM users WHERE username LIKE 'a%'",
    "SELECT * FROM users WHERE email LIKE '%@gmail.com'",
    "SELECT * FROM products WHERE price BETWEEN 10 AND 100",
    "SELECT * FROM orders WHERE total BETWEEN 50 AND 200",
    "SELECT * FROM users WHERE role='admin' AND enabled=1",
    "SELECT * FROM users WHERE enabled=0",
    "SELECT * FROM orders WHERE created_at >= '2024-01-01'",
    "SELECT * FROM orders WHERE created_at <= '2024-12-31'",
    "SELECT * FROM users WHERE id IN (1,2,3)",
    "SELECT * FROM products WHERE id IN (5,6,7)",
    "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE active=1)",
    "SELECT * FROM employees WHERE department IN ('IT','HR')",
    "SELECT * FROM users WHERE last_login IS NOT NULL",
    "SELECT * FROM users WHERE phone IS NULL",
    "SELECT DISTINCT category FROM products",
    "SELECT DISTINCT country FROM users",
    "SELECT * FROM users LIMIT 10 OFFSET 20",
    "SELECT * FROM products LIMIT 5",
    "SELECT MAX(price) FROM products",
    "SELECT MIN(salary) FROM employees",
    "SELECT * FROM users WHERE id = 1 OR id = 2",
    "SELECT * FROM users WHERE (id=1 OR id=2) AND active=1",
    "SELECT * FROM products WHERE (price > 50 AND stock > 0)",
    "SELECT * FROM orders WHERE status='paid' OR status='pending'",
    "SELECT * FROM users WHERE LENGTH(username) > 5",
    "SELECT * FROM users WHERE CHAR_LENGTH(email) > 10",
    
    # Additional normal queries that look tricky
    "SELECT * FROM users WHERE (id=1 OR id=2) AND id=1",
    "SELECT * FROM users WHERE (id=1 OR id=2) AND active=1",
    "SELECT * FROM products WHERE (price > 50 OR stock > 0) AND active=1",
    "SELECT * FROM orders WHERE (user_id=1 OR user_id=2) AND status='paid'",
    "SELECT * FROM users WHERE id = 10 AND status = 'active'",
    "SELECT * FROM users WHERE id = 5 AND role = 'admin'",
    "SELECT * FROM orders WHERE user_id = (SELECT id FROM users WHERE active = 1 LIMIT 1)",
    "SELECT * FROM products WHERE category_id = (SELECT id FROM categories WHERE name = 'electronics')",
]

# SQL Injection queries (150)
new_sqli_queries = [
    "SELECT * FROM users WHERE id = 1 OR 1=1--",
    "SELECT * FROM users WHERE username='admin' OR '1'='1'",
    "SELECT * FROM users WHERE id = 5 UNION SELECT username,password FROM users--",
    "SELECT * FROM users WHERE id=1 AND SLEEP(5)",
    "SELECT * FROM users WHERE username='admin'/**/OR/**/'x'='x'",
    "SELECT * FROM users WHERE id=1 AND BENCHMARK(5000000,MD5(1))",
    "SELECT * FROM users WHERE username=CHAR(97,100,109,105,110)",
    "SELECT * FROM users WHERE id=1 OR CHAR(49)=CHAR(49)",
    "SELECT * FROM users WHERE username=CHAR(97) OR CHAR(49)=CHAR(49)",
    "SELECT * FROM users WHERE id=CHAR(49)",
    "SELECT * FROM users WHERE username=CHAR(97,100,109,105,110) OR 1=1",
    "SELECT * FROM users WHERE id=1 AND CHAR(49)=CHAR(49)",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT * FROM users)",
    "SELECT * FROM users WHERE id=1; DROP TABLE users--",
    "SELECT * FROM users WHERE username='admin' OR ''=''",
    "SELECT * FROM users WHERE id=(SELECT id FROM users LIMIT 1) OR 1=1",
    "SELECT * FROM users WHERE id=1 OR TRUE",
    "SELECT * FROM users WHERE username='admin' OR 1 LIKE 1",
    "SELECT * FROM users WHERE id=1 AND (SELECT COUNT(*) FROM users)>0",
    "SELECT * FROM users WHERE id=1 OR 9999=9999",
    "SELECT * FROM users WHERE username='admin' OR 'a'='a'#",
    "SELECT * FROM users WHERE id=1 UNION SELECT NULL,NULL--",
    "SELECT * FROM users WHERE id=1 AND IF(1=1,SLEEP(3),0)",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT 1)",
    "SELECT * FROM users WHERE username='admin' OR 1=1/*comment*/",
    "SELECT * FROM products WHERE id=10 OR 1=1",
    "SELECT * FROM orders WHERE user_id=5 OR 'x'='x'",
    "SELECT * FROM users WHERE email='test@test.com' OR '1'='1'",
    "SELECT * FROM users WHERE id=1 AND 1=1--",
    "SELECT * FROM users WHERE id=1 AND 1=2 OR 1=1",
    "SELECT * FROM users WHERE username='admin' OR username LIKE '%'",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT username FROM users)",
    "SELECT * FROM users WHERE id=1 AND SLEEP(2)",
    "SELECT * FROM users WHERE id=1 AND IF(2>1,SLEEP(4),0)",
    "SELECT * FROM users WHERE id=1 OR (SELECT 1)",
    "SELECT * FROM users WHERE id=1 UNION SELECT username,email FROM users--",
    "SELECT * FROM users WHERE id=1 UNION ALL SELECT NULL,NULL--",
    "SELECT * FROM users WHERE id=1 AND (SELECT LENGTH(password) FROM users LIMIT 1)>0",
    "SELECT * FROM users WHERE id=1 OR id IN (SELECT id FROM users)",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT COUNT(*) FROM users)",
    "SELECT * FROM users WHERE id=1 AND 999=999",
    "SELECT * FROM users WHERE username='admin' OR 2>1",
    "SELECT * FROM users WHERE id=1 OR 'abc'='abc'",
    "SELECT * FROM users WHERE id=1 OR 'a' LIKE 'a'",
    "SELECT * FROM users WHERE id=1 OR 5 BETWEEN 1 AND 10",
    "SELECT * FROM users WHERE id=1 AND (SELECT SLEEP(1))",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT SLEEP(1))",
    
    # Additional tricky patterns from testing
    "SELECT * FROM users WHERE id = 10 AND 1=1--",
    "SELECT * FROM users WHERE id = 10 AND 1=2--",
    "SELECT * FROM users WHERE id = 5 AND 1=1--",
    "SELECT * FROM users WHERE id = 5 AND 1=2--",
    "SELECT * FROM orders WHERE user_id = (SELECT id FROM users WHERE username='admin' LIMIT 1) OR 1=1",
    "SELECT * FROM orders WHERE user_id = (SELECT id FROM users WHERE username='admin') OR 1=1",
    "SELECT * FROM products WHERE id = (SELECT id FROM users WHERE id=1) OR 1=1",
    
    # DROP TABLE variations (critical!)
    "1'; DROP TABLE users--",
    "1' ; DROP TABLE users--",
    "1';DROP TABLE users--",
    "1'; DROP TABLE products--",
    "1'; DROP TABLE orders--",
    "1'; DROP TABLE customers--",
    "1'; DROP TABLE users;--",
    "1'; DROP TABLE users #",
    "1'; DROP TABLE users/*",
    "' ; DROP TABLE users--",
    "'; DROP TABLE users--",
    "admin'; DROP TABLE users--",
    
    # DELETE variations
    "1'; DELETE FROM users--",
    "1' ; DELETE FROM users--",
    "1';DELETE FROM users--",
    "1'; DELETE FROM users WHERE id=1--",
    "'; DELETE FROM users--",
    
    # UPDATE variations
    "1'; UPDATE users SET password='hacked'--",
    "1' ; UPDATE users SET password='hacked'--",
    "1';UPDATE users SET password='hacked'--",
    "'; UPDATE users SET password='hacked'--",
    
    # Short SQL Injection patterns in context (safe approach - no performance impact)
    # Adding short patterns in minimal context to help model learn them
    "id=1 OR 1=1--",
    "id=1 OR 1=1#",
    "id=1 OR 1=1/*",
    "id=1 OR 1=2--",
    "id=1 OR 1=2#",
    "id=1 OR 1=2/*",
    "id=1 OR '1'='1'--",
    "id=1 OR '1'='1'#",
    "id=1 OR '1'='1'/*",
    "id=1 OR '1'='2'--",
    "id=1 OR '1'='2'#",
    "id=1 AND 1=1--",
    "id=1 AND 1=1#",
    "id=1 AND 1=2--",
    "id=1 AND 1=2#",
    "id=1 OR 1=1",
    "id=1 OR 1=2",
    "id=1 AND 1=1",
    "id=1 AND 1=2",
    "id=1 OR '1'='1'",
    "id=1 OR '1'='2'",
    "id=1 AND '1'='1'",
    "id=1 AND '1'='2'",
    # Very short patterns (will help with 1=1-- detection)
    "1=1--",
    "1=1--",
    "1=1#",
    "1=1#",
    "1=1/*",
    "1=1/*",
    "1=2--",
    "1=2--",
    "1=2#",
    "1=2#",
    "'1'='1'--",
    "'1'='1'--",
    "'1'='1'#",
    "'1'='1'#",
    "'1'='2'--",
    "'1'='2'--",
]

# Create DataFrames
new_normal_df = pd.DataFrame({
    'Query': new_normal_queries,
    'Label': [0] * len(new_normal_queries)
})

new_sqli_df = pd.DataFrame({
    'Query': new_sqli_queries,
    'Label': [1] * len(new_sqli_queries)
})

print(f"   [OK] Loaded {len(new_normal_queries)} Normal queries")
print(f"   [OK] Loaded {len(new_sqli_queries)} SQL Injection queries")

# ============================================
# 3. Filter Duplicates
# ============================================
print("\n3. Filtering duplicates...")

# Combine existing training data
all_existing_queries = set(train_df['Query'].str.strip().str.lower())

# Filter new queries
new_normal_filtered = []
new_sqli_filtered = []

for query in new_normal_queries:
    query_lower = query.strip().lower()
    if query_lower not in all_existing_queries:
        new_normal_filtered.append(query)
    else:
        print(f"   [SKIP] Duplicate Normal: {query[:60]}...")

# Short patterns that need to appear multiple times (for min_df=2)
short_patterns_list = ['1=1--', '1=1', '1=1#', '1=1/*', '1=2--', '1=2', '1=2#', "'1'='1'--", "'1'='1'", "'1'='1'#", "'1'='2'--"]

for query in new_sqli_queries:
    query_lower = query.strip().lower()
    query_stripped = query.strip()
    
    # For short patterns, always add (even if duplicate exists) - they need multiple instances
    if query_stripped in short_patterns_list:
        new_sqli_filtered.append(query)
    elif query_lower not in all_existing_queries:
        new_sqli_filtered.append(query)
    else:
        print(f"   [SKIP] Duplicate SQLi: {query[:60]}...")

print(f"\n   [OK] After filtering:")
print(f"      - Normal: {len(new_normal_filtered)} new (removed {len(new_normal_queries) - len(new_normal_filtered)} duplicates)")
print(f"      - SQL Injection: {len(new_sqli_filtered)} new (removed {len(new_sqli_queries) - len(new_sqli_filtered)} duplicates)")

# Create filtered DataFrames
new_normal_df_filtered = pd.DataFrame({
    'Query': new_normal_filtered,
    'Label': [0] * len(new_normal_filtered)
})

new_sqli_df_filtered = pd.DataFrame({
    'Query': new_sqli_filtered,
    'Label': [1] * len(new_sqli_filtered)
})

# ============================================
# 4. Combine with Training Data
# ============================================
print("\n4. Combining with training data...")

train_df_enhanced = pd.concat([train_df, new_normal_df_filtered, new_sqli_df_filtered], ignore_index=True)

# Remove duplicates BUT keep short patterns (they need to appear multiple times for min_df=2)
# Short patterns are critical for detection
short_patterns = ['1=1--', '1=1', '1=1#', '1=1/*', '1=2--', '1=2', '1=2#', "'1'='1'--", "'1'='1'", "'1'='1'#", "'1'='2'--"]

# For short patterns, keep ALL instances (don't remove duplicates)
# For other queries, remove duplicates
mask_short = train_df_enhanced['Query'].isin(short_patterns)
short_queries = train_df_enhanced[mask_short]  # Keep all, including duplicates
other_queries = train_df_enhanced[~mask_short].drop_duplicates(subset=['Query'], keep='first')

# Combine back
train_df_enhanced = pd.concat([short_queries, other_queries], ignore_index=True)

print(f"   [OK] Enhanced training set: {len(train_df_enhanced):,} samples")
print(f"   [OK] Added: {len(train_df_enhanced) - len(train_df):,} new examples")

# Check balance
label_counts = train_df_enhanced['Label'].value_counts()
print(f"\n   Balance:")
for label, count in label_counts.items():
    percentage = (count / len(train_df_enhanced)) * 100
    label_name = "SQL Injection" if label == 1 else "Normal Query"
    print(f"      - {label_name}: {count:,} ({percentage:.2f}%)")

# ============================================
# 5. Vectorization (Same Settings)
# ============================================
print("\n5. Vectorizing data...")
print("   Settings:")
print("      - max_features: 10000")
print("      - ngram_range: (1, 3)")
print("      - min_df: 2")
print("      - max_df: 1.0")
print("      - lowercase: False")
print("      - sublinear_tf: True")

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),
    min_df=2,
    max_df=1.0,
    lowercase=False,
    sublinear_tf=True
)

print("\n   Fitting vectorizer on training data...")
X_train = vectorizer.fit_transform(train_df_enhanced['Query'])
y_train = train_df_enhanced['Label'].values

print("   Transforming validation and test data...")
X_val = vectorizer.transform(val_df['Query'])
y_val = val_df['Label'].values

X_test = vectorizer.transform(test_df['Query'])
y_test = test_df['Label'].values

print(f"   [OK] Feature matrix shape: {X_train.shape}")
print(f"   [OK] Number of features: {X_train.shape[1]:,}")

# Save vectorizer
vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
joblib.dump(vectorizer, vectorizer_path)
print(f"   [SAVED] Vectorizer: {vectorizer_path}")

# ============================================
# 6. Train SVM Model (Same Settings)
# ============================================
print("\n6. Training SVM model...")
print("   Settings:")
print("      - kernel: rbf")
print("      - C: 1.0")
print("      - gamma: scale")
print("      - probability: True")
print("      - random_state: 42")

svm_model = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    random_state=42,
    probability=True
)

print("\n   Training...")
start_time = datetime.now()
svm_model.fit(X_train, y_train)
training_time = (datetime.now() - start_time).total_seconds()
print(f"   [OK] Training completed! (Time: {training_time:.2f} seconds)")

# Save model
svm_path = os.path.join(models_dir, 'svm_model.pkl')
joblib.dump(svm_model, svm_path)
print(f"   [SAVED] Model: {svm_path}")

# ============================================
# 7. Evaluate on Validation Set
# ============================================
print("\n7. Evaluating on Validation Set...")
y_val_pred = svm_model.predict(X_val)

val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred)
val_recall = recall_score(y_val, y_val_pred)
val_f1 = f1_score(y_val, y_val_pred)

print("\n   Results:")
print(f"      - Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
print(f"      - Precision: {val_precision:.4f} ({val_precision*100:.2f}%)")
print(f"      - Recall: {val_recall:.4f} ({val_recall*100:.2f}%)")
print(f"      - F1-Score: {val_f1:.4f} ({val_f1*100:.2f}%)")

# Save validation results
val_results_path = os.path.join(training_dir, 'svm_validation_results_user_queries.txt')
with open(val_results_path, 'w', encoding='utf-8') as f:
    f.write("SVM Model - Validation Results (With User Queries)\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Training Time: {training_time:.2f} seconds\n\n")
    f.write("Metrics:\n")
    f.write(f"  - Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {val_precision:.4f} ({val_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {val_recall:.4f} ({val_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {val_f1:.4f} ({val_f1*100:.2f}%)\n\n")
    f.write("Classification Report:\n")
    f.write(classification_report(y_val, y_val_pred,
                                target_names=['Normal Query', 'SQL Injection']))

print(f"   [SAVED] Validation results: {val_results_path}")

# ============================================
# 8. Test Critical Examples
# ============================================
print("\n8. Testing critical new patterns...")

test_queries = [
    # New patterns from user
    ("SELECT * FROM users WHERE email = ?", 0),  # Parameterized
    ("SELECT * FROM products WHERE category='phones' OR category='laptops'", 0),  # Legitimate OR
    ("SELECT * FROM users WHERE id=1 AND BENCHMARK(5000000,MD5(1))", 1),  # BENCHMARK
    ("SELECT * FROM users WHERE username=CHAR(97,100,109,105,110)", 1),  # CHAR()
    ("SELECT * FROM users WHERE id=1 AND IF(1=1,SLEEP(3),0)", 1),  # IF()
    
    # Existing critical patterns
    ("SELECT * FROM users WHERE id = 1 OR 1=1", 1),
    ("1' UNION SELECT version()--", 1),
    ("SELECT * FROM users WHERE id = 1", 0),
]

print("\n   Testing queries:")
correct = 0
for query, expected_label in test_queries:
    query_vec = vectorizer.transform([query])
    prediction = svm_model.predict(query_vec)[0]
    proba = svm_model.predict_proba(query_vec)[0]
    is_correct = (prediction == expected_label)
    if is_correct:
        correct += 1
    
    status = "[OK]" if is_correct else "[FAIL]"
    label = "SQL Injection" if prediction == 1 else "Normal Query"
    confidence = proba[prediction] * 100
    
    print(f"   {status} '{query[:60]}...'")
    print(f"      -> {label} ({confidence:.2f}% confidence)")
    print(f"      -> Expected: {'SQL Injection' if expected_label == 1 else 'Normal Query'}")

print(f"\n   [OK] Correct: {correct}/{len(test_queries)} ({correct/len(test_queries)*100:.1f}%)")

# ============================================
# 9. Summary
# ============================================
print("\n" + "=" * 80)
print("[SUCCESS] Training completed successfully!")
print("=" * 80)

print(f"\nSummary:")
print(f"   - Original training samples: {len(train_df):,}")
print(f"   - New Normal queries added: {len(new_normal_filtered):,}")
print(f"   - New SQL Injection queries added: {len(new_sqli_filtered):,}")
print(f"   - Total new examples: {len(new_normal_filtered) + len(new_sqli_filtered):,}")
print(f"   - Final training samples: {len(train_df_enhanced):,}")
print(f"   - SVM Validation Accuracy: {val_accuracy*100:.2f}%")
print(f"   - SVM Validation F1-Score: {val_f1*100:.2f}%")
print(f"   - Test queries correct: {correct}/{len(test_queries)}")

print(f"\nNew patterns added:")
print(f"   ✅ Parameterized queries (?)")
print(f"   ✅ BENCHMARK()")
print(f"   ✅ CHAR() encoding")
print(f"   ✅ IF() statements")
print(f"   ✅ Legitimate OR queries")

print(f"\nFiles saved:")
print(f"   - {svm_path}")
print(f"   - {vectorizer_path}")
print(f"   - {val_results_path}")

print("\n" + "=" * 80)

