import pandas as pd
import random
import re

print("=" * 80)
print("إعادة توازن Dataset")
print("=" * 80)

# قراءة البيانات
df = pd.read_csv('../dataset/False_Positives_Corrected_Dataset.csv')

# قراءة الأنماط الجديدة
try:
    new_patterns_df = pd.read_csv('../dataset/New_SQLi_Patterns.csv')
    df = pd.concat([df, new_patterns_df], ignore_index=True)
    print(f"\n✅ تم دمج الأنماط الجديدة ({len(new_patterns_df)} سجل)")
except:
    print("\n⚠️  لم يتم العثور على ملف الأنماط الجديدة")

print(f"\n📊 البيانات قبل إعادة التوازن:")
print(f"   - عدد السجلات: {len(df):,}")

label_counts = df['Label'].value_counts()
for label, count in label_counts.items():
    percentage = (count / len(df)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"   - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# Data Augmentation للـ SQL Injection
def augment_sqli(query):
    """زيادة تنوع استعلامات SQL Injection"""
    if pd.isna(query):
        return query
    
    query_str = str(query)
    augmented = []
    
    # 1. إضافة مسافات عشوائية
    if random.random() < 0.3:
        query_str = re.sub(r'(\w)(\w)', r'\1 \2', query_str, count=random.randint(1, 3))
    
    # 2. تغيير حالة الأحرف
    if random.random() < 0.3:
        words = query_str.split()
        for i in range(min(2, len(words))):
            idx = random.randint(0, len(words)-1)
            if words[idx].isalpha():
                words[idx] = words[idx].upper() if random.random() < 0.5 else words[idx].lower()
        query_str = ' '.join(words)
    
    # 3. إضافة تعليقات SQL
    if random.random() < 0.2:
        if '--' not in query_str:
            query_str = query_str + ' /**/'
        elif '/*' not in query_str:
            query_str = query_str.replace('--', '--/**/')
    
    # 4. تغيير ترتيب الكلمات (في حالات بسيطة)
    if random.random() < 0.1:
        if 'OR 1=1' in query_str:
            query_str = query_str.replace('OR 1=1', '1=1 OR')
        if 'AND 1=1' in query_str:
            query_str = query_str.replace('AND 1=1', '1=1 AND')
    
    return query_str

# إعادة التوازن
sqli_queries = df[df['Label'] == 1].copy()
normal_queries = df[df['Label'] == 0].copy()

print(f"\n🔄 بدء إعادة التوازن...")

# الهدف: 50/50 أو 60/40
target_normal = len(sqli_queries) * 1.2  # 60% طبيعي، 40% SQL Injection
target_normal = int(target_normal)

if len(normal_queries) > target_normal:
    # Undersampling للاستعلامات الطبيعية
    normal_queries = normal_queries.sample(n=target_normal, random_state=42)
    print(f"   ✅ تم تقليل الاستعلامات الطبيعية إلى: {len(normal_queries):,}")
else:
    # Data Augmentation لـ SQL Injection
    needed = int(target_normal * 0.4) - len(sqli_queries)
    if needed > 0:
        print(f"   🔄 توليد {needed} استعلام SQL Injection إضافي...")
        augmented_queries = []
        for _ in range(needed):
            base_query = sqli_queries.sample(n=1, random_state=None).iloc[0]['Query']
            augmented = augment_sqli(base_query)
            augmented_queries.append(augmented)
        
        augmented_df = pd.DataFrame({
            'Query': augmented_queries,
            'Label': [1] * len(augmented_queries)
        })
        sqli_queries = pd.concat([sqli_queries, augmented_df], ignore_index=True)
        print(f"   ✅ تم توليد {needed} استعلام إضافي")

# دمج البيانات المتوازنة
balanced_df = pd.concat([normal_queries, sqli_queries], ignore_index=True)
balanced_df = balanced_df.sample(frac=1, random_state=42).reset_index(drop=True)  # خلط عشوائي

print(f"\n📊 البيانات بعد إعادة التوازن:")
print(f"   - عدد السجلات: {len(balanced_df):,}")

label_counts = balanced_df['Label'].value_counts()
for label, count in label_counts.items():
    percentage = (count / len(balanced_df)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"   - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")

balance_ratio = min(label_counts) / max(label_counts)
print(f"\n⚖️  نسبة التوازن: {balance_ratio:.4f} ({balance_ratio*100:.2f}%)")

if balance_ratio > 0.8:
    print("   ✅ Dataset متوازن بشكل ممتاز!")
elif balance_ratio > 0.6:
    print("   ✅ Dataset متوازن بشكل جيد!")
else:
    print("   ⚠️  Dataset لا يزال يحتاج إلى تحسين")

# حفظ البيانات المتوازنة
output_file = '../dataset/Balanced_Dataset.csv'
balanced_df.to_csv(output_file, index=False)
print(f"\n✅ تم حفظ البيانات المتوازنة في: {output_file}")

print(f"\n{'='*80}")
print("✅ انتهى إعادة التوازن!")
print(f"{'='*80}")

