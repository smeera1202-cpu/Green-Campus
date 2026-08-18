import re
import json

with open('database.py', 'r', encoding='utf-8') as f:
    db_text = f.read()

print("--- PLANTS IN DATABASE.PY ---")
plant_matches = re.findall(r"\('P-\d+.*?\)", db_text, re.DOTALL)
for p in plant_matches:
    print(p)

print("\n--- BIODIVERSITY LOGS IN DATABASE.PY ---")
bio_matches = re.findall(r"\('(?:Golden|Asian|Purple|Peacock|Tulsi).*?\)", db_text, re.DOTALL)
for b in bio_matches:
    print(b)
