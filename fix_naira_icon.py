import re
with open('app.js', 'r') as f: js = f.read()

# Replace the mirrored Naira path with the correct one
old_path = '''sales: '<path d="M7 5v14M17 5v14M5 10h14M5 14h14M9 19l6-14"/>','''
new_path = '''sales: '<path d="M8 5v14M16 5v14M8 5l8 14M5 9h14M5 14h14"/>','''

if old_path in js:
    js = js.replace(old_path, new_path)
else:
    # Fallback regex just in case
    js = re.sub(r"sales: '<path d=\"M7 5v14.*?</svg>'", "sales: '<path d=\"M8 5v14M16 5v14M8 5l8 14M5 9h14M5 14h14\"/>',", js)

with open('app.js', 'w') as f: f.write(js)
print("Naira icon corrected.")
