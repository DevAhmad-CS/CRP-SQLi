import pandas as pd
from sklearn.model_selection import train_test_split

print("=" * 80)
print("التقسيم النهائي للـ Dataset")
print("=" * 80)

# قراءة البيانات المتوازنة
df = pd.read_csv('../dataset/Balanced_Dataset.csv')

print(f"\n📊 البيانات قبل التقسيم:")
print(f"   - إجمالي السجلات: {len(df):,}")

label_counts = df['Label'].value_counts()
for label, count in label_counts.items():
    percentage = (count / len(df)) * 100
    label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
    print(f"   - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")

# تقسيم البيانات: 70% Train, 30% للبقية
train_df, temp_df = train_test_split(
    df, 
    test_size=0.3, 
    random_state=42, 
    stratify=df['Label']  # الحفاظ على التوازن
)

# تقسيم الـ 30% إلى 15% Validation و 15% Test
val_df, test_df = train_test_split(
    temp_df, 
    test_size=0.5, 
    random_state=42, 
    stratify=temp_df['Label']
)

print(f"\n📈 توزيع البيانات بعد التقسيم:")
print(f"   - Train: {len(train_df):,} ({len(train_df)/len(df)*100:.2f}%)")
print(f"   - Validation: {len(val_df):,} ({len(val_df)/len(df)*100:.2f}%)")
print(f"   - Test: {len(test_df):,} ({len(test_df)/len(df)*100:.2f}%)")

# التحقق من التوازن في كل قسم
print(f"\n⚖️  التوازن في كل قسم:")

for name, data in [("Train", train_df), ("Validation", val_df), ("Test", test_df)]:
    label_counts = data['Label'].value_counts()
    print(f"\n   {name}:")
    for label, count in label_counts.items():
        percentage = (count / len(data)) * 100
        label_name = "SQL Injection" if label == 1 else "استعلام طبيعي"
        print(f"      - Label {label} ({label_name}): {count:,} ({percentage:.2f}%)")
    
    balance_ratio = min(label_counts) / max(label_counts)
    print(f"      نسبة التوازن: {balance_ratio:.4f}")

# حفظ الأقسام
train_df.to_csv('../dataset/final/train_final.csv', index=False)
val_df.to_csv('../dataset/final/validation_final.csv', index=False)
test_df.to_csv('../dataset/final/test_final.csv', index=False)

print(f"\n✅ تم حفظ الأقسام في:")
print(f"   - dataset/final/train_final.csv")
print(f"   - dataset/final/validation_final.csv")
print(f"   - dataset/final/test_final.csv")

print(f"\n{'='*80}")
print("✅ انتهى التقسيم النهائي!")
print(f"{'='*80}")

