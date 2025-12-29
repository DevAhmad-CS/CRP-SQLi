# 🚀 دليل رفع المشروع على GitHub

## الخطوات المطلوبة

### 1. إنشاء Repository على GitHub

1. اذهب إلى [GitHub.com](https://github.com)
2. اضغط على **"+"** في أعلى الصفحة → **"New repository"**
3. املأ البيانات:
   - **Repository name**: `CRP-SQLi` (أو أي اسم تريده)
   - **Description**: `SQL Injection Detection System using Machine Learning`
   - **Visibility**: ✅ **Private** (مهم جداً!)
   - **لا** تضع علامة على "Initialize with README" (لأننا أنشأنا README.md)
4. اضغط **"Create repository"**

### 2. ربط المشروع المحلي بـ GitHub

بعد إنشاء الـ repository، GitHub سيعطيك أوامر. استخدم هذه الأوامر:

```bash
# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: SQL Injection Detection System"

# إضافة remote repository (استبدل YOUR_USERNAME بـ DevAhmad-CS)
git remote add origin https://github.com/DevAhmad-CS/CRP-SQLi.git

# رفع الملفات
git branch -M main
git push -u origin main
```

### 3. إذا طلب منك Authentication

إذا طلب منك GitHub اسم المستخدم وكلمة المرور:

**الطريقة 1: Personal Access Token (موصى بها)**
1. اذهب إلى GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. اضغط "Generate new token"
3. اختر الصلاحيات: `repo` (Full control of private repositories)
4. انسخ الـ token واستخدمه ككلمة مرور عند push

**الطريقة 2: GitHub CLI**
```bash
gh auth login
```

### 4. التحقق من الرفع

اذهب إلى: `https://github.com/DevAhmad-CS/CRP-SQLi`

يجب أن ترى جميع الملفات مرفوعة.

---

## 📝 ملاحظات مهمة

### الملفات التي لن تُرفع (بسبب .gitignore):
- `__pycache__/` - ملفات Python المؤقتة
- `venv/` - البيئة الافتراضية
- `models/*.pkl` - ملفات النماذج (كبيرة)
- `.env` - متغيرات البيئة

### إذا أردت رفع النماذج:
1. احذف `models/*.pkl` من `.gitignore`
2. أو استخدم [Git LFS](https://git-lfs.github.com/) للملفات الكبيرة

---

## 🔗 الخطوة التالية: ربط مع Render

بعد رفع المشروع على GitHub، يمكنك ربطه مع Render:

1. اذهب إلى [Render.com](https://render.com)
2. سجل دخول بحساب GitHub
3. اضغط "New" → "Web Service"
4. اختر الـ repository: `DevAhmad-CS/CRP-SQLi`
5. املأ الإعدادات:
   - **Name**: `sql-injection-detector`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd web_app && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. اضغط "Create Web Service"

---

## ✅ Checklist قبل الرفع

- [x] تم إنشاء `.gitignore`
- [x] تم إنشاء `README.md`
- [x] تم إنشاء `requirements.txt`
- [ ] تم تهيئة Git (`git init`)
- [ ] تم إضافة الملفات (`git add .`)
- [ ] تم عمل Commit (`git commit`)
- [ ] تم إنشاء Repository على GitHub (Private)
- [ ] تم ربط المشروع (`git remote add origin`)
- [ ] تم رفع الملفات (`git push`)

---

## 🆘 حل المشاكل

### مشكلة: "Permission denied"
- تأكد من أن الـ repository موجود على GitHub
- تأكد من استخدام Personal Access Token

### مشكلة: "Large files"
- استخدم Git LFS للملفات الكبيرة
- أو احذف الملفات الكبيرة من `.gitignore`

### مشكلة: "Authentication failed"
- استخدم Personal Access Token بدلاً من كلمة المرور
- أو استخدم GitHub CLI

---

**جاهز للرفع! 🚀**

