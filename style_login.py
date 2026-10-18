with open('index.html', 'r') as f: html = f.read()

# 1. Replace the Login View HTML
login_start = html.find('<div id="login-view" class="view active">')
app_start = html.find('<div id="app-view" class="view">')

if login_start != -1 and app_start != -1:
    new_login = '''<div id="login-view" class="view active" style="position: relative; justify-content: center; align-items: center; padding: 24px;">
        <div class="login-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%; max-width: 340px; height: 100%;">
            
            <!-- Top: Title & Description -->
            <div style="text-align: center; margin-bottom: 40px; margin-top: 40px;">
                <div class="brand-mark" id="login-logo" style="margin: 0 auto 20px;">AJ</div>
                <h1 id="login-title-text" style="font-size: 26px; font-weight: 800; letter-spacing: -0.6px; line-height: 1.2;">Loading...</h1>
                <div class="sub" id="login-sub-text" style="font-size: 13px; font-weight: 500; color: #94a3b8; letter-spacing: 0.5px; margin-top: 8px;">Business Management Portal</div>
            </div>

            <!-- Middle: Login Form -->
            <div style="width: 100%;">
                <input type="password" id="pin-input" class="pin-input" placeholder="••••" maxlength="4" inputmode="numeric" autocomplete="off">
                <button class="btn-primary" onclick="login()">Login</button>
                <div id="login-error">Invalid PIN</div>
            </div>

            <!-- Bottom: Rating Button -->
            <div style="position: absolute; bottom: 40px; left: 0; width: 100%; text-align: center; padding: 0 20px;">
                <button onclick="openRating()" style="background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.15); color: #e2e8f0; padding: 12px 24px; border-radius: 24px; font-size: 13px; font-weight: 600; display: inline-flex; align-items: center; gap: 8px; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    <span style="font-size: 16px;">⭐</span> Rate this App & Give Feedback
                </button>
            </div>
        </div>
    </div>

    '''
    html = html[:login_start] + new_login + html[app_start:]

# 2. Update JS to set the description text on load
old_js = '''    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    if(document.getElementById('login-title-text')) {
        document.getElementById('login-title-text').textContent = bizName;
        document.getElementById('login-logo').textContent = bizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
    }'''
new_js = '''    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    if(document.getElementById('login-title-text')) {
        document.getElementById('login-title-text').textContent = bizName;
        document.getElementById('login-logo').textContent = bizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        document.getElementById('login-sub-text').textContent = "Block Production & POS Manager";
    }'''
html = html.replace(old_js, new_js)

with open('index.html', 'w') as f: f.write(html)
