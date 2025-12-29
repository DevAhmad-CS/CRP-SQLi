# شرح منطق التنبؤ (Prediction Logic)

## كيف يعمل التنبؤ في النظام؟

### الخطوات:

#### 1. **تحويل الاستعلام إلى أرقام (Vectorization)**
```python
query_vector = vectorizer.transform([query])
```
- يأخذ الاستعلام النصي (مثل `"1'; DROP TABLE users--"`)
- يحوله إلى متجه رقمي (vector) باستخدام TF-IDF
- النتيجة: متجه ببعد 10,000 (كل رقم يمثل ميزة معينة)

---

#### 2. **حساب الاحتمالات (Probability Calculation)**
```python
prediction_proba = model.predict_proba(query_vector)[0]
normal_prob = float(prediction_proba[0])      # احتمال أن يكون عادي
malicious_prob = float(prediction_proba[1])   # احتمال أن يكون SQL Injection
```

**مثال:**
- `normal_prob = 0.4623` (46.23%)
- `malicious_prob = 0.5377` (53.77%)

---

#### 3. **اتخاذ القرار (Decision Making)**
```python
# إذا كان احتمال SQL Injection > 0.5 → SQL Injection
# إذا كان احتمال Normal > 0.5 → Normal Query
is_malicious = malicious_prob > 0.5
```

**مثال:**
- `malicious_prob = 0.5377` (53.77%)
- `0.5377 > 0.5` → `True`
- النتيجة: **SQL Injection**

---

#### 4. **حساب الثقة (Confidence Score)**
```python
# الثقة = الاحتمال الأعلى
confidence = malicious_prob * 100  # إذا كان SQL Injection
# أو
confidence = normal_prob * 100     # إذا كان Normal
```

**مثال:**
- `malicious_prob = 0.5377`
- `confidence = 0.5377 * 100 = 53.77%`

---

## الفرق بين الطريقة القديمة والجديدة:

### ❌ **الطريقة القديمة (كانت تسبب مشاكل):**
```python
prediction = model.predict(query_vector)[0]  # يعطي 0 أو 1 مباشرة
is_malicious = bool(prediction)              # قد يعطي Normal رغم أن Malicious أعلى!
```

**المشكلة:**
- `predict()` يستخدم `decision_function()` داخلياً
- قد يعطي `0` (Normal) رغم أن `predict_proba()` يعطي `malicious_prob = 0.5377` (أعلى من 0.5!)

---

### ✅ **الطريقة الجديدة (الحالية):**
```python
prediction_proba = model.predict_proba(query_vector)[0]
is_malicious = malicious_prob > 0.5  # قرار مباشر بناءً على الاحتمالات
```

**المزايا:**
- قرار واضح بناءً على الاحتمالات
- إذا `malicious_prob > 0.5` → SQL Injection
- إذا `normal_prob > 0.5` → Normal Query
- لا توجد تناقضات

---

## مثال كامل:

### الاستعلام: `"1'; DROP TABLE users--"`

#### الخطوة 1: Vectorization
```
"1'; DROP TABLE users--" 
    ↓
[0.0, 0.5, 0.3, 0.8, ..., 0.2]  (10,000 رقم)
```

#### الخطوة 2: Probability Calculation
```
normal_prob = 0.4623 (46.23%)
malicious_prob = 0.5377 (53.77%)
```

#### الخطوة 3: Decision
```
malicious_prob (0.5377) > 0.5? → True
is_malicious = True
result_label = "SQL Injection"
```

#### الخطوة 4: Confidence
```
confidence = 0.5377 * 100 = 53.77%
```

#### النتيجة النهائية:
```json
{
    "prediction": "SQL Injection",
    "is_malicious": true,
    "confidence": 53.77,
    "probabilities": {
        "normal": 46.23,
        "malicious": 53.77
    }
}
```

---

## الخلاصة:

1. **Vectorization**: تحويل النص إلى أرقام
2. **Probability**: حساب احتمالية كل فئة
3. **Decision**: اختيار الفئة بناءً على الاحتمال الأعلى (> 0.5)
4. **Confidence**: استخدام الاحتمال الأعلى كدرجة ثقة

**القاعدة الأساسية:**
- إذا `malicious_prob > 0.5` → **SQL Injection**
- إذا `normal_prob > 0.5` → **Normal Query**

