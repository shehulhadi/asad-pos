with open('index.html', 'r') as f: html = f.read()

# 1. Add IDs to the login page elements
html = html.replace(
    '<div class="brand-mark">AJ</div>\n            <h1>A. Jibrialla</h1>\n            <div class="sub">Construction Ltd.</div>',
    '<div class="brand-mark" id="login-logo">AJ</div>\n            <h1 id="login-title-text">A. Jibrialla</h1>\n            <div class="sub" id="login-sub-text">Construction Ltd.</div>'
)

# 2. Add logic to update these elements on startup
old_init = '''    // Update title on initial load
    document.title = settings.businessName || 'POS App';
    document.getElementById('app-title').textContent = settings.businessName || 'POS App';'''

new_init = '''    // Update title on initial load
    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    document.getElementById('app-title').textContent = bizName;
    
    // Update Login Page texts
    if(document.getElementById('login-title-text')) {
        document.getElementById('login-title-text').textContent = bizName;
        document.getElementById('login-sub-text').textContent = 'Management Portal';
        // Generate dynamic logo initials (e.g. "Asad Tech" -> "AT")
        const initials = bizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        document.getElementById('login-logo').textContent = initials;
    }'''
html = html.replace(old_init, new_init)

# 3. Update it in loadApp as well (just in case)
old_load = '''        // Update App Titles dynamically
        document.title = settings.businessName || 'POS App';
        document.getElementById('app-title').textContent = settings.businessName || 'POS App';'''
new_load = '''        // Update App Titles dynamically
        const bizName = settings.businessName || 'My Business';
        document.title = bizName;
        document.getElementById('app-title').textContent = bizName;'''
html = html.replace(old_load, new_load)

with open('index.html', 'w') as f: f.write(html)
