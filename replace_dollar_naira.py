import re

# 1. Process app.js safely
with open('app.js', 'r') as f: js = f.read()
# Replace $ with ₦, EXCEPT when it's part of a JS template literal ${
js = re.sub(r'\$(?!\{)', '₦', js)
with open('app.js', 'w') as f: f.write(js)

# 2. Process index.html safely
with open('index.html', 'r') as f: html = f.read()
html = re.sub(r'\$(?!\{)', '₦', html)
with open('index.html', 'w') as f: f.write(html)

# 3. Process style.css safely
with open('style.css', 'r') as f: css = f.read()
css = re.sub(r'\$(?!\{)', '₦', css)
with open('style.css', 'w') as f: f.write(css)

print("Dollar signs successfully replaced with Naira symbols.")
