with open('index.html', 'r') as f: html = f.read()

# 1. Add Setup View HTML
setup_html = '''
    <div id="setup-view" class="view">
        <div class="login-card">
            <div class="brand-mark">AJ</div>
            <h1>Setup Account</h1>
            <div class="sub">Create your business profile</div>
            <input type="text" id="setup-biz" class="pin-input" style="font-size:16px; letter-spacing:normal; text-indent:0;" placeholder="Business Name">
            <input type="password" id="setup-owner" class="pin-input" maxlength="4" placeholder="Owner PIN (4 digits)">
            <input type="password" id="setup-staff" class="pin-input" maxlength="4" placeholder="Staff PIN (4 digits)">
            <button class="btn-primary" onclick="createAccount()">Create Account</button>
        </div>
    </div>
'''
html = html.replace('<div id="app-view" class="view">', setup_html + '\n    <div id="app-view" class="view">')

# 2. Add Setup Logic
setup_js = '''
    function checkFirstTime() {
        if (!localStorage.getItem('asad:settings')) {
            document.getElementById('login-view').classList.remove('active');
            document.getElementById('setup-view').classList.add('active');
        } else {
            restoreSession();
        }
    }

    function createAccount() {
        const biz = document.getElementById('setup-biz').value || 'My Business';
        const ownerPin = document.getElementById('setup-owner').value;
        const staffPin = document.getElementById('setup-staff').value;
        
        if (ownerPin.length !== 4 || staffPin.length !== 4) {
            return showToast('PINs must be exactly 4 digits', 'err');
        }
        
        settings.businessName = biz;
        settings.ownerPin = ownerPin;
        settings.staffPin = staffPin;
        saveData('settings', settings);
        
        showToast('Account created successfully!', 'success');
        document.getElementById('setup-view').classList.remove('active');
        document.getElementById('login-view').classList.add('active');
    }
'''
html = html.replace('// --- Auth & Navigation ---', setup_js + '\n// --- Auth & Navigation ---')

# 3. Add Security to Settings Modal
settings_sec = '''
            <div class="eyebrow">Security</div>
            <div class="row">
                <div class="form-group"><label>Owner PIN</label><input type="password" id="set-owner-pin" maxlength="4" value="${settings.ownerPin}"></div>
                <div class="form-group"><label>Staff PIN</label><input type="password" id="set-staff-pin" maxlength="4" value="${settings.staffPin}"></div>
            </div>
            <button class="btn" onclick="saveSettings()">${t.saveSettings}</button>
'''
html = html.replace('<button class="btn" onclick="saveSettings()">${t.saveSettings}</button>', settings_sec)

# 4. Save PINs in saveSettings
save_logic = '''
        settings.ownerPin = document.getElementById('set-owner-pin').value || settings.ownerPin;
        settings.staffPin = document.getElementById('set-staff-pin').value || settings.staffPin;
'''
html = html.replace("settings.lang = newLang;", "settings.lang = newLang;" + save_logic)

# 5. Change initial restoreSession call to checkFirstTime
html = html.replace('restoreSession();\n</script>', 'checkFirstTime();\n</script>')

with open('index.html', 'w') as f: f.write(html)
