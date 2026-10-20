import re
with open('app.js', 'r') as f: js = f.read()

# Replace the sales icon SVG path with a Naira symbol path
old_icon = '''sales: '<circle cx="12" cy="12" r="9"/><path d="M14.5 9.5c-.5-1-1.5-1.5-2.5-1.5-1.5 0-2.5.8-2.5 2s1 1.7 2.5 2 2.5.8 2.5 2-1 2-2.5 2c-1 0-2-.5-2.5-1.5M12 6v2m0 8v2"/>','''
new_icon = '''sales: '<path d="M7 5v14M17 5v14M5 10h14M5 14h14M9 19l6-14"/>','''

if old_icon in js:
    js = js.replace(old_icon, new_icon)
else:
    # Fallback regex if string formatting was slightly different
    js = re.sub(r"sales: '<circle cx=\"12\" cy=\"12\" r=\"9\"/>.*?</svg>'", "sales: '<path d=\"M7 5v14M17 5v14M5 10h14M5 14h14M9 19l6-14\"/>',", js)

with open('app.js', 'w') as f: f.write(js)
print("Sales icon replaced with Naira symbol.")
