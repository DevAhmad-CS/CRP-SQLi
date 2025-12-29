"""
Debug: لماذا 1=1-- لا يظهر في بيانات التدريب
"""

import sys
import codecs

if sys.platform == 'win32':
    try:
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

import pandas as pd
from pathlib import Path

base_dir = Path(__file__).parent.parent
dataset_dir = base_dir / 'dataset' / 'final'

print("=" * 80)
print("Debug: لماذا 1=1-- لا يظهر في بيانات التدريب")
print("=" * 80)

# Read training data
train_df = pd.read_csv(dataset_dir / 'train_final.csv')
print(f"\n1. Training data size: {len(train_df):,}")

# Check if 1=1-- exists
exact = train_df[train_df['Query'] == '1=1--']
print(f"2. Exact match '1=1--': {len(exact)}")

# Check all queries that contain 1=1--
contains = train_df[train_df['Query'].str.contains('1=1--', case=False, na=False)]
print(f"3. Contains '1=1--': {len(contains)}")

# Check what happens when we add it
test_query = "1=1--"
test_df = pd.DataFrame({'Query': [test_query], 'Label': [1]})
combined = pd.concat([train_df, test_df], ignore_index=True)

print(f"\n4. After adding '1=1--': {len(combined):,}")

# Check duplicates
duplicates = combined[combined.duplicated(subset=['Query'], keep=False)]
print(f"5. Duplicates in combined: {len(duplicates)}")

if len(duplicates) > 0:
    print(f"\n   Duplicate queries:")
    for query in duplicates['Query'].unique()[:10]:
        count = len(duplicates[duplicates['Query'] == query])
        print(f"   - '{query}': {count} times")

# After drop_duplicates
after_drop = combined.drop_duplicates(subset=['Query'], keep='first')
print(f"\n6. After drop_duplicates: {len(after_drop):,}")

# Check if 1=1-- still exists
still_exists = after_drop[after_drop['Query'] == '1=1--']
print(f"7. '1=1--' still exists after drop_duplicates: {len(still_exists)}")

if len(still_exists) > 0:
    print(f"   ✅ Found! Label: {still_exists.iloc[0]['Label']}")
else:
    print(f"   ❌ Not found! It was removed by drop_duplicates")

print("\n" + "=" * 80)

