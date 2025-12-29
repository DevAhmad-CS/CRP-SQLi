"""
Logistic Regression Model Training Script
Train Logistic Regression model using pre-vectorized data
"""

import numpy as np
from scipy.sparse import load_npz
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score, f1_score, precision_score, recall_score
import joblib
import os
import sys
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 80)
print("تدريب نموذج Logistic Regression")
print("=" * 80)

# Create directories
base_dir = '../'
models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
training_dir = os.path.join(results_dir, 'training')

for directory in [models_dir, results_dir, training_dir]:
    os.makedirs(directory, exist_ok=True)

# ============================================
# 1. Load Vectorized Data
# ============================================
print("\n📂 1. تحميل المتجهات المحفوظة...")

vectorization_dir = os.path.join(results_dir, 'vectorization')

X_train = load_npz(os.path.join(vectorization_dir, 'X_train_sparse.npz'))
X_val = load_npz(os.path.join(vectorization_dir, 'X_val_sparse.npz'))
y_train = np.load(os.path.join(vectorization_dir, 'y_train.npy'))
y_val = np.load(os.path.join(vectorization_dir, 'y_val.npy'))

print(f"   ✅ Train: {X_train.shape[0]:,} عينة")
print(f"   ✅ Validation: {X_val.shape[0]:,} عينة")
print(f"   ✅ عدد الميزات: {X_train.shape[1]:,}")

# ============================================
# 2. Train Logistic Regression Model
# ============================================
print("\n🤖 2. تدريب نموذج Logistic Regression...")
print("   ⚙️  الإعدادات:")
print("      - max_iter: 1000")
print("      - C: 1.0")
print("      - penalty: l2")

lr_model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    penalty='l2',
    random_state=42
)

print("\n   🔄 بدء التدريب...")
start_time = datetime.now()
lr_model.fit(X_train, y_train)
training_time = (datetime.now() - start_time).total_seconds()
print(f"   ✅ تم التدريب بنجاح! (الوقت: {training_time:.2f} ثانية)")

# ============================================
# 3. Save Model
# ============================================
print("\n💾 3. حفظ النموذج...")
lr_path = os.path.join(models_dir, 'lr_model.pkl')
joblib.dump(lr_model, lr_path)
print(f"   ✅ تم حفظ النموذج في: {lr_path}")

# ============================================
# 4. Evaluate on Validation Set
# ============================================
print("\n📊 4. التقييم على Validation Set...")
y_val_pred = lr_model.predict(X_val)

val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred)
val_recall = recall_score(y_val, y_val_pred)
val_f1 = f1_score(y_val, y_val_pred)

print("\n   📈 النتائج:")
print(f"      - Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
print(f"      - Precision: {val_precision:.4f} ({val_precision*100:.2f}%)")
print(f"      - Recall: {val_recall:.4f} ({val_recall*100:.2f}%)")
print(f"      - F1-Score: {val_f1:.4f} ({val_f1*100:.2f}%)")

# ============================================
# 5. Save Results
# ============================================
print("\n💾 5. حفظ النتائج...")
val_results_path = os.path.join(training_dir, 'lr_validation_results.txt')
with open(val_results_path, 'w', encoding='utf-8') as f:
    f.write("Logistic Regression Model - Validation Results\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("Model Settings:\n")
    f.write(f"  - max_iter: 1000\n")
    f.write(f"  - C: 1.0\n")
    f.write(f"  - penalty: l2\n\n")
    
    f.write(f"Training Time: {training_time:.2f} seconds\n\n")
    
    f.write("Metrics:\n")
    f.write(f"  - Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {val_precision:.4f} ({val_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {val_recall:.4f} ({val_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {val_f1:.4f} ({val_f1*100:.2f}%)\n\n")
    
    f.write("Classification Report:\n")
    f.write(classification_report(y_val, y_val_pred,
                                target_names=['Normal Query', 'SQL Injection']))

print(f"   ✅ تم حفظ النتائج في: {val_results_path}")

# ============================================
# 6. Summary
# ============================================
print("\n" + "=" * 80)
print("✅ تم تدريب Logistic Regression بنجاح!")
print("=" * 80)

print(f"\n📊 الملخص:")
print(f"   - Training Time: {training_time:.2f} ثانية")
print(f"   - Accuracy: {val_accuracy*100:.2f}%")
print(f"   - F1-Score: {val_f1*100:.2f}%")
print(f"   - النموذج محفوظ في: models/lr_model.pkl")

print("\n" + "=" * 80)
print("🎉 جاهز للخطوة التالية!")
print("=" * 80)
print("\nالخطوة التالية: تشغيل scripts/9_compare_and_test.py")

