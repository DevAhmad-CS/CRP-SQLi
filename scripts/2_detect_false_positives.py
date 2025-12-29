import pandas as pd
import re

print("=" * 80)
print("كشف وإعادة تصنيف False Positives")
print("=" * 80)

# قراءة البيانات
df = pd.read_csv('../dataset/Advanced_Cleaned_Dataset.csv')

print(f"\n📊 البيانات قبل التصحيح:")
print(f"   - عدد السجلات: {len(df):,}")

# قواعد كشف SQL Injection
def is_likely_sqli(query):
    """
    كشف إذا كان الاستعلام يحتوي على SQL Injection
    """
    if pd.isna(query):
        return False
    
    query_str = str(query).lower()
    
    # أنماط SQL Injection واضحة
    sqli_patterns = [
        r"'\s*or\s*['\"]?\s*1\s*=\s*1",  # OR 1=1
        r"'\s*or\s*['\"]?\s*['\"]?\s*=\s*['\"]",  # OR ''='
        r"union\s+select.*version",  # UNION SELECT version
        r"union\s+select.*database\s*\(",  # UNION SELECT database()
        r"union\s+select.*user\s*\(",  # UNION SELECT user()
        r"'\s*;\s*drop",  # '; DROP
        r"'\s*;\s*delete",  # '; DELETE
        r"sleep\s*\(",  # SLEEP(
        r"pg_sleep\s*\(",  # pg_sleep(
        r"waitfor\s+delay",  # WAITFOR DELAY
        r"benchmark\s*\(",  # benchmark(
        r"'\s*--\s*'",  # '--'
        r"'\s*or\s*['\"]?\s*1\s*=\s*1\s*--",  # OR 1=1 --
        r"'\s*or\s*['\"]?\s*1\s*=\s*1\s*#",  # OR 1=1 #
        r"extractvalue\s*\(",  # extractvalue(
        r"updatexml\s*\(",  # updatexml(
        r"exp\s*\(",  # exp(
        r"floor\s*\(",  # floor(
        r"'\s*or\s*['\"]?\s*['\"]?\s*=\s*['\"]\s*--",  # OR ''=''--
        r"'\s*and\s*['\"]?\s*1\s*=\s*1\s*--",  # AND 1=1 --
        r"'\s*and\s*['\"]?\s*['\"]?\s*=\s*['\"]",  # AND ''='
    ]
    
    for pattern in sqli_patterns:
        if re.search(pattern, query_str, re.IGNORECASE):
            return True
    return False

# فحص الاستعلامات الطبيعية (Label = 0)
normal_queries = df[df['Label'] == 0].copy()
print(f"\n🔍 فحص الاستعلامات الطبيعية:")
print(f"   - عدد الاستعلامات الطبيعية: {len(normal_queries):,}")

# كشف False Positives
normal_queries['is_sqli'] = normal_queries['Query'].apply(is_likely_sqli)
false_positives = normal_queries[normal_queries['is_sqli'] == True]

print(f"\n⚠️  False Positives المكتشفة:")
print(f"   - عدد الاستعلامات المشبوهة: {len(false_positives):,}")

# إعادة تصنيف False Positives الواضحة
df_corrected = df.copy()
df_corrected.loc[false_positives.index, 'Label'] = 1

# إحصائيات بعد التصحيح
print(f"\n📈 إحصائيات بعد التصحيح:")
print(f"   - تم إعادة تصنيف: {len(false_positives):,} استعلام من 0 إلى 1")

# توزيع Labels بعد التصحيح
label_counts = df_corrected['Label'].value_counts()
print(f"\n📊 توزيع Labels بعد التصحيح:")
for label, count in label_counts.items():
    percentage = (count / len(df_corrected)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"   - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# حفظ الاستعلامات المشبوهة للمراجعة (عينة من 100)
suspicious_sample = false_positives.sample(n=min(100, len(false_positives)), random_state=42)
suspicious_sample[['Query', 'Label']].to_csv('../review/suspicious_queries_for_review.csv', index=False)
print(f"\n📝 تم حفظ {len(suspicious_sample)} استعلام مشبوه في: ../review/suspicious_queries_for_review.csv")

# حفظ البيانات المصححة
output_file = '../dataset/False_Positives_Corrected_Dataset.csv'
df_corrected.to_csv(output_file, index=False)
print(f"✅ تم حفظ البيانات المصححة في: {output_file}")

print(f"\n{'='*80}")
print("✅ انتهى كشف False Positives!")
print(f"{'='*80}")

