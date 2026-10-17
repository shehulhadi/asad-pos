import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add specific CSS for the Setup view
css_addition = '''
        /* ---------- Setup View ---------- */
        #setup-view { justify-content: center; align-items: center; padding: 24px; background: var(--ink); color: #fff; display: none; flex: 1; flex-direction: column; }
        #setup-view.active { display: flex; }
        #setup-view .login-card { width: 100%; max-width: 340px; text-align: left; }
        #setup-view h1, #setup-view .sub { text-align: center; }
        #setup-view input { background: rgba(255,255,255,.06) !important; border-color: rgba(255,255,255,.14) !important; color: #fff !important; }
        #setup-view label { color: #94a3b8 !important; }
        #setup-view input:focus { border-color: var(--brand) !important; box-shadow: 0 0 0 4px rgba(16,185,129,.2) !important; }
'''
html = html.replace('/* ---------- Shell ---------- */', css_addition + '\n        /* ---------- Shell ---------- */')

# 2. Replace the broken setup-view HTML
new_setup_html = '''    <div id="setup-view" class="view">
        <div class="login-card">
            <div style="text-align: center;">
                <div class="brand-mark">AJ</div>
                <h1>Setup Account</h1>
                <div class="sub">Create your business profile</div>
            </div>
            <div class="form-group">
                <label>Business Name</label>
                <input type="text" id="setup-biz" placeholder="e.g. A. Jibrialla Construction">
            </div>
            <div class="row">
                <div class="form-group">
                    <label>Owner PIN (4 digits)</label>
                    <input type="password" id="setup-owner" maxlength="4" placeholder="••••">
                </div>
                <div class="form-group">
                    <label>Staff PIN (4 digits)</label>
                    <input type="password" id="setup-staff" maxlength="4" placeholder="••••">
                </div>
            </div>
            <button class="btn-primary" onclick="createAccount()" style="margin-top: 10px;">Create Account</button>
        </div>
    </div>'''

html = re.sub(r'    <div id="setup-view" class="view">.*?</div>\n    </div>', new_setup_html, html, flags=re.DOTALL)

# 3. Ensure the createAccount function handles the transition properly
old_create = '''        showToast('Account created successfully!', 'success');
        document.getElementById('setup-view').classList.remove('active');
        document.getElementById('login-view').classList.add('active');'''
new_create = '''        showToast('Account created successfully! Please login.', 'success');
        document.getElementById('setup-view').classList.remove('active');
        document.getElementById('login-view').classList.add('active');
        document.getElementById('pin-input').focus();'''
html = html.replace(old_create, new_create)

with open('index.html', 'w') as f: f.write(html)
