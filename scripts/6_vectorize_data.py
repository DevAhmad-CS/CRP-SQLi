"""
Vectorization Script - Convert text to vectors only
This script converts SQL queries to numerical vectors using TF-IDF
and saves everything for later use in training
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import save_npz
import joblib
import os
from datetime import datetime

print("=" * 80)
print("تحويل النصوص إلى متجهات (TF-IDF)")
print("=" * 80)

# Create directories
base_dir = '../'
models_dir = os.path.join(base_dir, 'models')
results_dir = os.path.join(base_dir, 'results')
vectorization_dir = os.path.join(results_dir, 'vectorization')

for directory in [models_dir, results_dir, vectorization_dir]:
    os.makedirs(directory, exist_ok=True)

print(f"\n📁 المجلدات:")
print(f"   - models/ - لحفظ Vectorizer")
print(f"   - results/vectorization/ - لحفظ المتجهات والنتائج")

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

# Save data info
data_info_path = os.path.join(vectorization_dir, 'dataset_info.txt')
with open(data_info_path, 'w', encoding='utf-8') as f:
    f.write("Dataset Information\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    f.write(f"Train Set: {len(train_df):,} samples\n")
    f.write(f"Validation Set: {len(val_df):,} samples\n")
    f.write(f"Test Set: {len(test_df):,} samples\n\n")
    
    train_labels = train_df['Label'].value_counts()
    f.write("Train Set Balance:\n")
    for label, count in train_labels.items():
        percentage = (count / len(train_df)) * 100
        label_name = "SQL Injection" if label == 1 else "Normal Query"
        f.write(f"  - {label_name}: {count:,} ({percentage:.2f}%)\n")

print(f"   💾 تم حفظ معلومات Dataset في: {data_info_path}")

# ============================================
# 2. Convert Text to Vectors (TF-IDF)
# ============================================
print("\n🔄 2. تحويل النصوص إلى متجهات (TF-IDF)...")
print("   ⚙️  الإعدادات:")
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

# Calculate sparsity
sparsity = (1 - X_train.nnz / (X_train.shape[0] * X_train.shape[1])) * 100
print(f"      - Sparsity: {sparsity:.2f}%")

# ============================================
# 3. Save Vectorizer
# ============================================
print("\n💾 3. حفظ Vectorizer...")
vectorizer_path = os.path.join(models_dir, 'tfidf_vectorizer.pkl')
joblib.dump(vectorizer, vectorizer_path)
print(f"   ✅ تم حفظ Vectorizer في: {vectorizer_path}")

# ============================================
# 4. Save Vectors
# ============================================
print("\n💾 4. حفظ المتجهات...")

# Save sparse matrices
X_train_path = os.path.join(vectorization_dir, 'X_train_sparse.npz')
X_val_path = os.path.join(vectorization_dir, 'X_val_sparse.npz')
X_test_path = os.path.join(vectorization_dir, 'X_test_sparse.npz')

save_npz(X_train_path, X_train)
save_npz(X_val_path, X_val)
save_npz(X_test_path, X_test)

print(f"   ✅ تم حفظ X_train في: {X_train_path}")
print(f"   ✅ تم حفظ X_val في: {X_val_path}")
print(f"   ✅ تم حفظ X_test في: {X_test_path}")

# Save labels
y_train_path = os.path.join(vectorization_dir, 'y_train.npy')
y_val_path = os.path.join(vectorization_dir, 'y_val.npy')
y_test_path = os.path.join(vectorization_dir, 'y_test.npy')

np.save(y_train_path, y_train)
np.save(y_val_path, y_val)
np.save(y_test_path, y_test)

print(f"   ✅ تم حفظ y_train في: {y_train_path}")
print(f"   ✅ تم حفظ y_val في: {y_val_path}")
print(f"   ✅ تم حفظ y_test في: {y_test_path}")

# ============================================
# 5. Save Vectorization Info
# ============================================
vectorization_info_path = os.path.join(vectorization_dir, 'vectorization_info.txt')
with open(vectorization_info_path, 'w', encoding='utf-8') as f:
    f.write("Vectorization Information\n")
    f.write("=" * 50 + "\n\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
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
    f.write(f"  - Sparsity: {sparsity:.2f}%\n")
    f.write(f"  - Non-zero elements: {X_train.nnz:,}\n")

print(f"   💾 تم حفظ معلومات التحويل في: {vectorization_info_path}")

# ============================================
# 6. Summary
# ============================================
print("\n" + "=" * 80)
print("✅ تم التحويل بنجاح!")
print("=" * 80)

print(f"\n📊 الملخص:")
print(f"   - عدد الميزات: {X_train.shape[1]:,}")
print(f"   - Sparsity: {sparsity:.2f}%")
print(f"   - Vectorizer محفوظ في: models/tfidf_vectorizer.pkl")
print(f"   - المتجهات محفوظة في: results/vectorization/")

print(f"\n📁 الملفات المحفوظة:")
print(f"   - models/tfidf_vectorizer.pkl")
print(f"   - results/vectorization/X_train_sparse.npz")
print(f"   - results/vectorization/X_val_sparse.npz")
print(f"   - results/vectorization/X_test_sparse.npz")
print(f"   - results/vectorization/y_train.npy")
print(f"   - results/vectorization/y_val.npy")
print(f"   - results/vectorization/y_test.npy")

print("\n" + "=" * 80)
print("🎉 جاهز للتدريب!")
print("=" * 80)
print("\nالخطوة التالية: تشغيل scripts/7_train_svm.py")

