import re
with open('index.html', 'r') as f: html = f.read()

# 1. Remove the broken auto-popup JS and the broken init script
html = re.sub(r'    // Force Title on load.*?\}\);\n', '', html, flags=re.DOTALL)
html = re.sub(r'    let ratingTimer;.*?function checkRatingPrompt\(\) \{.*?\n    \}', '', html, flags=re.DOTALL)

# 2. Remove the broken rating modal HTML completely
html = re.sub(r'<!-- RATING MODAL -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<!-- RATING & FEEDBACK MODAL -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# 3. Add the "Rate App" button to the login screen
login_btn = '<button class="btn-primary" onclick="login()">Login</button>'
if 'id="btn-rate-login"' not in html:
    new_login_btn = login_btn + '\n            <button class="btn-lang" id="btn-rate-login" onclick="openRating()" style="margin-top: 12px; border: none; background: transparent; color: #94a3b8; font-size: 13px; text-decoration: underline;">⭐ Rate this App / Feedback</button>'
    html = html.replace(login_btn, new_login_btn)

# 4. Add the new Modal with INLINE styles (guaranteed to work)
modal_html = '''
    <!-- NEW RATING MODAL -->
    <div id="rating-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(11,18,32,0.85); z-index: 99999; align-items: center; justify-content: center; backdrop-filter: blur(3px);">
        <div style="background: #fff; border-radius: 20px; padding: 24px; width: 90%; max-width: 400px; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
            <div style="width:56px; height:56px; border-radius:50%; background:var(--accent-soft); color:var(--accent); display:grid; place-items:center; margin:0 auto 14px;">
                <svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </div>
            <h3 id="rating-app-title" style="margin-bottom: 4px; font-size:18px; font-weight:800;">Rate this App</h3>
            <p style="font-size:13px; color:var(--muted); margin-bottom: 16px;">How is your experience so far?</p>
            
            <div style="display:flex; justify-content:center; gap:12px; font-size:36px; cursor:pointer; margin-bottom:16px;" id="rating-stars-main">
                <span onclick="setStars(1)">☆</span>
                <span onclick="setStars(2)">☆</span>
                <span onclick="setStars(3)">☆</span>
                <span onclick="setStars(4)">☆</span>
                <span onclick="setStars(5)">☆</span>
            </div>

            <div style="margin-bottom:16px;">
                <textarea id="feedback-text" style="width:100%; height:70px; padding:12px; border:1.5px solid var(--line); border-radius:8px; font-size:14px; resize:none; background:#f8fafc; outline:none;" placeholder="Any feedback or feature requests?"></textarea>
            </div>

            <button class="btn btn-primary" style="margin-top:0; background:#25D366; color:#fff; box-shadow:none; margin-bottom:8px; font-weight:bold; border-radius:8px; padding:12px; border:none; width:100%;" onclick="sendFeedback()">Send via WhatsApp</button>
            <button class="btn btn-outline" style="margin-top:0; padding:12px; border-radius:8px; border:1px solid #ccc; width:100%; font-weight:bold; background:#fff; color:#333;" onclick="closeRating()">Maybe Later</button>
            
            <div style="margin-top:20px; font-size:11px; color:var(--muted); line-height:1.5;">
                <strong id="rating-app-footer">App v1.0.0</strong><br>
                Built by Asad Tech Concepts<br>
                <a href="https://wa.me/2348000000000" target="_blank" style="color:var(--brand); text-decoration:none;">Contact Support</a>
            </div>
        </div>
    </div>
'''
html = html.replace('</body>', modal_html + '\n</body>')

# 5. Add the clean JS functions
js_logic = '''
    let currentRating = 0;

    function openRating() {
        const bizName = (JSON.parse(localStorage.getItem('asad:settings')) || {}).businessName || 'My Business';
        document.getElementById('rating-app-title').textContent = bizName;
        document.getElementById('rating-app-footer').textContent = bizName + ' (v1.0.0)';
        document.getElementById('rating-modal').style.display = 'flex';
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
        const bizName = (JSON.parse(localStorage.getItem('asad:settings')) || {}).businessName || 'My Business';
        const msg = encodeURIComponent(`Hello Asad Tech Concepts!\\n\\nApp Rating: ${currentRating} out of 5 stars ⭐\\n\\nFeedback: ${text || 'No extra text.'}\\n\\nBusiness: ${bizName}`);
        
        localStorage.setItem('asad:rated', 'true');
        closeRating();
        showToast('Thank you for your feedback!', 'success');
        setTimeout(() => { window.open(`https://wa.me/${devPhone}?text=${msg}`, '_blank'); }, 500);
    }

    function closeRating() {
        localStorage.setItem('asad:rated', 'true');
        document.getElementById('rating-modal').style.display = 'none';
    }

    // Update title on load
    const initialBizName = (JSON.parse(localStorage.getItem('asad:settings')) || {}).businessName || 'My Business';
    document.title = initialBizName;
    if(document.getElementById('login-title-text')) {
        document.getElementById('login-title-text').textContent = initialBizName;
        document.getElementById('login-logo').textContent = initialBizName.split(' ').map(w => w[0]).join('').substring(0, 2).toUpperCase();
    }
'''
html = html.replace('restoreSession();\n</script>', js_logic + '\n    restoreSession();\n</script>')

with open('index.html', 'w') as f: f.write(html)
