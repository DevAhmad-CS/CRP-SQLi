# الأدوات والطرق المستخدمة لتنظيف وتحسين Dataset

## 📋 نظرة عامة

هذا الملف يوضح جميع الأدوات والطرق والتقنيات المستخدمة لتنظيف وتحسين Dataset للكشف عن SQL Injection.

---

## 🛠️ الأدوات المستخدمة

### المكتبات البرمجية:

1. **Pandas** (`pandas`)
   - قراءة ومعالجة البيانات من CSV
   - عمليات التصفية والتنظيف
   - دمج البيانات

2. **NumPy** (`numpy`)
   - العمليات الحسابية
   - معالجة المصفوفات

3. **Scikit-learn** (`sklearn`)
   - `train_test_split`: تقسيم البيانات
   - `stratify`: الحفاظ على التوازن في التقسيم

4. **Regular Expressions** (`re`)
   - البحث عن الأنماط في النصوص
   - كشف SQL Injection patterns

5. **urllib.parse**
   - ترميز URL (URL Encoding)
   - تحويل النصوص إلى ترميز URL

---

## 🔧 الطرق والتقنيات المستخدمة

### 1️⃣ التنظيف المتقدم (Advanced Cleaning)

#### الطرق المستخدمة:

**أ) إزالة الاستعلامات الطويلة جداً:**
```python
df = df[df['Query'].str.len() <= 5000]
```
- **السبب:** الاستعلامات الطويلة جداً (>5000 حرف) قد تكون أخطاء أو بيانات غير واقعية
- **النتيجة:** إزالة 1 استعلام

**ب) تنظيف المسافات الزائدة:**
```python
df['Query'] = df['Query'].str.replace(r'\s+', ' ', regex=True)  # مسافات متعددة → واحدة
df['Query'] = df['Query'].str.strip()  # إزالة المسافات من البداية والنهاية
```
- **السبب:** توحيد التنسيق وتحسين جودة البيانات
- **النتيجة:** بيانات منظمة ونظيفة

**ج) إزالة الاستعلامات التي تحتوي على رموز فقط:**
```python
df = df[df['Query'].str.contains(r'[a-zA-Z0-9]', regex=True, na=False)]
```
- **السبب:** الاستعلامات التي تحتوي على رموز فقط (مثل `!@#$%`) غير منطقية
- **النتيجة:** إزالة البيانات غير المفيدة

**د) إزالة الأحرف غير القابلة للطباعة:**
```python
def remove_non_printable(text):
    return ''.join(char for char in str(text) if char.isprintable() or char in ['\n', '\t', '\r'])
```
- **السبب:** الأحرف مثل `\x00`, `\x01` قد تسبب مشاكل في المعالجة
- **النتيجة:** بيانات نظيفة وآمنة للمعالجة

---

### 2️⃣ كشف False Positives

#### الطريقة: Pattern Matching باستخدام Regular Expressions

**القواعد المستخدمة:**

```python
sqli_patterns = [
    r"'\s*or\s*['\"]?\s*1\s*=\s*1",  # OR 1=1
    r"union\s+select.*version",  # UNION SELECT version
    r"sleep\s*\(",  # SLEEP(
    r"pg_sleep\s*\(",  # pg_sleep(
    r"waitfor\s+delay",  # WAITFOR DELAY
    r"benchmark\s*\(",  # benchmark(
    r"'\s*--\s*'",  # '--'
    # ... وغيرها
]
```

**الخطوات:**
1. فحص جميع الاستعلامات الطبيعية (Label=0)
2. تطبيق القواعد على كل استعلام
3. إذا تطابق مع أي نمط → إعادة تصنيف إلى Label=1
4. حفظ الاستعلامات المشبوهة للمراجعة

**النتيجة:**
- تم كشف 8 False Positives
- تم إعادة تصنيفها تلقائياً

---

### 3️⃣ توليد أنماط SQL Injection جديدة

#### الطرق المستخدمة:

**أ) Blind SQL Injection (Boolean-based):**
- استخدام `AND (SELECT...)` للاستنتاج البوليني
- أنماط لـ MySQL, PostgreSQL, MSSQL, Oracle
- مثال: `' AND (SELECT SUBSTRING(@@version,1,1))='5' --`

**ب) Blind SQL Injection (Time-based):**
- استخدام دوال التأخير: `SLEEP()`, `pg_sleep()`, `WAITFOR DELAY`
- مثال: `' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --`

**ج) Second-order SQL Injection:**
- محاكاة سيناريوهات واقعية
- أنماط للتخزين والاستخدام اللاحق
- مثال: `admin'--`, `user' OR '1'='1`

**د) SQL Injection مع ترميز:**
- **URL Encoding:** استخدام `urllib.parse.quote()`
  - مثال: `' OR 1=1` → `%27%20OR%201%3D1`
- **Double URL Encoding:** ترميز مرتين
- **Hex Encoding:** استخدام `0x27`, `CHAR(39)`
- **Unicode Encoding:** استخدام `%u0027`, `\u0027`

**هـ) NoSQL Injection:**
- أنماط MongoDB: `{"$ne": null}`, `{"$gt": ""}`, `{"$regex": ".*"}`

**النتيجة:**
- تم توليد 124 نمط جديد
- تم حفظها في ملف منفصل ثم دمجها

---

### 4️⃣ إعادة التوازن

#### الطرق المستخدمة:

**أ) Undersampling (تقليل الأغلبية):**
```python
normal_queries = normal_queries.sample(n=target_normal, random_state=42)
```
- **الطريقة:** أخذ عينة عشوائية من الاستعلامات الطبيعية
- **السبب:** تقليل عدد الاستعلامات الطبيعية للوصول إلى توازن أفضل
- **النتيجة:** تقليل من 19,474 إلى 13,756

**ب) Data Augmentation (زيادة الأقلية):**
```python
def augment_sqli(query):
    # إضافة مسافات عشوائية
    # تغيير حالة الأحرف
    # إضافة تعليقات SQL
    # تغيير ترتيب الكلمات
```
- **الطريقة:** تعديل استعلامات SQL Injection الموجودة لإنشاء متغيرات جديدة
- **السبب:** زيادة تنوع البيانات دون فقدان المعلومات
- **النتيجة:** زيادة تنوع الأنماط

**النتيجة النهائية:**
- التوازن: من 58.26% إلى 83.34%
- نسبة 54.54% طبيعي | 45.46% SQL Injection

---

### 5️⃣ التقسيم النهائي

#### الطريقة: Stratified Split

```python
train_df, temp_df = train_test_split(
    df, 
    test_size=0.3, 
    random_state=42, 
    stratify=df['Label']  # الحفاظ على التوازن
)
```

**المميزات:**
- **Stratify:** يضمن الحفاظ على نسبة Labels في كل قسم
- **Random State:** يضمن إمكانية إعادة النتائج
- **النسبة:** 70% Train, 15% Validation, 15% Test

**النتيجة:**
- كل قسم يحافظ على التوازن (~54.5% طبيعي | ~45.5% SQL Injection)
- جاهز للتدريب مباشرة

---

## 📊 السكربتات المستخدمة

### 1. `advanced_clean.py`
**الوظيفة:** التنظيف المتقدم للبيانات
**الطرق:**
- إزالة الاستعلامات الطويلة
- تنظيف المسافات
- إزالة الأحرف غير القابلة للطباعة
- إزالة البيانات غير المنطقية

### 2. `detect_false_positives.py`
**الوظيفة:** كشف وإعادة تصنيف False Positives
**الطرق:**
- Pattern Matching باستخدام Regular Expressions
- فحص تلقائي لجميع الاستعلامات
- إعادة تصنيف تلقائية

### 3. `generate_new_patterns.py`
**الوظيفة:** توليد أنماط SQL Injection جديدة
**الطرق:**
- إنشاء أنماط Blind SQL Injection
- إنشاء أنماط Time-based
- إنشاء أنماط Second-order
- ترميز مختلف (URL, Hex, Unicode)
- NoSQL Injection

### 4. `balance_dataset.py`
**الوظيفة:** إعادة توازن Dataset
**الطرق:**
- Undersampling للاستعلامات الطبيعية
- Data Augmentation لـ SQL Injection
- دمج الأنماط الجديدة

### 5. `final_split.py`
**الوظيفة:** تقسيم Dataset النهائي
**الطرق:**
- Stratified Split
- الحفاظ على التوازن في كل قسم

---

## 🔄 سير العمل (Workflow)

```
1. البيانات الأصلية (Modified_SQL_Dataset.csv)
   ↓
2. التنظيف الأساسي (clean_dataset.py) - تم سابقاً
   ↓
3. التنظيف المتقدم (advanced_clean.py)
   ↓
4. كشف False Positives (detect_false_positives.py)
   ↓
5. توليد الأنماط الجديدة (generate_new_patterns.py)
   ↓
6. إعادة التوازن (balance_dataset.py)
   ↓
7. التقسيم النهائي (final_split.py)
   ↓
8. Dataset النهائي (train_final.csv, validation_final.csv, test_final.csv)
```

---

## 📈 الإحصائيات

### البيانات المعالجة:
- **البيانات الأصلية:** 30,919 سجل
- **بعد التنظيف المتقدم:** 30,814 سجل
- **بعد تصحيح False Positives:** 30,814 سجل
- **بعد إضافة الأنماط الجديدة:** 30,938 سجل
- **بعد إعادة التوازن:** 25,220 سجل
- **Dataset النهائي:** 25,220 سجل

### العمليات المنفذة:
- ✅ إزالة 105 سجل (ضوضاء)
- ✅ إعادة تصنيف 8 استعلامات
- ✅ إضافة 124 نمط جديد
- ✅ تقليل 5,718 استعلام طبيعي (Undersampling)
- ✅ تقسيم إلى 3 أقسام

---

## 💡 أفضل الممارسات المستخدمة

1. **الحفاظ على التوازن:** استخدام Stratified Split
2. **إزالة الضوضاء:** تنظيف شامل قبل المعالجة
3. **كشف الأخطاء:** Pattern Matching تلقائي
4. **زيادة التنوع:** إضافة أنماط جديدة متنوعة
5. **التوثيق:** حفظ كل خطوة في ملفات منفصلة

---

## 🎯 الخلاصة

تم استخدام مجموعة من الأدوات والطرق المتقدمة:
- ✅ Regular Expressions للكشف عن الأنماط
- ✅ Undersampling لإعادة التوازن
- ✅ Data Augmentation لزيادة التنوع
- ✅ Stratified Split للتقسيم المنظم
- ✅ Pattern Matching لكشف False Positives

**النتيجة:** Dataset نظيف، متوازن، متنوع، وجاهز للتدريب! 🚀

---

**تاريخ الإنشاء:** 2025  
**الأدوات:** Python, Pandas, Scikit-learn, Regular Expressions  
**عدد السكربتات:** 5

