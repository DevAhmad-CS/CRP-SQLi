"""
Model Comparison and Final Testing Script
Compare SVM and Logistic Regression models
Select the best one and test it on Test Set
"""

import numpy as np
from scipy.sparse import load_npz
import joblib
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys
from datetime import datetime

# Fix encoding for Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

print("=" * 80)
print("مقارنة النماذج واختيار الأفضل")
print("=" * 80)

# Create directories
# Get the script directory and go up to project root
script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.dirname(script_dir)  # Go up from scripts/ to project root
models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
evaluation_dir = os.path.join(results_dir, 'evaluation')

for directory in [models_dir, results_dir, evaluation_dir]:
    os.makedirs(directory, exist_ok=True)

# ============================================
# 1. Load Models and Data
# ============================================
print("\n📂 1. تحميل النماذج والبيانات...")

# Load models
svm_model = joblib.load(os.path.join(models_dir, 'svm_model.pkl'))
lr_model = joblib.load(os.path.join(models_dir, 'lr_model.pkl'))

# Load validation data
vectorization_dir = os.path.join(results_dir, 'vectorization')
X_val = load_npz(os.path.join(vectorization_dir, 'X_val_sparse.npz'))
X_test = load_npz(os.path.join(vectorization_dir, 'X_test_sparse.npz'))
y_val = np.load(os.path.join(vectorization_dir, 'y_val.npy'))
y_test = np.load(os.path.join(vectorization_dir, 'y_test.npy'))

print("   ✅ تم تحميل النماذج والبيانات")

# ============================================
# 2. Compare Models on Validation Set
# ============================================
print("\n📊 2. مقارنة النماذج على Validation Set...")

# SVM predictions
y_val_pred_svm = svm_model.predict(X_val)
svm_accuracy = accuracy_score(y_val, y_val_pred_svm)
svm_f1 = f1_score(y_val, y_val_pred_svm)
svm_precision = precision_score(y_val, y_val_pred_svm)
svm_recall = recall_score(y_val, y_val_pred_svm)

# LR predictions
y_val_pred_lr = lr_model.predict(X_val)
lr_accuracy = accuracy_score(y_val, y_val_pred_lr)
lr_f1 = f1_score(y_val, y_val_pred_lr)
lr_precision = precision_score(y_val, y_val_pred_lr)
lr_recall = recall_score(y_val, y_val_pred_lr)

print("\n   📈 نتائج SVM:")
print(f"      - Accuracy: {svm_accuracy:.4f} ({svm_accuracy*100:.2f}%)")
print(f"      - Precision: {svm_precision:.4f} ({svm_precision*100:.2f}%)")
print(f"      - Recall: {svm_recall:.4f} ({svm_recall*100:.2f}%)")
print(f"      - F1-Score: {svm_f1:.4f} ({svm_f1*100:.2f}%)")

print("\n   📈 نتائج Logistic Regression:")
print(f"      - Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)")
print(f"      - Precision: {lr_precision:.4f} ({lr_precision*100:.2f}%)")
print(f"      - Recall: {lr_recall:.4f} ({lr_recall*100:.2f}%)")
print(f"      - F1-Score: {lr_f1:.4f} ({lr_f1*100:.2f}%)")

# ============================================
# 3. Select Best Model
# ============================================
print("\n🏆 3. اختيار أفضل نموذج...")

if svm_f1 >= lr_f1:
    best_model = svm_model
    best_model_name = "SVM"
    best_f1 = svm_f1
    best_accuracy = svm_accuracy
    print(f"   ✅ أفضل نموذج: SVM (F1-Score: {svm_f1:.4f})")
else:
    best_model = lr_model
    best_model_name = "Logistic Regression"
    best_f1 = lr_f1
    best_accuracy = lr_accuracy
    print(f"   ✅ أفضل نموذج: Logistic Regression (F1-Score: {lr_f1:.4f})")

# ============================================
# 4. Test Both Models on Test Set
# ============================================
print("\n📊 4. اختبار كلا النموذجين على Test Set...")

# Test SVM on Test Set
print("\n   🔵 اختبار SVM على Test Set...")
y_test_pred_svm = svm_model.predict(X_test)
test_accuracy_svm = accuracy_score(y_test, y_test_pred_svm)
test_precision_svm = precision_score(y_test, y_test_pred_svm)
test_recall_svm = recall_score(y_test, y_test_pred_svm)
test_f1_svm = f1_score(y_test, y_test_pred_svm)

print(f"      - Accuracy: {test_accuracy_svm:.4f} ({test_accuracy_svm*100:.2f}%)")
print(f"      - Precision: {test_precision_svm:.4f} ({test_precision_svm*100:.2f}%)")
print(f"      - Recall: {test_recall_svm:.4f} ({test_recall_svm*100:.2f}%)")
print(f"      - F1-Score: {test_f1_svm:.4f} ({test_f1_svm*100:.2f}%)")

# Test LR on Test Set
print("\n   🟢 اختبار Logistic Regression على Test Set...")
y_test_pred_lr = lr_model.predict(X_test)
test_accuracy_lr = accuracy_score(y_test, y_test_pred_lr)
test_precision_lr = precision_score(y_test, y_test_pred_lr)
test_recall_lr = recall_score(y_test, y_test_pred_lr)
test_f1_lr = f1_score(y_test, y_test_pred_lr)

print(f"      - Accuracy: {test_accuracy_lr:.4f} ({test_accuracy_lr*100:.2f}%)")
print(f"      - Precision: {test_precision_lr:.4f} ({test_precision_lr*100:.2f}%)")
print(f"      - Recall: {test_recall_lr:.4f} ({test_recall_lr*100:.2f}%)")
print(f"      - F1-Score: {test_f1_lr:.4f} ({test_f1_lr*100:.2f}%)")

# Use best model for final results
test_accuracy = test_accuracy_svm if best_model_name == "SVM" else test_accuracy_lr
test_precision = test_precision_svm if best_model_name == "SVM" else test_precision_lr
test_recall = test_recall_svm if best_model_name == "SVM" else test_recall_lr
test_f1 = test_f1_svm if best_model_name == "SVM" else test_f1_lr
y_test_pred = y_test_pred_svm if best_model_name == "SVM" else y_test_pred_lr

# ============================================
# 5. Create Confusion Matrices
# ============================================
print("\n📊 5. إنشاء Confusion Matrices...")

# SVM Confusion Matrix
cm_svm = confusion_matrix(y_test, y_test_pred_svm)
plt.figure(figsize=(10, 8))
sns.heatmap(cm_svm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Normal Query', 'SQL Injection'],
            yticklabels=['Normal Query', 'SQL Injection'],
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - SVM Model\nTest Set Results', 
          fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()

cm_svm_path = os.path.join(evaluation_dir, 'confusion_matrix_svm.png')
plt.savefig(cm_svm_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   💾 تم حفظ SVM Confusion Matrix في: {cm_svm_path}")

# LR Confusion Matrix
cm_lr = confusion_matrix(y_test, y_test_pred_lr)
plt.figure(figsize=(10, 8))
sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Greens',
            xticklabels=['Normal Query', 'SQL Injection'],
            yticklabels=['Normal Query', 'SQL Injection'],
            cbar_kws={'label': 'Count'})
plt.title('Confusion Matrix - Logistic Regression Model\nTest Set Results', 
          fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()

cm_lr_path = os.path.join(evaluation_dir, 'confusion_matrix_lr.png')
plt.savefig(cm_lr_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   💾 تم حفظ LR Confusion Matrix في: {cm_lr_path}")

# Best model confusion matrix (for backward compatibility)
cm = cm_svm if best_model_name == "SVM" else cm_lr
cm_path = os.path.join(evaluation_dir, 'confusion_matrix.png')
plt.figure(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues' if best_model_name == "SVM" else 'Greens',
            xticklabels=['Normal Query', 'SQL Injection'],
            yticklabels=['Normal Query', 'SQL Injection'],
            cbar_kws={'label': 'Count'})
plt.title(f'Confusion Matrix - {best_model_name} Model\nTest Set Results', 
          fontsize=14, fontweight='bold')
plt.ylabel('True Label', fontsize=12)
plt.xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig(cm_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"   💾 تم حفظ Best Model Confusion Matrix في: {cm_path}")

# ============================================
# 6. Save Final Results
# ============================================
print("\n💾 6. حفظ النتائج النهائية...")
results_path = os.path.join(evaluation_dir, 'final_test_results.txt')
with open(results_path, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("Final Test Results - SQL Injection Detection Model\n")
    f.write("=" * 80 + "\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    f.write("Model Comparison (Validation Set):\n")
    f.write("-" * 50 + "\n")
    f.write("SVM:\n")
    f.write(f"  - Accuracy: {svm_accuracy:.4f} ({svm_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {svm_precision:.4f} ({svm_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {svm_recall:.4f} ({svm_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {svm_f1:.4f} ({svm_f1*100:.2f}%)\n\n")
    
    f.write("Logistic Regression:\n")
    f.write(f"  - Accuracy: {lr_accuracy:.4f} ({lr_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {lr_precision:.4f} ({lr_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {lr_recall:.4f} ({lr_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {lr_f1:.4f} ({lr_f1*100:.2f}%)\n\n")
    
    f.write(f"Best Model: {best_model_name}\n")
    f.write(f"Selection Criteria: F1-Score (Validation Set)\n\n")
    
    f.write("Test Set Results - Both Models:\n")
    f.write("-" * 50 + "\n")
    f.write("SVM on Test Set:\n")
    f.write(f"  - Accuracy: {test_accuracy_svm:.4f} ({test_accuracy_svm*100:.2f}%)\n")
    f.write(f"  - Precision: {test_precision_svm:.4f} ({test_precision_svm*100:.2f}%)\n")
    f.write(f"  - Recall: {test_recall_svm:.4f} ({test_recall_svm*100:.2f}%)\n")
    f.write(f"  - F1-Score: {test_f1_svm:.4f} ({test_f1_svm*100:.2f}%)\n\n")
    
    f.write("Logistic Regression on Test Set:\n")
    f.write(f"  - Accuracy: {test_accuracy_lr:.4f} ({test_accuracy_lr*100:.2f}%)\n")
    f.write(f"  - Precision: {test_precision_lr:.4f} ({test_precision_lr*100:.2f}%)\n")
    f.write(f"  - Recall: {test_recall_lr:.4f} ({test_recall_lr*100:.2f}%)\n")
    f.write(f"  - F1-Score: {test_f1_lr:.4f} ({test_f1_lr*100:.2f}%)\n\n")
    
    f.write("Final Selected Model Results:\n")
    f.write("-" * 50 + "\n")
    f.write(f"Model: {best_model_name}\n")
    f.write(f"  - Accuracy: {test_accuracy:.4f} ({test_accuracy*100:.2f}%)\n")
    f.write(f"  - Precision: {test_precision:.4f} ({test_precision*100:.2f}%)\n")
    f.write(f"  - Recall: {test_recall:.4f} ({test_recall*100:.2f}%)\n")
    f.write(f"  - F1-Score: {test_f1:.4f} ({test_f1*100:.2f}%)\n\n")
    
    f.write("SVM Classification Report:\n")
    f.write("-" * 50 + "\n")
    f.write(classification_report(y_test, y_test_pred_svm,
                                target_names=['Normal Query', 'SQL Injection']))
    f.write("\n\n")
    
    f.write("Logistic Regression Classification Report:\n")
    f.write("-" * 50 + "\n")
    f.write(classification_report(y_test, y_test_pred_lr,
                                target_names=['Normal Query', 'SQL Injection']))

print(f"   ✅ تم حفظ النتائج النهائية في: {results_path}")

# ============================================
# 7. Summary
# ============================================
print("\n" + "=" * 80)
print("✅ تم التقييم بنجاح!")
print("=" * 80)

print(f"\n📊 الملخص النهائي:")
print(f"   - النموذج المستخدم: {best_model_name}")
print(f"   - Accuracy على Test Set: {test_accuracy*100:.2f}%")
print(f"   - F1-Score على Test Set: {test_f1*100:.2f}%")
print(f"   - Precision: {test_precision*100:.2f}%")
print(f"   - Recall: {test_recall*100:.2f}%")

print(f"\n📁 الملفات المحفوظة:")
print(f"   - results/evaluation/confusion_matrix.png")
print(f"   - results/evaluation/confusion_matrix_svm.png")
print(f"   - results/evaluation/confusion_matrix_lr.png")
print(f"   - results/evaluation/final_test_results.txt")

print("\n" + "=" * 80)
print("🎉 انتهى التدريب والتقييم!")
print("=" * 80)

