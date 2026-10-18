import re
with open('index.html', 'r') as f: html = f.read()

# Fix the login-view CSS to remove the huge top gap
html = html.replace(
    '.login-card { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; max-width: 340px; height: 100%; }',
    '.login-card { display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; max-width: 340px; }'
)

# Change the subtitle to be universal
html = html.replace(
    '<div class="sub" id="login-sub-text" style="font-size: 13px; font-weight: 500; color: #94a3b8; letter-spacing: 0.5px; margin-top: 8px;">Business Management Portal</div>',
    '<div class="sub" id="login-sub-text" style="font-size: 13px; font-weight: 500; color: #94a3b8; letter-spacing: 0.5px; margin-top: 8px;">BUSINESS & INVENTORY MANAGER</div>'
)

# Ensure the dynamic JS text sets the new subtitle
html = html.replace(
    "document.getElementById('login-sub-text').textContent = \"Block Production & POS Manager\";",
    "document.getElementById('login-sub-text').textContent = \"BUSINESS & INVENTORY MANAGER\";"
)

# Add a margin-top to the top wrapper to balance the absolute bottom button
html = html.replace(
    '<div style="text-align: center; margin-bottom: 40px; margin-top: 40px;">',
    '<div style="text-align: center; margin-bottom: 40px;">'
)

with open('index.html', 'w') as f: f.write(html)
