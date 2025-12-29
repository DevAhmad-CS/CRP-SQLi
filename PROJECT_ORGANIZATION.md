# تنظيم المشروع - Project Organization

## 📁 هيكل المجلدات النهائي

```
CRP-SQLi/
│
├── dataset/                          # البيانات
│   ├── original/                     # البيانات الأصلية
│   │   └── Modified_SQL_Dataset.csv
│   └── final/                        # البيانات النهائية
│       ├── train_final.csv
│       ├── validation_final.csv
│       └── test_final.csv
│
├── scripts/                          # السكربتات
│   ├── 1_advanced_clean.py          # التنظيف المتقدم
│   ├── 2_detect_false_positives.py  # كشف False Positives
│   ├── 3_generate_new_patterns.py   # توليد الأنماط الجديدة
│   ├── 4_balance_dataset.py         # إعادة التوازن
│   ├── 5_final_split.py             # التقسيم النهائي
│   └── 6_train_model.py             # تدريب النموذج
│
├── models/                           # النماذج المدربة
│   ├── tfidf_vectorizer.pkl         # Vectorizer المحفوظ
│   ├── svm_model.pkl                 # نموذج SVM
│   └── lr_model.pkl                  # نموذج Logistic Regression
│
├── results/                          # النتائج
│   ├── vectorization/                # نتائج التحويل
│   │   ├── dataset_info.txt         # معلومات Dataset
│   │   ├── vectorization_info.txt   # معلومات التحويل
│   │   ├── X_train_sparse.npz      # متجهات Train
│   │   ├── X_val_sparse.npz        # متجهات Validation
│   │   └── X_test_sparse.npz       # متجهات Test
│   │
│   ├── training/                     # نتائج التدريب
│   │   ├── svm_validation_results.txt
│   │   └── lr_validation_results.txt
│   │
│   └── evaluation/                   # نتائج التقييم
│       ├── confusion_matrix.png     # Confusion Matrix
│       └── final_test_results.txt   # النتائج النهائية
│
├── docs/                             # التوثيق
│   ├── complete_project_summary.md
│   ├── dataset_evaluation_report.md
│   └── methods_and_tools.md
│
├── review/                           # المراجعة
│   └── suspicious_queries_for_review.csv
│
├── README.md
├── requirements.txt
└── PROJECT_ORGANIZATION.md           # هذا الملف
```

---

## 📂 شرح المجلدات

### 📂 models/
**الوصف:** يحتوي على جميع النماذج المدربة والـ Vectorizer

**الملفات:**
- `tfidf_vectorizer.pkl` - Vectorizer المحفوظ (للاستخدام لاحقاً)
- `svm_model.pkl` - نموذج SVM المدرب
- `lr_model.pkl` - نموذج Logistic Regression المدرب

**الاستخدام:**
```python
import joblib
vectorizer = joblib.load('models/tfidf_vectorizer.pkl')
model = joblib.load('models/svm_model.pkl')
```

---

### 📂 results/vectorization/
**الوصف:** نتائج مرحلة تحويل النصوص إلى متجهات

**الملفات:**
- `dataset_info.txt` - معلومات عن Dataset (الحجم، التوازن)
- `vectorization_info.txt` - معلومات عن التحويل (الإعدادات، النتائج)
- `X_train_sparse.npz` - متجهات Train (Sparse Matrix)
- `X_val_sparse.npz` - متجهات Validation
- `X_test_sparse.npz` - متجهات Test

**الاستخدام:**
```python
from scipy.sparse import load_npz
X_train = load_npz('results/vectorization/X_train_sparse.npz')
```

---

### 📂 results/training/
**الوصف:** نتائج مرحلة التدريب

**الملفات:**
- `svm_validation_results.txt` - نتائج SVM على Validation Set
- `lr_validation_results.txt` - نتائج Logistic Regression على Validation Set

**المحتوى:**
- Metrics (Accuracy, Precision, Recall, F1-Score)
- Classification Report
- Training Time

---

### 📂 results/evaluation/
**الوصف:** نتائج التقييم النهائي على Test Set

**الملفات:**
- `confusion_matrix.png` - صورة Confusion Matrix
- `final_test_results.txt` - النتائج النهائية الكاملة

**المحتوى:**
- Final Metrics
- Classification Report
- Model Comparison

---

## 🔄 سير العمل (Workflow)

### المرحلة 1: تحضير البيانات
```
scripts/1_advanced_clean.py
  → dataset/Advanced_Cleaned_Dataset.csv
```

### المرحلة 2: كشف False Positives
```
scripts/2_detect_false_positives.py
  → dataset/False_Positives_Corrected_Dataset.csv
```

### المرحلة 3: إضافة الأنماط الجديدة
```
scripts/3_generate_new_patterns.py
  → dataset/New_SQLi_Patterns.csv
```

### المرحلة 4: إعادة التوازن
```
scripts/4_balance_dataset.py
  → dataset/Balanced_Dataset.csv
```

### المرحلة 5: التقسيم النهائي
```
scripts/5_final_split.py
  → dataset/final/train_final.csv
  → dataset/final/validation_final.csv
  → dataset/final/test_final.csv
```

### المرحلة 6: التدريب
```
scripts/6_train_model.py
  → models/tfidf_vectorizer.pkl
  → models/svm_model.pkl
  → models/lr_model.pkl
  → results/vectorization/* (متجهات)
  → results/training/* (نتائج التدريب)
  → results/evaluation/* (نتائج التقييم)
```

---

## 📝 ملاحظات مهمة

### التنظيم:
- ✅ كل مرحلة في مجلدها الخاص
- ✅ أسماء واضحة ومفهومة
- ✅ ملفات منظمة حسب الوظيفة

### الحفظ:
- ✅ النماذج محفوظة في `models/`
- ✅ المتجهات محفوظة في `results/vectorization/`
- ✅ النتائج محفوظة في `results/training/` و `results/evaluation/`

### الاستخدام لاحقاً:
- يمكن تحميل النماذج والـ Vectorizer للاستخدام
- يمكن تحميل المتجهات لتجربة نماذج جديدة
- جميع النتائج موثقة في ملفات نصية

---

**آخر تحديث:** 2025  
**الحالة:** ✅ منظم وجاهز

