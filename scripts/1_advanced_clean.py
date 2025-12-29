import pandas as pd
import re
import os

print("=" * 80)
print("التنظيف المتقدم للـ Dataset")
print("=" * 80)

# قراءة البيانات الأصلية
input_file = '../dataset/original/Modified_SQL_Dataset.csv'
df = pd.read_csv(input_file)

print(f"\n📊 البيانات قبل التنظيف المتقدم:")
print(f"   - عدد السجلات: {len(df):,}")

initial_count = len(df)

# 1. إزالة الاستعلامات الطويلة جداً (>5000 حرف)
df = df[df['Query'].str.len() <= 5000].copy()
removed_long = initial_count - len(df)
print(f"\n1️⃣  بعد إزالة الاستعلامات الطويلة جداً (>5000 حرف): {len(df):,} ({removed_long} تمت إزالتها)")

# 2. تنظيف المسافات الزائدة
df['Query'] = df['Query'].str.replace(r'\s+', ' ', regex=True)  # مسافات متعددة إلى واحدة
df['Query'] = df['Query'].str.strip()  # إزالة المسافات من البداية والنهاية

# 3. إزالة الاستعلامات التي تحتوي على رموز فقط (بدون حروف أو أرقام)
df = df[df['Query'].str.contains(r'[a-zA-Z0-9]', regex=True, na=False)].copy()
print(f"2️⃣  بعد إزالة الاستعلامات التي تحتوي على رموز فقط: {len(df):,}")

# 4. إزالة الأحرف غير القابلة للطباعة (مثل \x00, \x01, إلخ)
def remove_non_printable(text):
    if pd.isna(text):
        return text
    # إزالة الأحرف غير القابلة للطباعة (باستثناء المسافات والتبويبات)
    return ''.join(char for char in str(text) if char.isprintable() or char in ['\n', '\t', '\r'])

df['Query'] = df['Query'].apply(remove_non_printable)
df = df[df['Query'].str.len() > 0].copy()
print(f"3️⃣  بعد إزالة الأحرف غير القابلة للطباعة: {len(df):,}")

# 5. إزالة الاستعلامات الفارغة بعد التنظيف
df = df[df['Query'].str.strip().str.len() > 0].copy()
print(f"4️⃣  بعد إزالة الاستعلامات الفارغة: {len(df):,}")

# إحصائيات
final_count = len(df)
removed_total = initial_count - final_count

print(f"\n📈 إحصائيات التنظيف المتقدم:")
print(f"   - السجلات الأصلية: {initial_count:,}")
print(f"   - السجلات بعد التنظيف: {final_count:,}")
print(f"   - تمت إزالة: {removed_total:,} سجل ({removed_total/initial_count*100:.2f}%)")

# توزيع Labels بعد التنظيف
label_counts = df['Label'].value_counts()
print(f"\n📊 توزيع Labels بعد التنظيف المتقدم:")
for label, count in label_counts.items():
    percentage = (count / len(df)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"   - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# حفظ البيانات المنظفة
output_file = '../dataset/Advanced_Cleaned_Dataset.csv'
df.to_csv(output_file, index=False)
print(f"\n✅ تم حفظ البيانات المنظفة في: {output_file}")

print(f"\n{'='*80}")
print("✅ انتهى التنظيف المتقدم!")
print(f"{'='*80}")

