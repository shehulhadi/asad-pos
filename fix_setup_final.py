with open('index.html', 'r') as f: html = f.read()

# 1. Force correct CSS for setup view inputs
css_addition = '''
        #setup-view input { letter-spacing: normal !important; text-indent: 0 !important; font-size: 16px !important; text-align: left !important; padding: 12px 14px !important; }
        #setup-view .login-card { text-align: left; }
        #setup-view .brand-mark, #setup-view h1, #setup-view .sub { text-align: center; margin-left: auto; margin-right: auto; }
'''
# Remove old css if it exists
html = html.replace('/* ---------- Setup View ---------- */', '')
# Insert new css
html = html.replace('/* ---------- Shell ---------- */', css_addition + '\n        /* ---------- Shell ---------- */')

# 2. Locate the Setup View block and completely replace it
start_idx = html.find('<div id="setup-view" class="view">')
end_idx = html.find('<div id="app-view" class="view">')

if start_idx != -1 and end_idx != -1:
    new_setup = '''<div id="setup-view" class="view">
        <div class="login-card">
            <div style="text-align: center; margin-bottom: 24px;">
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
    </div>

    '''
    html = html[:start_idx] + new_setup + html[end_idx:]

with open('index.html', 'w') as f: f.write(html)
