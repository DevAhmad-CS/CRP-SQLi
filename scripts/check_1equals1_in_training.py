"""
فحص إذا كان 1=1-- موجود في بيانات التدريب
"""

import sys
import codecs

# Fix encoding for Windows console
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
print("فحص وجود 1=1-- في بيانات التدريب")
print("=" * 80)

train_df = pd.read_csv(dataset_dir / 'train_final.csv')

# Search for exact matches
exact_matches = train_df[train_df['Query'] == '1=1--']
print(f"\n1. Exact match '1=1--': {len(exact_matches)}")

if len(exact_matches) > 0:
    for idx, row in exact_matches.iterrows():
        print(f"   - Label {row['Label']}: {row['Query']}")

# Search for similar patterns
similar = train_df[train_df['Query'].str.contains('1=1--', case=False, na=False)]
print(f"\n2. Contains '1=1--': {len(similar)}")

if len(similar) > 0:
    print(f"   Examples:")
    for idx, row in similar.head(10).iterrows():
        print(f"   - Label {row['Label']}: {row['Query'][:70]}...")

# Check short patterns
short_patterns = ['1=1--', '1=1', '1=1#', '1=2--']
print(f"\n3. Checking short patterns:")
for pattern in short_patterns:
    matches = train_df[train_df['Query'] == pattern]
    print(f"   - '{pattern}': {len(matches)} matches (Labels: {matches['Label'].tolist() if len(matches) > 0 else 'None'})")

print("\n" + "=" * 80)

