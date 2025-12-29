# 📋 تعليمات رفع المشروع على GitHub

## ✅ الخطوات المطلوبة

### 1️⃣ إنشاء Repository على GitHub

1. اذهب إلى: https://github.com/new
2. املأ البيانات:
   - **Repository name**: `CRP-SQLi`
   - **Description**: `SQL Injection Detection System using Machine Learning`
   - **Visibility**: ✅ **Private** (مهم!)
   - **لا** تضع علامة على "Add a README file"
3. اضغط **"Create repository"**

### 2️⃣ ربط المشروع ورفعه

بعد إنشاء الـ repository، نفذ هذه الأوامر في Terminal:

```bash
# إضافة جميع الملفات
git add .

# عمل commit
git commit -m "Initial commit: SQL Injection Detection System"

# إضافة remote (استبدل YOUR_REPO_NAME إذا كان مختلف)
git remote add origin https://github.com/DevAhmad-CS/CRP-SQLi.git

# رفع الملفات
git branch -M main
git push -u origin main
```

### 3️⃣ Authentication

عند الـ push، GitHub سيطلب:
- **Username**: `DevAhmad-CS`
- **Password**: استخدم **Personal Access Token** (ليس كلمة المرور!)

#### كيفية إنشاء Personal Access Token:
1. اذهب إلى: https://github.com/settings/tokens
2. اضغط **"Generate new token"** → **"Generate new token (classic)"**
3. املأ:
   - **Note**: `CRP-SQLi Project`
   - **Expiration**: اختر المدة
   - **Select scopes**: ✅ `repo` (Full control of private repositories)
4. اضغط **"Generate token"**
5. **انسخ الـ token** (لن يظهر مرة أخرى!)
6. استخدمه ككلمة مرور عند push

---

## 🔗 الخطوة التالية: Render

بعد رفع المشروع، لربطه مع Render:

1. اذهب إلى: https://render.com
2. سجل دخول بحساب GitHub
3. اضغط **"New"** → **"Web Service"**
4. اختر الـ repository: `DevAhmad-CS/CRP-SQLi`
5. املأ الإعدادات:
   - **Name**: `sql-injection-detector`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd web_app && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. اضغط **"Create Web Service"**

---

## 📝 ملاحظات

- ✅ Repository سيكون **Private**
- ✅ Email: `ahmadmahmouddev@gmail.com`
- ✅ GitHub Username: `DevAhmad-CS`
- ✅ Models (`.pkl` files) لن تُرفع (كبيرة جداً)

---

**جاهز! 🚀**

