"""
تحليل الاستعلامات الجديدة وتقييمها
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

# الاستعلامات من المستخدم
normal_queries = [
    "SELECT * FROM users WHERE id = 1",
    "SELECT * FROM users WHERE id = 2",
    "SELECT name FROM products WHERE price > 50",
    "SELECT name,price FROM products WHERE category='phones'",
    "SELECT * FROM orders WHERE user_id = 10",
    "SELECT * FROM orders WHERE status='shipped'",
    "SELECT COUNT(*) FROM users",
    "SELECT COUNT(*) FROM users WHERE active=1",
    "SELECT * FROM employees WHERE department='IT'",
    "SELECT * FROM employees WHERE salary > 700",
    "SELECT * FROM students WHERE grade >= 90",
    "SELECT * FROM students WHERE grade BETWEEN 70 AND 90",
    "SELECT id,username FROM users WHERE status='active'",
    "SELECT id,email FROM users WHERE verified=1",
    "SELECT * FROM logs WHERE created_at > NOW() - INTERVAL 1 DAY",
    "SELECT * FROM logs WHERE level='error'",
    "SELECT * FROM payments WHERE status IN ('paid','pending')",
    "SELECT * FROM payments WHERE amount > 100",
    "SELECT * FROM products WHERE category='phones' OR category='laptops'",
    "SELECT * FROM products WHERE stock > 0 AND active=1",
    "SELECT SUM(total) FROM sales WHERE year=2024",
    "SELECT AVG(price) FROM products",
    "SELECT * FROM users WHERE email = ?",  # Parameterized - NEW!
    "SELECT * FROM users WHERE username = ?",  # Parameterized - NEW!
    "SELECT * FROM sessions WHERE expires_at > NOW()",
    "SELECT * FROM sessions WHERE user_id=5",
    "SELECT * FROM reviews WHERE rating >= 4",
    "SELECT * FROM reviews WHERE product_id=3",
    "SELECT * FROM users ORDER BY created_at DESC LIMIT 5",
    "SELECT * FROM users ORDER BY username ASC",
    "SELECT department,COUNT(*) FROM employees GROUP BY department",
    "SELECT role,COUNT(*) FROM users GROUP BY role",
    "SELECT * FROM users WHERE username LIKE 'a%'",
    "SELECT * FROM users WHERE email LIKE '%@gmail.com'",
    "SELECT * FROM products WHERE price BETWEEN 10 AND 100",
    "SELECT * FROM orders WHERE total BETWEEN 50 AND 200",
    "SELECT * FROM users WHERE role='admin' AND enabled=1",
    "SELECT * FROM users WHERE enabled=0",
    "SELECT * FROM orders WHERE created_at >= '2024-01-01'",
    "SELECT * FROM orders WHERE created_at <= '2024-12-31'",
    "SELECT * FROM users WHERE id IN (1,2,3)",
    "SELECT * FROM products WHERE id IN (5,6,7)",
    "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE active=1)",
    "SELECT * FROM employees WHERE department IN ('IT','HR')",
    "SELECT * FROM users WHERE last_login IS NOT NULL",
    "SELECT * FROM users WHERE phone IS NULL",
    "SELECT DISTINCT category FROM products",
    "SELECT DISTINCT country FROM users",
    "SELECT * FROM users LIMIT 10 OFFSET 20",
    "SELECT * FROM products LIMIT 5",
    "SELECT MAX(price) FROM products",
    "SELECT MIN(salary) FROM employees",
    "SELECT * FROM users WHERE id = 1 OR id = 2",  # Legitimate OR
    "SELECT * FROM users WHERE (id=1 OR id=2) AND active=1",
    "SELECT * FROM products WHERE (price > 50 AND stock > 0)",
    "SELECT * FROM orders WHERE status='paid' OR status='pending'",
    "SELECT * FROM users WHERE LENGTH(username) > 5",
    "SELECT * FROM users WHERE CHAR_LENGTH(email) > 10",
]

sqli_queries = [
    "SELECT * FROM users WHERE id = 1 OR 1=1--",
    "SELECT * FROM users WHERE username='admin' OR '1'='1'",
    "SELECT * FROM users WHERE id = 5 UNION SELECT username,password FROM users--",
    "SELECT * FROM users WHERE id=1 AND SLEEP(5)",
    "SELECT * FROM users WHERE username='admin'/**/OR/**/'x'='x'",
    "SELECT * FROM users WHERE id=1 AND BENCHMARK(5000000,MD5(1))",  # BENCHMARK - NEW!
    "SELECT * FROM users WHERE username=CHAR(97,100,109,105,110)",  # CHAR() - NEW!
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT * FROM users)",
    "SELECT * FROM users WHERE id=1; DROP TABLE users--",
    "SELECT * FROM users WHERE username='admin' OR ''=''",
    "SELECT * FROM users WHERE id=(SELECT id FROM users LIMIT 1) OR 1=1",
    "SELECT * FROM users WHERE id=1 OR TRUE",
    "SELECT * FROM users WHERE username='admin' OR 1 LIKE 1",
    "SELECT * FROM users WHERE id=1 AND (SELECT COUNT(*) FROM users)>0",
    "SELECT * FROM users WHERE id=1 OR 9999=9999",
    "SELECT * FROM users WHERE username='admin' OR 'a'='a'#",
    "SELECT * FROM users WHERE id=1 UNION SELECT NULL,NULL--",
    "SELECT * FROM users WHERE id=1 AND IF(1=1,SLEEP(3),0)",  # IF() - NEW!
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT 1)",
    "SELECT * FROM users WHERE username='admin' OR 1=1/*comment*/",
    "SELECT * FROM products WHERE id=10 OR 1=1",
    "SELECT * FROM orders WHERE user_id=5 OR 'x'='x'",
    "SELECT * FROM users WHERE email='test@test.com' OR '1'='1'",
    "SELECT * FROM users WHERE id=1 AND 1=1--",
    "SELECT * FROM users WHERE id=1 AND 1=2 OR 1=1",
    "SELECT * FROM users WHERE username='admin' OR username LIKE '%'",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT username FROM users)",
    "SELECT * FROM users WHERE id=1 AND SLEEP(2)",
    "SELECT * FROM users WHERE id=1 AND IF(2>1,SLEEP(4),0)",  # IF() - NEW!
    "SELECT * FROM users WHERE id=1 OR (SELECT 1)",
    "SELECT * FROM users WHERE id=1 UNION SELECT username,email FROM users--",
    "SELECT * FROM users WHERE id=1 UNION ALL SELECT NULL,NULL--",
    "SELECT * FROM users WHERE id=1 AND (SELECT LENGTH(password) FROM users LIMIT 1)>0",
    "SELECT * FROM users WHERE id=1 OR id IN (SELECT id FROM users)",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT COUNT(*) FROM users)",
    "SELECT * FROM users WHERE id=1 AND 999=999",
    "SELECT * FROM users WHERE username='admin' OR 2>1",
    "SELECT * FROM users WHERE id=1 OR 'abc'='abc'",
    "SELECT * FROM users WHERE id=1 OR 'a' LIKE 'a'",
    "SELECT * FROM users WHERE id=1 OR 5 BETWEEN 1 AND 10",
    "SELECT * FROM users WHERE id=1 AND (SELECT SLEEP(1))",
    "SELECT * FROM users WHERE id=1 OR EXISTS(SELECT SLEEP(1))",
]

print("=" * 80)
print("تحليل الاستعلامات الجديدة")
print("=" * 80)

# تحليل Normal Queries
print("\n📊 تحليل Normal Queries (150):")
print(f"   - إجمالي: {len(normal_queries)}")

# فحص Parameterized queries
param_queries = [q for q in normal_queries if '?' in q]
print(f"\n   ✅ Parameterized Queries (جديد!): {len(param_queries)}")
for q in param_queries:
    print(f"      - {q}")

# فحص Legitimate OR
legit_or = [q for q in normal_queries if ' OR ' in q.upper() and '1=1' not in q and 'OR 1=1' not in q.upper()]
print(f"\n   ✅ Legitimate OR (مهم!): {len(legit_or)}")
for q in legit_or[:5]:  # أول 5 فقط
    print(f"      - {q}")

# تحليل SQL Injection Queries
print("\n📊 تحليل SQL Injection Queries (150):")
print(f"   - إجمالي: {len(sqli_queries)}")

# فحص BENCHMARK
benchmark_queries = [q for q in sqli_queries if 'BENCHMARK' in q.upper()]
print(f"\n   ⚠️  BENCHMARK (جديد!): {len(benchmark_queries)}")
for q in benchmark_queries:
    print(f"      - {q}")

# فحص CHAR()
char_queries = [q for q in sqli_queries if 'CHAR(' in q.upper()]
print(f"\n   ⚠️  CHAR() encoding (جديد!): {len(char_queries)}")
for q in char_queries:
    print(f"      - {q}")

# فحص IF()
if_queries = [q for q in sqli_queries if 'IF(' in q.upper()]
print(f"\n   ⚠️  IF() statements (جديد!): {len(if_queries)}")
for q in if_queries:
    print(f"      - {q}")

# فحص EXISTS variations
exists_queries = [q for q in sqli_queries if 'EXISTS(' in q.upper()]
print(f"\n   ✅ EXISTS subqueries: {len(exists_queries)}")
print(f"      - بعضها موجود، بعضها جديد")

# فحص LIKE in SQLi context
like_sqli = [q for q in sqli_queries if 'LIKE' in q.upper() and ('OR' in q.upper() or 'AND' in q.upper())]
print(f"\n   ✅ LIKE in SQLi context: {len(like_sqli)}")

print("\n" + "=" * 80)
print("التوصيات:")
print("=" * 80)

print("\n✅ يجب إضافة:")
print("   1. Parameterized queries (?) - مهم جداً!")
print("   2. BENCHMARK() - نمط جديد")
print("   3. CHAR() encoding - نمط جديد")
print("   4. IF() statements - نمط جديد")
print("   5. Legitimate OR queries - مهم للتمييز")

print("\n⚠️  يجب مراجعة:")
print("   1. بعض EXISTS variations - قد تكون مكررة")
print("   2. بعض OR 1=1 variations - قد تكون مكررة")

print("\n❌ لا حاجة لإضافة:")
print("   1. الاستعلامات المكررة تماماً")
print("   2. الاستعلامات المشابهة جداً للموجودة")

