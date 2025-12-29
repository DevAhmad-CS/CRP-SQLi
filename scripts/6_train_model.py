"""
SQL Injection Detection Model Training Script
Converts text to vectors and trains SVM/Logistic Regression models
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime

print("=" * 80)
print("تدريب نموذج الكشف عن SQL Injection")
print("=" * 80)

# Create organized directories
base_dir = '../'
models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
vectorization_dir = os.path.join(results_dir, 'vectorization')
training_dir = os.path.join(results_dir, 'training')
evaluation_dir = os.path.join(results_dir, 'evaluation')

for directory in [models_dir, results_dir, vectorization_dir, training_dir, evaluation_dir]:
    os.makedirs(directory, exist_ok=True)

print(f"\n📁 المجلدات المنظمة:")
print(f"   - models/ - لحفظ النماذج")
print(f"   - results/vectorization/ - نتائج التحويل")
print(f"   - results/training/ - نتائج التدريب")
print(f"   - results/evaluation/ - نتائج التقييم")

# ============================================
# 1. Load Data
# ============================================
print("\n📂 1. تحميل البيانات...")
train_df = pd.read_csv('../dataset/final/train_final.csv')
val_df = pd.read_csv('../dataset/final/validation_final.csv')
test_df = pd.read_csv('../dataset/final/test_final.csv')

print(f"   ✅ Train: {len(train_df):,} سجل")
print(f"   ✅ Validation: {len(val_df):,} سجل")
print(f"   ✅ Test: {len(test_df):,} سجل")

# Check balance
print(f"\n   📊 توازن Train Set:")
train_labels = train_df['Label'].value_counts()
for label, count in train_labels.items():
    percentage = (count / len(train_df)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"      - {label_name}: {count:,} ({percentage:.2f}%)")

# Save data info
data_info_path = os.path.join(vectorization_dir, 'dataset_info.txt')
with open(data_info_path, 'w', encoding='utf-8') as f:
    f.write("Dataset Information\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Train Set: {len(train_df):,} samples\n")
    f.write(f"Validation Set: {len(val_df):,} samples\n")
    f.write(f"Test Set: {len(test_df):,} samples\n\n")
    f.write("Train Set Balance:\n")
    for label, count in train_labels.items():
        percentage = (count / len(train_df)) * 100
        label_name = "SQL Injection" if label == 1 else "Normal Query"
        f.write(f"  - {label_name}: {count:,} ({percentage:.2f}%)\n")

print(f"   💾 تم حفظ معلومات Dataset في: {data_info_path}")

# ============================================
# 2. Convert Text to Vectors (TF-IDF with improved settings)
# ============================================
print("\n🔄 2. تحويل النصوص إلى متجهات (TF-IDF)...")
print("   ⚙️  الإعدادات المحسّنة:")
print("      - max_features: 10000")
print("      - ngram_range: (1, 3)")
print("      - min_df: 2")
print("      - max_df: 1.0")
print("      - lowercase: False")

vectorizer = TfidfVectorizer(
    max_features=10000,
    ngram_range=(1, 3),
    min_df=2,
    max_df=1.0,
    stop_words=None,
    lowercase=False,
    sublinear_tf=True
)

# Transform data
print("\n   🔄 تحويل Train Set...")
X_train = vectorizer.fit_transform(train_df['Query'])
y_train = train_df['Label'].values

print("   🔄 تحويل Validation Set...")
X_val = vectorizer.transform(val_df['Query'])
y_val = val_df['Label'].values

print("   🔄 تحويل Test Set...")
X_test = vectorizer.transform(test_df['Query'])
y_test = test_df['Label'].values

print(f"\n   ✅ تم التحويل بنجاح!")
print(f"      - شكل المصفوفة: {X_train.shape}")
print(f"      - عدد الميزات: {X_train.shape[1]:,}")

# Save vectorizer
vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
joblib.dump(vectorizer, vectorizer_path)
print(f"   💾 تم حفظ Vectorizer في: {vectorizer_path}")

# Save vectorization info
vectorization_info_path = os.path.join(vectorization_dir, 'vectorization_info.txt')
with open(vectorization_info_path, 'w', encoding='utf-8') as f:
    f.write("Vectorization Information\n")
    f.write("=" * 50 + "\n\n")
    f.write("Settings:\n")
    f.write(f"  - max_features: 10000\n")
    f.write(f"  - ngram_range: (1, 3)\n")
    f.write(f"  - min_df: 2\n")
    f.write(f"  - max_df: 1.0\n")
    f.write(f"  - lowercase: False\n")
    f.write(f"  - sublinear_tf: True\n\n")
    f.write("Results:\n")
    f.write(f"  - Feature matrix shape: {X_train.shape}\n")
    f.write(f"  - Number of features: {X_train.shape[1]:,}\n")
    f.write(f"  - Sparsity: {(1 - X_train.nnz / (X_train.shape[0] * X_train.shape[1])) * 100:.2f}%\n")

print(f"   💾 تم حفظ معلومات التحويل في: {vectorization_info_path}")

# Save sparse matrices (optional - for later use)
print("\n   💾 حفظ المتجهات...")
X_train_path = os.path.join(vectorization_dir, 'X_train_sparse.npz')
X_val_path = os.path.join(vectorization_dir, 'X_val_sparse.npz')
X_test_path = os.path.join(vectorization_dir, 'X_test_sparse.npz')

from scipy.sparse import save_npz
save_npz(X_train_path, X_train)
save_npz(X_val_path, X_val)
save_npz(X_test_path, X_test)

print(f"      - تم حفظ X_train في: {X_train_path}")
print(f"      - تم حفظ X_val في: {X_val_path}")
print(f"      - تم حفظ X_test في: {X_test_path}")

# ============================================
# 3. Train SVM Model (Primary Model)
# ============================================
print("\n🤖 3. تدريب SVM Model...")
print("   ⚙️  الإعدادات:")
print("      - kernel: rbf")
print("      - C: 1.0")
print("      - gamma: scale")

svm_model = SVC(
    kernel='rbf',
    C=1.0,
    gamma='scale',
    random_state=42,
    probability=True
)

print("\n   🔄 بدء التدريب...")
start_time = datetime.now()
svm_model.fit(X_train, y_train)
training_time = (datetime.now() - start_time).total_seconds()
print(f"   ✅ تم التدريب بنجاح! (الوقت: {training_time:.2f} ثانية)")

# Save model
svm_path = os.path.join(models_dir, 'svm_model.pkl')
joblib.dump(svm_model, svm_path)
print(f"   💾 تم حفظ النموذج في: {svm_path}")

# ============================================
# 4. Evaluate on Validation Set
# ============================================
print("\n📊 4. التقييم على Validation Set...")
y_val_pred = svm_model.predict(X_val)

val_accuracy = accuracy_score(y_val, y_val_pred)
val_precision = precision_score(y_val, y_val_pred)
val_recall = recall_score(y_val, y_val_pred)
val_f1 = f1_score(y_val, y_val_pred)

print("\n   📈 النتائج:")
print(f"      - Accuracy: {val_accuracy:.4f} ({val_accuracy*100:.2f}%)")
print(f"      - Precision: {val_precision:.4f} ({val_precision*100:.2f}%)")
print(f"      - Recall: {val_recall:.4f} ({val_recall*100:.2f}%)")
print(f"      - F1-Score: {val_f1:.4f} ({val_f1*100:.2f}%)")

# Save validation results
val_results_path = os.path.join(training_dir, 'svm_validation_results.txt')
with open(val_results_path, 'w', encoding='utf-8') as f:
    f.write("SVM Model - Validation Results\n")
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

print(f"   💾 تم حفظ نتائج Validation في: {val_results_path}")

# ============================================
# 5. Train Logistic Regression (Comparison)
# ============================================
print("\n🤖 5. تدريب Logistic Regression (مقارنة)...")
lr_model = LogisticRegression(
    max_iter=1000,
    C=1.0,
    penalty='l2',
    random_state=42
)

print("   🔄 بدء التدريب...")
start_time_lr = datetime.now()
lr_model.fit(X_train, y_train)
training_time_lr = (datetime.now() - start_time_lr).total_seconds()
print(f"   ✅ تم التدريب بنجاح! (الوقت: {training_time_lr:.2f} ثانية)")

# Save model
lr_path = os.path.join(models_dir, 'lr_model.pkl')
joblib.dump(lr_model, lr_path)
print(f"   💾 تم حفظ النموذج في: {lr_path}")

# Evaluate
y_val_pred_lr = lr_model.predict(X_val)
val_accuracy_lr = accuracy_score(y_val, y_val_pred_lr)
val_f1_lr = f1_score(y_val, y_val_pred_lr)

print(f"\n   📈 النتائج (Logistic Regression):")
print(f"      - Accuracy: {val_accuracy_lr:.4f} ({val_accuracy_lr*100:.2f}%)")
print(f"      - F1-Score: {val_f1_lr:.4f} ({val_f1_lr*100:.2f}%)")

# Save LR validation results
lr_val_results_path = os.path.join(training_dir, 'lr_validation_results.txt')
with open(lr_val_results_path, 'w', encoding='utf-8') as f:
    f.write("Logistic Regression Model - Validation Results\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Training Time: {training_time_lr:.2f} seconds\n\n")
    f.write("Metrics:\n")
    f.write(f"  - Accuracy: {val_accuracy_lr:.4f} ({val_accuracy_lr*100:.2f}%)\n")
    f.write(f"  - F1-Score: {val_f1_lr:.4f} ({val_f1_lr*100:.2f}%)\n\n")
    f.write("Classification Report:\n")
    f.write(classification_report(y_val, y_val_pred_lr,
                                target_names=['Normal Query', 'SQL Injection']))

print(f"   💾 تم حفظ نتائج Validation في: {lr_val_results_path}")

# ============================================
# 6. Select Best Model and Test on Test Set
# ============================================
print("\n" + "=" * 80)
print("6. اختيار أفضل نموذج واختباره على Test Set")
print("=" * 80)

# Select best model based on F1-Score
if val_f1 >= val_f1_lr:
    best_model = svm_model
    best_model_name = "SVM"
    print(f"\n✅ أفضل نموذج: SVM (F1-Score: {val_f1:.4f})")
else:
    best_model = lr_model
    best_model_name = "Logistic Regression"
    print(f"\n✅ أفضل نموذج: Logistic Regression (F1-Score: {val_f1_lr:.4f})")

# Test on Test Set
print("\n📊 اختبار على Test Set...")
y_test_pred = best_model.predict(X_test)

test_accuracy = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred)
test_recall = recall_score(y_test, y_test_pred)
test_f1 = f1_score(y_test, y_test_pred)

print("\n   📈 النتائج النهائية:")
print(f"      - Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
print(f"      - Precision: {test_precision:.4f} ({test_precision*100:.2f}%)")
print(f"      - Recall: {test_recall:.4f} ({test_recall*100:.2f}%)")
print(f"      - F1-Score: {test_f1:.4f} ({test_f1*100:.2f}%)")

# ============================================
# 7. Confusion Matrix
# ============================================
print("\n📊 7. إنشاء Confusion Matrix...")
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal Query', 'SQL Injection'],
            yticklabels=['Normal Query', 'SQL Injection'],
            cbar_kws={'label': 'Count'})
plt.title(f'Confusion Matrix - {best_model_name} Model\nTest Set Results', 
          fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()

cm_path = os.path.join(evaluation_dir, 'confusion_matrix.png')
plt.savefig(cm_path, dpi=300, bbox_inches='tight')
print(f"   💾 تم حفظ Confusion Matrix في: {cm_path}")

# ============================================
# 8. Save Final Results
# ============================================
results_path = os.path.join(evaluation_dir, 'final_test_results.txt')
with open(results_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("Final Test Results - SQL Injection Detection Model\n")
    f.write("=" * 80 + "\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("Best Model: " + best_model_name + "\n\n")
    
    f.write("Vectorization Settings:\n")
    f.write(f"  - max_features: 10000\n")
    f.write(f"  - ngram_range: (1, 3)\n")
    f.write(f"  - min_df: 2\n")
    f.write(f"  - max_df: 1.0\n")
    f.write(f"  - lowercase: False\n\n")
    
    f.write("Model Comparison (Validation Set):\n")
    f.write(f"  - SVM Accuracy: {val_accuracy:.4f} | F1-Score: {val_f1:.4f}\n")
    f.write(f"  - LR Accuracy: {val_accuracy_lr:.4f} | F1-Score: {val_f1_lr:.4f}\n\n")
    
    f.write("Final Test Set Results:\n")
    f.write(f"  - Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {test_precision:.4f} ({test_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {test_recall:.4f} ({test_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {test_f1:.4f} ({test_f1*100:.2f}%)\n\n")
    
    f.write("Classification Report:\n")
    f.write(classification_report(y_test, y_test_pred,
                                target_names=['Normal Query', 'SQL Injection']))

print(f"   💾 تم حفظ النتائج النهائية في: {results_path}")

# ============================================
# 9. Summary
# ============================================
print("\n" + "=" * 80)
print("✅ تم التدريب بنجاح!")
print("=" * 80)

print(f"\n📊 الملخص النهائي:")
print(f"   - النموذج المستخدم: {best_model_name}")
print(f"   - Accuracy: {test_accuracy*100:.2f}%")
print(f"   - F1-Score: {test_f1*100:.2f}%")
print(f"   - Precision: {test_precision*100:.2f}%")
print(f"   - Recall: {test_recall*100:.2f}%")

print(f"\n📁 التنظيم النهائي:")
print(f"   📂 models/")
print(f"      - tfidf_vectorizer.pkl")
print(f"      - svm_model.pkl")
print(f"      - lr_model.pkl")
print(f"   📂 results/vectorization/")
print(f"      - dataset_info.txt")
print(f"      - vectorization_info.txt")
print(f"      - X_train_sparse.npz")
print(f"      - X_val_sparse.npz")
print(f"      - X_test_sparse.npz")
print(f"   📂 results/training/")
print(f"      - svm_validation_results.txt")
print(f"      - lr_validation_results.txt")
print(f"   📂 results/evaluation/")
print(f"      - confusion_matrix.png")
print(f"      - final_test_results.txt")

print("\n" + "=" * 80)
print("🎉 جاهز للاستخدام!")
print("=" * 80)
