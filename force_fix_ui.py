import re
with open('index.html', 'r') as f: html = f.read()

# 1. Force replace the Login View
login_start = html.find('<div id="login-view" class="view active">')
app_start = html.find('<div id="app-view" class="view">')
if login_start != -1 and app_start != -1:
    new_login = '''<div id="login-view" class="view active">
        <div class="login-card">
            <div class="brand-mark" id="login-logo">AJ</div>
            <h1 id="login-title-text" style="font-size: 22px; line-height: 1.2; word-break: break-word;">A. Jibrialla</h1>
            <div class="sub" id="login-sub-text" style="font-size: 11px;">MANAGEMENT PORTAL</div>
            <input type="password" id="pin-input" class="pin-input" placeholder="••••" maxlength="4" inputmode="numeric" autocomplete="off">
            <button class="btn-primary" onclick="login()">Login</button>
            <div id="login-error">Invalid PIN</div>
        </div>
    </div>

    '''
    html = html[:login_start] + new_login + html[app_start:]

# 2. Force replace the Rating Modal
rating_start = html.find('<!-- RATING & FEEDBACK MODAL -->')
toast_start = html.find('<div id="toast-container"></div>')
if rating_start != -1 and toast_start != -1:
    new_rating = '''<!-- RATING & FEEDBACK MODAL -->
    <div id="rating-modal" class="modal" onclick="if(event.target===this)closeRating()">
        <div class="modal-content">
            <div style="text-align:center; margin-bottom:16px;">
                <div style="width:56px; height:56px; border-radius:50%; background:var(--accent-soft); color:var(--accent); display:grid; place-items:center; margin:0 auto 14px;">
                    <svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                </div>
                <h3 id="rating-app-title" style="margin-bottom: 4px;">Rate this App</h3>
                <p style="font-size:13px; color:var(--muted);">How is your experience so far?</p>
            </div>
            
            <div style="display:flex; justify-content:center; gap:12px; font-size:36px; cursor:pointer; margin-bottom:16px;" id="rating-stars-main">
                <span onclick="setStars(1)">☆</span>
                <span onclick="setStars(2)">☆</span>
                <span onclick="setStars(3)">☆</span>
                <span onclick="setStars(4)">☆</span>
                <span onclick="setStars(5)">☆</span>
            </div>

            <div class="form-group">
                <textarea id="feedback-text" style="width:100%; height:80px; padding:12px; border:1.5px solid var(--line); border-radius:8px; font-size:14px; resize:none; background:#f8fafc; outline:none;" placeholder="Any feedback or feature requests?"></textarea>
            </div>

            <button class="btn btn-primary" style="margin-top:0; background:#25D366; color:#fff; box-shadow:none;" onclick="sendFeedback()">Send via WhatsApp</button>
            <button class="btn btn-outline" style="margin-top:8px;" onclick="closeRating()">Maybe Later</button>
            
            <div style="text-align:center; margin-top:20px; font-size:11px; color:var(--muted); line-height:1.5;">
                <strong id="rating-app-footer">App Version 1.0.0</strong><br>
                Built by Asad Tech Concepts<br>
                <a href="https://wa.me/2348000000000" target="_blank" style="color:var(--brand); text-decoration:none;">Contact Support</a>
            </div>
        </div>
    </div>

    '''
    html = html[:rating_start] + new_rating + html[toast_start:]

# 3. Force replace the Rating Logic
old_logic = re.search(r'    let ratingTimer;.*?function closeRating\(\) \{.*?\n    \}', html, re.DOTALL)
if old_logic:
    new_logic = '''    let ratingTimer;
    let currentRating = 0;

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
    }

    function setStars(stars) {
        currentRating = stars;
        const starsEl = document.getElementById('rating-stars-main');
        let display = '';
        for (let i = 1; i <= 5; i++) {
            display += `<span onclick="setStars(${i})" style="color:${i <= stars ? 'var(--accent)' : 'var(--muted)'}">${i <= stars ? '★' : '☆'}</span>`;
        }
        starsEl.innerHTML = display;
    }

    function sendFeedback() {
        if (currentRating === 0) return showToast('Please select a star rating first', 'err');
        const text = document.getElementById('feedback-text').value;
        const devPhone = "2348000000000"; 
        const msg = encodeURIComponent(`Hello Asad Tech Concepts!\\n\\nApp Rating: ${currentRating} out of 5 stars ⭐\\n\\nFeedback: ${text || 'No extra text.'}\\n\\nBusiness: ${settings.businessName || 'N/A'}`);
        
        localStorage.setItem('asad:rated', 'true');
        document.getElementById('rating-modal').classList.remove('active');
        showToast('Thank you for your feedback!', 'success');
        
        setTimeout(() => { window.open(`https://wa.me/${devPhone}?text=${msg}`, '_blank'); }, 500);
    }

    function closeRating() {
        localStorage.setItem('asad:rated', 'true');
        document.getElementById('rating-modal').classList.remove('active');
    }'''
    html = html[:old_logic.start()] + new_logic + html[old_logic.end():]

# 4. Fix the dynamic title injection in initialization
old_init = '''    // Update title on initial load
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
new_init = '''    // Update title on initial load
    const bizName = settings.businessName || 'My Business';
    document.title = bizName;
    if(document.getElementById('app-title')) document.getElementById('app-title').textContent = bizName;
    
    // Update Login Page texts
    if(document.getElementById('login-title-text')) {
        document.getElementById('login-title-text').textContent = bizName;
        const initials = bizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
        document.getElementById('login-logo').textContent = initials;
    }'''
html = html.replace(old_init, new_init)

with open('index.html', 'w') as f: f.write(html)
