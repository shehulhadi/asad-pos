import re
with open('index.html', 'r') as f: html = f.read()

# 1. Fix the literal text in the HTML modal
html = html.replace(
    '<h3 style="margin-bottom: 4px;">${settings.businessName || \'POS App\'}</h3>',
    '<h3 id="rating-app-title" style="margin-bottom: 4px;">Rate this App</h3>'
)
html = html.replace(
    '<strong>${settings.businessName || \'POS App\'} (v1.0.0)</strong><br>',
    '<strong id="rating-app-footer">App Version 1.0.0</strong><br>'
)

# 2. Fix the JS logic and add a timer variable
old_js = '''    function checkRatingPrompt() {
        if (!localStorage.getItem('asad:rated')) {
            setTimeout(() => {
                if (document.getElementById('login-view').classList.contains('active')) {
                    document.getElementById('rating-modal').classList.add('active');
                }
            }, 3000);
        }
    }'''

new_js = '''    let ratingTimer;

    function checkRatingPrompt() {
        if (!localStorage.getItem('asad:rated')) {
            ratingTimer = setTimeout(() => {
                if (document.getElementById('login-view').classList.contains('active')) {
                    document.getElementById('rating-app-title').textContent = settings.businessName || 'POS App';
                    document.getElementById('rating-app-footer').textContent = (settings.businessName || 'POS App') + ' (v1.0.0)';
                    document.getElementById('rating-modal').classList.add('active');
                }
            }, 3000);
        }
    }'''
html = re.sub(r'    function checkRatingPrompt\(\) \{.*?\n    \}', new_js, html, flags=re.DOTALL)

# 3. Cancel the timer when the user successfully logs in
old_login = '''        localStorage.setItem('asad:auth', currentUser);
        loadApp();'''
new_login = '''        localStorage.setItem('asad:auth', currentUser);
        clearTimeout(ratingTimer);
        document.getElementById('rating-modal').classList.remove('active');
        loadApp();'''
html = html.replace(old_login, new_login)

with open('index.html', 'w') as f: f.write(html)
