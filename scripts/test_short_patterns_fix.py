"""
اختبار Rule-based للأنماط القصيرة
"""

import sys
import os
import re

# Fix encoding for Windows console
if sys.platform == 'win32':
    try:
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

# Short SQL Injection patterns (same as in main.py)
SHORT_SQLI_PATTERNS = [
    r'^1=1--?\s*$',           # 1=1-- or 1=1-
    r'^1=1#\s*$',              # 1=1#
    r'^1=1/\*',                # 1=1/*
    r'^1=2--?\s*$',            # 1=2-- or 1=2-
    r'^1=2#\s*$',              # 1=2#
    r"^'1'='1'--?\s*$",        # '1'='1'--
    r"^'1'='1'#\s*$",          # '1'='1'#
    r"^'1'='2'--?\s*$",        # '1'='2'--
    r'^1=1\s*$',               # 1=1
    r'^1=2\s*$',               # 1=2
    r"^'1'='1'\s*$",           # '1'='1'
    r"^'1'='2'\s*$",           # '1'='2'
]

def is_short_sqli_pattern(query: str) -> bool:
    """Check if query is a short SQL Injection pattern"""
    if not query or len(query.strip()) > 15:
        return False
    
    query_stripped = query.strip()
    
    for pattern in SHORT_SQLI_PATTERNS:
        if re.match(pattern, query_stripped, re.IGNORECASE):
            return True
    
    return False

print("=" * 80)
print("اختبار Rule-based للأنماط القصيرة")
print("=" * 80)

test_queries = [
    ("1=1--", True, "Short pattern"),
    ("1=1", True, "Short pattern"),
    ("1=1#", True, "Short pattern"),
    ("1=2--", True, "Short pattern"),
    ("'1'='1'--", True, "Short pattern"),
    ("SELECT * FROM users WHERE id = 1", False, "Normal query"),
    ("SELECT * FROM users WHERE id = 1 OR 1=1--", False, "Long query (use ML)"),
    ("1' OR 1=1--", False, "Long query (use ML)"),
]

print("\nTesting queries:")
all_correct = True
for query, expected, description in test_queries:
    result = is_short_sqli_pattern(query)
    status = "✅" if result == expected else "❌"
    if result != expected:
        all_correct = False
    
    print(f"\n   {status} '{query}'")
    print(f"      -> Detected as short pattern: {result}")
    print(f"      -> Expected: {expected}")
    print(f"      -> {description}")

print("\n" + "=" * 80)
if all_correct:
    print("[SUCCESS] All tests passed!")
else:
    print("[WARNING] Some tests failed!")
print("=" * 80)

