# 🚀 إعداد Render للـ Deployment

## 📋 الإعدادات المطلوبة في Render

### 1. Basic Settings
- **Name**: `sql-injection-detector` (أو أي اسم تريده)
- **Region**: اختر الأقرب لك (Singapore, Frankfurt, etc.)
- **Branch**: `main`
- **Root Directory**: **اتركه فارغاً** (أو `.`)

### 2. Build & Deploy
- **Environment**: `Python 3` (سيستخدم Python 3.12 تلقائياً بسبب `runtime.txt`)
- **Build Command**: 
  ```bash
  pip install --upgrade pip && pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  cd web_app && uvicorn main:app --host 0.0.0.0 --port $PORT
  ```

### ⚠️ مهم: Python Version
- تم إضافة `runtime.txt` لتحديد Python 3.12.8
- هذا يحل مشكلة توافق scikit-learn مع Python 3.13

### 3. Advanced Settings (اختياري)
- **Auto-Deploy**: `Yes` (يحدث تلقائياً عند push جديد)
- **Health Check Path**: `/` (أو اتركه فارغاً)

---

## ⚠️ ملاحظات مهمة

### 1. Models (ملفات .pkl)
- Models موجودة في `models/` لكنها **مستبعدة** من Git (في `.gitignore`)
- يجب رفعها يدوياً إلى Render:
  - اذهب إلى Render Dashboard → Environment
  - أضف Environment Variable أو استخدم **Persistent Disk** لرفع الملفات

### 2. Environment Variables (إن احتجت)
- يمكنك إضافة متغيرات البيئة في Render Dashboard → Environment

### 3. Port
- Render يستخدم متغير `$PORT` تلقائياً
- لا تغيره في Start Command

---

## 🔧 إذا واجهت مشاكل

### مشكلة: "Module not found"
- تأكد من أن `requirements.txt` موجود في Root Directory
- تأكد من أن جميع المكتبات موجودة في `requirements.txt`

### مشكلة: "Models not found"
- Models موجودة في `models/` لكنها غير مرفوعة
- يجب رفعها يدوياً أو استخدام Git LFS

### مشكلة: "Port already in use"
- تأكد من استخدام `$PORT` في Start Command
- Render يحدد الـ port تلقائياً

---

## ✅ Checklist

- [ ] Root Directory: فارغ (أو `.`)
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `cd web_app && uvicorn main:app --host 0.0.0.0 --port $PORT`
- [ ] Environment: Python 3
- [ ] Branch: main
- [ ] Auto-Deploy: Yes

---

**جاهز! 🚀**

