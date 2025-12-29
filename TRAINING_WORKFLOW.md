# خطة التدريب - Training Workflow

## 📋 الترتيب الصحيح للتدريب

### المرحلة 1: تحويل النصوص إلى متجهات
**السكربت:** `scripts/6_vectorize_data.py`

**ما يفعله:**
- تحميل البيانات (Train/Val/Test)
- تحويل النصوص إلى متجهات باستخدام TF-IDF
- حفظ Vectorizer
- حفظ المتجهات (X_train, X_val, X_test)
- حفظ Labels (y_train, y_val, y_test)
- حفظ معلومات التحويل

**النتائج:**
- `models/tfidf_vectorizer.pkl`
- `results/vectorization/X_train_sparse.npz`
- `results/vectorization/X_val_sparse.npz`
- `results/vectorization/X_test_sparse.npz`
- `results/vectorization/y_train.npy`
- `results/vectorization/y_val.npy`
- `results/vectorization/y_test.npy`

---

### المرحلة 2: تدريب SVM
**السكربت:** `scripts/7_train_svm.py`

**ما يفعله:**
- تحميل المتجهات المحفوظة
- تدريب نموذج SVM
- تقييم على Validation Set
- حفظ النموذج
- حفظ النتائج

**النتائج:**
- `models/svm_model.pkl`
- `results/training/svm_validation_results.txt`

---

### المرحلة 3: تدريب Logistic Regression
**السكربت:** `scripts/8_train_lr.py`

**ما يفعله:**
- تحميل المتجهات المحفوظة (نفس المتجهات)
- تدريب نموذج Logistic Regression
- تقييم على Validation Set
- حفظ النموذج
- حفظ النتائج

**النتائج:**
- `models/lr_model.pkl`
- `results/training/lr_validation_results.txt`

---

### المرحلة 4: المقارنة والاختبار النهائي
**السكربت:** `scripts/9_compare_and_test.py`

**ما يفعله:**
- تحميل كلا النموذجين
- مقارنة النتائج على Validation Set
- اختيار الأفضل (بناءً على F1-Score)
- اختبار الأفضل على Test Set
- إنشاء Confusion Matrix
- حفظ النتائج النهائية

**النتائج:**
- `results/evaluation/confusion_matrix.png`
- `results/evaluation/final_test_results.txt`

---

## 🔄 سير العمل الكامل

```
1. تشغيل: scripts/6_vectorize_data.py
   ↓
   [تحويل النصوص إلى متجهات]
   ↓
2. تشغيل: scripts/7_train_svm.py
   ↓
   [تدريب SVM وتقييمه]
   ↓
3. تشغيل: scripts/8_train_lr.py
   ↓
   [تدريب Logistic Regression وتقييمه]
   ↓
4. تشغيل: scripts/9_compare_and_test.py
   ↓
   [مقارنة واختيار الأفضل واختباره]
   ↓
   ✅ النتيجة النهائية
```

---

## 📁 التنظيم النهائي

```
CRP-SQLi/
├── models/
│   ├── tfidf_vectorizer.pkl      (من المرحلة 1)
│   ├── svm_model.pkl             (من المرحلة 2)
│   └── lr_model.pkl              (من المرحلة 3)
│
├── results/
│   ├── vectorization/            (من المرحلة 1)
│   │   ├── X_train_sparse.npz
│   │   ├── X_val_sparse.npz
│   │   ├── X_test_sparse.npz
│   │   ├── y_train.npy
│   │   ├── y_val.npy
│   │   └── y_test.npy
│   │
│   ├── training/                 (من المرحلة 2 و 3)
│   │   ├── svm_validation_results.txt
│   │   └── lr_validation_results.txt
│   │
│   └── evaluation/               (من المرحلة 4)
│       ├── confusion_matrix.png
│       └── final_test_results.txt
```

---

## ✅ المميزات

1. **فصل واضح:** كل مرحلة في سكربت منفصل
2. **جزء جزء:** تدريب كل نموذج على حدة
3. **إعادة الاستخدام:** المتجهات محفوظة يمكن استخدامها لاحقاً
4. **منظم:** كل شيء في مجلداته
5. **واضح:** أسماء مفهومة وترتيب منطقي

---

## 🚀 كيفية التشغيل

### الخطوة 1: التحويل
```bash
cd scripts
python 6_vectorize_data.py
```

### الخطوة 2: تدريب SVM
```bash
python 7_train_svm.py
```

### الخطوة 3: تدريب Logistic Regression
```bash
python 8_train_lr.py
```

### الخطوة 4: المقارنة والاختبار
```bash
python 9_compare_and_test.py
```

---

**آخر تحديث:** 2025  
**الحالة:** ✅ جاهز للاستخدام

