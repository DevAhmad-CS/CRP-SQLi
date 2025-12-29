"""
Retrain Model with Additional SQL Injection Examples
Adds missing patterns (OR 1=1 in SELECT, UNION SELECT variations) and retrains
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
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
import joblib
from datetime import datetime

print("=" * 80)
print("Retraining Model with Additional SQL Injection Examples")
print("=" * 80)

# Get script directory and project root
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up from scripts/ to project root

models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
vectorization_dir = os.path.join(results_dir, 'vectorization')
training_dir = os.path.join(results_dir, 'training')

for directory in [models_dir, results_dir, vectorization_dir, training_dir]:
    os.makedirs(directory, exist_ok=True)

# ============================================
# 1. Load Existing Data
# ============================================
print("\n1. Loading existing data...")
train_df = pd.read_csv(os.path.join(base_dir, 'dataset', 'final', 'train_final.csv'))
val_df = pd.read_csv(os.path.join(base_dir, 'dataset', 'final', 'validation_final.csv'))
test_df = pd.read_csv(os.path.join(base_dir, 'dataset', 'final', 'test_final.csv'))

print(f"   [OK] Train: {len(train_df):,} samples")
print(f"   [OK] Validation: {len(val_df):,} samples")
print(f"   [OK] Test: {len(test_df):,} samples")

# ============================================
# 2. Add New SQL Injection Examples + Normal Examples
# ============================================
print("\n2. Adding new SQL Injection examples AND normal examples...")

# New SQL Injection examples - COMPREHENSIVE LIST
new_sqli_examples = [
    # ============================================
    # OR 1=1 in SELECT context
    # ============================================
    "SELECT * FROM users WHERE id = 1 OR 1=1",
    "SELECT * FROM users WHERE id = 1 OR 2=2",
    "SELECT * FROM users WHERE id = 1 OR 3=3",
    "SELECT * FROM users WHERE name = 'admin' OR 1=1",
    "SELECT * FROM users WHERE id = 1 OR 1=1--",
    "SELECT * FROM users WHERE id = 1 OR 1=1#",
    "SELECT * FROM users WHERE id = 1 OR 1=1/*",
    "SELECT * FROM products WHERE id = 1 OR 1=1",
    "SELECT * FROM orders WHERE user_id = 1 OR 1=1",
    "SELECT * FROM users WHERE id = 1 OR 1=1 OR '1'='1'",
    "SELECT * FROM users WHERE id = 1 OR 1=1 AND 1=1",
    "SELECT * FROM users WHERE id = 1 OR true",
    "SELECT * FROM users WHERE id = 1 OR 1=1 UNION SELECT NULL",
    "SELECT * FROM users WHERE id = 1 OR 1=1; DROP TABLE users--",
    
    # ============================================
    # UNION SELECT variations (WITH SELECT prefix)
    # ============================================
    "SELECT * FROM users WHERE id = 1 UNION SELECT NULL--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT version()--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT database()--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT user()--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT NULL,NULL--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT NULL,NULL,NULL--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT table_name FROM information_schema.tables--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT column_name FROM information_schema.columns--",
    "SELECT * FROM users WHERE id = 1 UNION ALL SELECT NULL--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT 1,2,3--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT @@version--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT @@database--",
    
    # ============================================
    # UNION SELECT variations (WITHOUT SELECT prefix) - CRITICAL!
    # ============================================
    "1' UNION SELECT NULL--",
    "1' UNION SELECT version()--",
    "1' UNION SELECT database()--",
    "1' UNION SELECT user()--",
    "1' UNION SELECT NULL,NULL--",
    "1' UNION SELECT NULL,NULL,NULL--",
    "1' UNION SELECT table_name FROM information_schema.tables--",
    "1' UNION SELECT column_name FROM information_schema.columns--",
    "1' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'--",
    "1' UNION ALL SELECT NULL--",
    "1' UNION SELECT 1,2,3--",
    "1' UNION SELECT @@version--",
    "1' UNION SELECT @@database--",
    "1' UNION SELECT version(),database(),user()--",
    "1' UNION SELECT table_name,column_name FROM information_schema.columns--",
    "1' UNION SELECT schema_name FROM information_schema.schemata--",
    "1' UNION SELECT table_schema,table_name FROM information_schema.tables--",
    
    # More variations starting with quote
    "' UNION SELECT NULL--",
    "' UNION SELECT version()--",
    "' UNION SELECT database()--",
    "' UNION SELECT table_name FROM information_schema.tables--",
    "' UNION SELECT column_name FROM information_schema.columns--",
    
    # Variations with different numbers
    "2' UNION SELECT NULL--",
    "3' UNION SELECT version()--",
    "10' UNION SELECT table_name FROM information_schema.tables--",
    
    # ============================================
    # OR-based variations
    # ============================================
    "SELECT * FROM users WHERE id = 1 OR '1'='1'",
    "SELECT * FROM users WHERE id = 1 OR \"1\"=\"1\"",
    "SELECT * FROM users WHERE id = 1 OR 'a'='a'",
    "SELECT * FROM users WHERE id = 1 OR 1=1 OR 1=1",
    "SELECT * FROM users WHERE id = 1 OR 1=1 OR 2=2",
    "SELECT * FROM users WHERE id = 1 OR 1=1 OR 'x'='x'",
    "admin' OR '1'='1",
    "admin' OR '1'='1'--",
    "admin' OR '1'='1'#",
    "admin' OR '1'='1'/*",
    "' OR '1'='1",
    "' OR '1'='1'--",
    "' OR '1'='1'#",
    "1' OR '1'='1",
    "1' OR '1'='1'--",
    "1' OR '1'='1'#",
    
    # ============================================
    # Combined patterns
    # ============================================
    "SELECT * FROM users WHERE id = 1 OR 1=1 UNION SELECT NULL--",
    "SELECT * FROM users WHERE id = 1 OR 1=1 AND SLEEP(5)--",
    "SELECT * FROM users WHERE id = 1 OR 1=1 AND (SELECT * FROM information_schema.tables)--",
    "1' OR 1=1 UNION SELECT NULL--",
    "1' OR '1'='1' UNION SELECT version()--",
    
    # ============================================
    # Time-based injections
    # ============================================
    "SELECT * FROM users WHERE id = 1 AND SLEEP(5)--",
    "SELECT * FROM users WHERE id = 1 AND pg_sleep(5)--",
    "SELECT * FROM users WHERE id = 1 AND WAITFOR DELAY '00:00:05'--",
    "1' AND SLEEP(5)--",
    "1' AND pg_sleep(5)--",
    "1' AND WAITFOR DELAY '00:00:05'--",
    "' AND SLEEP(5)--",
    "' AND pg_sleep(5)--",
    "admin' AND SLEEP(5)--",
    
    # ============================================
    # Boolean-based injections
    # ============================================
    "SELECT * FROM users WHERE id = 1 AND 1=1--",
    "SELECT * FROM users WHERE id = 1 AND 1=2--",
    "SELECT * FROM users WHERE id = 1 AND '1'='1'--",
    "SELECT * FROM users WHERE id = 1 AND '1'='2'--",
    "1' AND 1=1--",
    "1' AND 1=2--",
    "1' AND '1'='1'--",
    "1' AND '1'='2'--",
    "' AND 1=1--",
    "' AND 1=2--",
    
    # ============================================
    # Information schema queries
    # ============================================
    "SELECT * FROM users WHERE id = 1 UNION SELECT table_name FROM information_schema.tables--",
    "SELECT * FROM users WHERE id = 1 UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'--",
    "1' UNION SELECT table_name FROM information_schema.tables--",
    "1' UNION SELECT column_name FROM information_schema.columns WHERE table_name='users'--",
    "1' UNION SELECT * FROM information_schema.tables--",
    "' UNION SELECT table_name FROM information_schema.tables--",
    
    # ============================================
    # Stacked queries
    # ============================================
    "SELECT * FROM users WHERE id = 1; DROP TABLE users--",
    "SELECT * FROM users WHERE id = 1; DELETE FROM users--",
    "SELECT * FROM users WHERE id = 1; UPDATE users SET password='hacked'--",
    "1'; DROP TABLE users--",
    "1'; DELETE FROM users--",
    "1'; UPDATE users SET password='hacked'--",
    "'; DROP TABLE users--",
    "'; DELETE FROM users--",
    
    # ============================================
    # Comment-based injections
    # ============================================
    "admin'--",
    "admin'#",
    "admin'/*",
    "1'--",
    "1'#",
    "'--",
    "'#",
    "SELECT * FROM users WHERE id = 1'--",
    "SELECT * FROM users WHERE id = 1'#",
    
    # ============================================
    # More variations
    # ============================================
    "SELECT * FROM users WHERE id = 1 OR 1=1 LIMIT 1",
    "SELECT * FROM users WHERE id = 1 OR 1=1 ORDER BY 1--",
    "SELECT * FROM users WHERE id = 1 OR 1=1 GROUP BY 1--",
    "1' OR 1=1 LIMIT 1",
    "1' OR 1=1 ORDER BY 1--",
    "1' OR 1=1 GROUP BY 1--",
    
    # ============================================
    # Error-based injections
    # ============================================
    "1' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
    "1' AND EXTRACTVALUE(1, CONCAT(0x7e, (SELECT version()), 0x7e))--",
    "1' AND (SELECT 1 FROM (SELECT COUNT(*),CONCAT(database(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
    
    # ============================================
    # Second-order injections
    # ============================================
    "admin' OR '1'='1",
    "admin' OR '1'='1' OR '1'='1",
    "1' OR EXISTS(SELECT * FROM information_schema.tables)--",
    "1' OR (SELECT COUNT(*) FROM information_schema.tables)>0--",
]

print(f"   Adding {len(new_sqli_examples)} new SQL Injection examples")

# Add NORMAL examples - COMPREHENSIVE LIST
# This helps the model distinguish between normal and malicious queries
new_normal_examples = [
    # ============================================
    # Normal SELECT queries (similar structure but without OR 1=1)
    # ============================================
    "SELECT * FROM users WHERE id = 1",
    "SELECT * FROM users WHERE id = 2",
    "SELECT * FROM users WHERE id = 3",
    "SELECT * FROM users WHERE id = 10",
    "SELECT * FROM users WHERE id = 100",
    "SELECT * FROM users WHERE name = 'admin'",
    "SELECT * FROM users WHERE name = 'user'",
    "SELECT * FROM users WHERE id = 1 AND status = 'active'",
    "SELECT * FROM products WHERE id = 1",
    "SELECT * FROM orders WHERE user_id = 1",
    "SELECT * FROM users WHERE id = 1 AND deleted = 0",
    "SELECT * FROM users WHERE id = 1 LIMIT 1",
    "SELECT * FROM users WHERE id = 1 ORDER BY name",
    "SELECT * FROM users WHERE id = 1 GROUP BY status",
    
    # ============================================
    # Normal SELECT with different conditions
    # ============================================
    "SELECT * FROM users WHERE status = 'active'",
    "SELECT * FROM users WHERE email = 'user@example.com'",
    "SELECT * FROM users WHERE created_at > '2024-01-01'",
    "SELECT * FROM users WHERE id = 1 AND role = 'admin'",
    "SELECT * FROM users WHERE id = 1 AND verified = 1",
    "SELECT * FROM users WHERE id = 1 AND active = 1",
    "SELECT * FROM users WHERE id = 1 AND deleted = 0",
    "SELECT * FROM users WHERE id = 1 AND status = 'active'",
    "SELECT * FROM users WHERE id = 1 AND role = 'user'",
    "SELECT * FROM users WHERE id = 1 AND password = 'hashed_password'",
    "SELECT * FROM users WHERE id = 1 AND email_verified = 1",
    "SELECT * FROM users WHERE id = 1 AND last_login > '2024-01-01'",
    
    # ============================================
    # Normal SELECT with JOIN
    # ============================================
    "SELECT * FROM users WHERE id = 1 JOIN posts ON users.id = posts.user_id",
    "SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id WHERE u.id = 1",
    "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id WHERE u.id = 1",
    "SELECT * FROM users u INNER JOIN posts p ON u.id = p.user_id",
    "SELECT * FROM users u LEFT JOIN posts p ON u.id = p.user_id",
    
    # ============================================
    # Normal SELECT with specific columns
    # ============================================
    "SELECT email FROM users WHERE status = 'active'",
    "SELECT name, email FROM users WHERE id = 1",
    "SELECT id, name, email FROM users WHERE id = 1",
    "SELECT id, name FROM users WHERE id = 1",
    "SELECT * FROM users WHERE id = 1",
    "SELECT name FROM users WHERE id = 1",
    "SELECT email FROM users WHERE id = 1",
    
    # ============================================
    # Normal queries with functions (but not in UNION context)
    # ============================================
    "SELECT version()",
    "SELECT database()",
    "SELECT user()",
    "SELECT NOW()",
    "SELECT COUNT(*) FROM users",
    "SELECT MAX(id) FROM users",
    "SELECT MIN(id) FROM users",
    "SELECT AVG(price) FROM products",
    
    # ============================================
    # Normal information_schema queries (legitimate use)
    # ============================================
    "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'",
    "SELECT column_name FROM information_schema.columns WHERE table_name = 'users'",
    "SELECT * FROM information_schema.tables WHERE table_schema = 'public'",
    "SELECT table_name, table_type FROM information_schema.tables",
    "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'users'",
    
    # ============================================
    # Normal queries with WHERE conditions
    # ============================================
    "SELECT * FROM users WHERE id = 1 AND active = 1",
    "SELECT * FROM users WHERE id = 1 AND deleted = 0",
    "SELECT * FROM users WHERE id = 1 AND status = 'active'",
    "SELECT * FROM users WHERE id = 1 AND role = 'user'",
    "SELECT * FROM users WHERE id = 1 AND verified = 1",
    "SELECT * FROM users WHERE id = 1 AND email_verified = 1",
    
    # ============================================
    # Normal queries with ORDER BY, LIMIT, etc.
    # ============================================
    "SELECT * FROM users WHERE id = 1 ORDER BY name LIMIT 10",
    "SELECT * FROM users WHERE id = 1 GROUP BY status ORDER BY count(*)",
    "SELECT * FROM users ORDER BY id LIMIT 10",
    "SELECT * FROM users ORDER BY name DESC LIMIT 20",
    "SELECT * FROM users GROUP BY status",
    
    # ============================================
    # Normal INSERT, UPDATE, DELETE queries
    # ============================================
    "INSERT INTO users (name, email) VALUES ('John', 'john@example.com')",
    "UPDATE users SET status = 'active' WHERE id = 1",
    "DELETE FROM users WHERE id = 1",
    "UPDATE users SET email = 'new@example.com' WHERE id = 1",
    
    # ============================================
    # Normal queries with subqueries (legitimate)
    # ============================================
    "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders)",
    "SELECT * FROM users WHERE id = (SELECT MAX(id) FROM users)",
    "SELECT * FROM users WHERE EXISTS (SELECT 1 FROM orders WHERE orders.user_id = users.id)",
    
    # ============================================
    # Normal queries with LIKE, IN, BETWEEN
    # ============================================
    "SELECT * FROM users WHERE name LIKE 'admin%'",
    "SELECT * FROM users WHERE id IN (1, 2, 3)",
    "SELECT * FROM users WHERE id BETWEEN 1 AND 100",
    "SELECT * FROM users WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31'",
    
    # ============================================
    # More normal variations
    # ============================================
    "SELECT COUNT(*) FROM users",
    "SELECT COUNT(*) FROM users WHERE status = 'active'",
    "SELECT * FROM users WHERE id > 1",
    "SELECT * FROM users WHERE id < 100",
    "SELECT * FROM users WHERE id >= 1",
    "SELECT * FROM users WHERE id <= 100",
    "SELECT * FROM users WHERE name = 'John'",
    "SELECT * FROM users WHERE email = 'user@example.com'",
]

print(f"   Adding {len(new_normal_examples)} new Normal examples")

# Create DataFrames for both types
new_sqli_df = pd.DataFrame({
    'Query': new_sqli_examples,
    'Label': [1] * len(new_sqli_examples)  # All are SQL Injection
})

new_normal_df = pd.DataFrame({
    'Query': new_normal_examples,
    'Label': [0] * len(new_normal_examples)  # All are Normal
})

# Combine all new examples
new_df = pd.concat([new_sqli_df, new_normal_df], ignore_index=True)

print(f"   [OK] Total new examples: {len(new_df):,} ({len(new_sqli_examples)} SQLi + {len(new_normal_examples)} Normal)")

# Combine with existing training data
train_df_enhanced = pd.concat([train_df, new_df], ignore_index=True)

# Remove duplicates
train_df_enhanced = train_df_enhanced.drop_duplicates(subset=['Query'], keep='first')

print(f"   [OK] After adding: {len(train_df_enhanced):,} samples")
print(f"   [OK] Added: {len(train_df_enhanced) - len(train_df):,} new examples")

# Check balance
label_counts = train_df_enhanced['Label'].value_counts()
print(f"\n   Balance:")
for label, count in label_counts.items():
    percentage = (count / len(train_df_enhanced)) * 100
    label_name = "SQL Injection" if label == 1 else "Normal Query"
    print(f"      - {label_name}: {count:,} ({percentage:.2f}%)")

# ============================================
# 3. Vectorization
# ============================================
print("\n3. Vectorizing data...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),
    min_df=2,
    max_df=1.0,
    lowercase=False,
    sublinear_tf=True
)

print("   Fitting vectorizer on training data...")
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
# 4. Train SVM Model
# ============================================
print("\n4. Training SVM model...")
print("   Settings:")
print("      - kernel: rbf")
print("      - C: 1.0")
print("      - gamma: scale")
print("      - probability: True")

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
# 5. Evaluate on Validation Set
# ============================================
print("\n5. Evaluating on Validation Set...")
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
val_results_path = os.path.join(training_dir, 'svm_validation_results_retrained.txt')
with open(val_results_path, 'w', encoding='utf-8') as f:
    f.write("SVM Model - Validation Results (Retrained)\n")
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
# 6. Test Specific Examples
# ============================================
print("\n6. Testing specific problematic examples...")

test_queries = [
    # SQL Injection (should be detected)
    ("SELECT * FROM users WHERE id = 1 OR 1=1", 1),
    ("SELECT * FROM users WHERE id = 1 OR 2=2", 1),
    ("1' UNION SELECT NULL--", 1),
    ("1' UNION SELECT version()--", 1),  # CRITICAL TEST
    ("1' UNION SELECT table_name FROM information_schema.tables--", 1),  # CRITICAL TEST
    ("admin' OR '1'='1", 1),
    ("SELECT * FROM users WHERE id = 1 UNION SELECT version()--", 1),
    ("' UNION SELECT version()--", 1),
    ("1' AND SLEEP(5)--", 1),
    ("admin'--", 1),
    
    # Normal queries (should NOT be detected as SQL Injection)
    ("SELECT * FROM users WHERE id = 1", 0),
    ("SELECT email FROM users WHERE status = 'active'", 0),
    ("SELECT * FROM users WHERE id = 1 AND status = 'active'", 0),
    ("SELECT u.name, p.title FROM users u JOIN posts p ON u.id = p.user_id", 0),
    ("SELECT version()", 0),
    ("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'", 0),
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
    
    print(f"   {status} '{query[:50]}...'")
    print(f"      -> {label} ({confidence:.2f}% confidence)")
    print(f"      -> Expected: {'SQL Injection' if expected_label == 1 else 'Normal Query'}")

print(f"\n   [OK] Correct: {correct}/{len(test_queries)} ({correct/len(test_queries)*100:.1f}%)")

# ============================================
# 7. Train Logistic Regression (for comparison)
# ============================================
print("\n7. Training Logistic Regression model...")

lr_model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    random_state=42
)

print("   Training...")
start_time = datetime.now()
lr_model.fit(X_train, y_train)
training_time_lr = (datetime.now() - start_time).total_seconds()
print(f"   [OK] Training completed! (Time: {training_time_lr:.2f} seconds)")

# Save model
lr_path = os.path.join(models_dir, 'lr_model.pkl')
joblib.dump(lr_model, lr_path)
print(f"   [SAVED] Model: {lr_path}")

# Evaluate LR
y_val_pred_lr = lr_model.predict(X_val)
lr_accuracy = accuracy_score(y_val, y_val_pred_lr)
lr_f1 = f1_score(y_val, y_val_pred_lr)

print(f"\n   LR Results:")
print(f"      - Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"      - F1-Score: {lr_f1:.4f} ({lr_f1*100:.2f}%)")

# ============================================
# 8. Summary
# ============================================
print("\n" + "=" * 80)
print("[SUCCESS] Retraining completed successfully!")
print("=" * 80)

print(f"\nSummary:")
print(f"   - Training samples: {len(train_df_enhanced):,}")
print(f"   - New examples added: {len(train_df_enhanced) - len(train_df):,}")
print(f"   - SVM Validation Accuracy: {val_accuracy*100:.2f}%")
print(f"   - SVM Validation F1-Score: {val_f1*100:.2f}%")
print(f"   - Test queries correct: {correct}/{len(test_queries)}")

print(f"\nFiles saved:")
print(f"   - {svm_path}")
print(f"   - {lr_path}")
print(f"   - {vectorizer_path}")
print(f"   - {val_results_path}")

print("\n" + "=" * 80)

