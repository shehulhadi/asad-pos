import re
with open('index.html', 'r') as f: html = f.read()

# 1. Remove the Setup View HTML block
start_idx = html.find('<div id="setup-view" class="view">')
end_idx = html.find('<div id="app-view" class="view">')
if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + html[end_idx:]

# 2. Remove the Setup Logic functions
html = re.sub(r'    function checkFirstTime\(\) \{.*?\n    \}', '', html, flags=re.DOTALL)
html = re.sub(r'    function createAccount\(\) \{.*?\n    \}', '', html, flags=re.DOTALL)

# 3. Revert initialization back to restoreSession()
html = html.replace('checkFirstTime();\n</script>', 'restoreSession();\n</script>')

# 4. Remove the Setup CSS additions to clean up
html = html.replace('/* ---------- Setup View ---------- */', '')
html = html.replace('#setup-view input { letter-spacing: normal !important; text-indent: 0 !important; font-size: 16px !important; text-align: left !important; padding: 12px 14px !important; }\n        #setup-view .login-card { text-align: left; }\n        #setup-view .brand-mark, #setup-view h1, #setup-view .sub { text-align: center; margin-left: auto; margin-right: auto; }', '')

with open('index.html', 'w') as f: f.write(html)
