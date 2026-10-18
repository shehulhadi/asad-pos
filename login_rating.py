with open('index.html', 'r') as f: html = f.read()

# 1. Remove the old rating UI from Settings
old_settings_rating = '''            <div class="eyebrow" style="margin-top:24px; text-align:center;">Rate this App</div>
            <div style="display:flex; justify-content:center; gap:10px; font-size:28px; cursor:pointer; margin-bottom:10px;" id="rating-stars">
                <span onclick="submitRating(1)">☆</span>
                <span onclick="submitRating(2)">☆</span>
                <span onclick="submitRating(3)">☆</span>
                <span onclick="submitRating(4)">☆</span>
                <span onclick="submitRating(5)">☆</span>
            </div>
            <p style="text-align:center; font-size:11px; color:var(--muted);">Built by Asad Tech Concepts</p>'''
html = html.replace(old_settings_rating, '')

# 2. Add the Rating Modal HTML right before the closing </body>
rating_html = '''
    <!-- RATING MODAL -->
    <div id="rating-modal" class="modal" onclick="if(event.target===this)closeRating()">
        <div class="modal-content" style="text-align:center;">
            <div style="width:56px; height:56px; border-radius:50%; background:var(--accent-soft); color:var(--accent); display:grid; place-items:center; margin:0 auto 14px;">
                <svg class="ic" style="width:28px;height:28px;stroke-width:2.2" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            </div>
            <h3 style="margin-bottom: 8px;">Enjoying the app?</h3>
            <p style="font-size:14px; color:var(--muted); margin-bottom: 24px;">Tap a star to rate your experience.</p>
            <div style="display:flex; justify-content:center; gap:12px; font-size:36px; cursor:pointer; margin-bottom:24px;" id="rating-stars-main">
                <span onclick="submitRating(1)">☆</span>
                <span onclick="submitRating(2)">☆</span>
                <span onclick="submitRating(3)">☆</span>
                <span onclick="submitRating(4)">☆</span>
                <span onclick="submitRating(5)">☆</span>
            </div>
            <button class="btn btn-outline" onclick="closeRating()">Maybe Later</button>
        </div>
    </div>
'''
html = html.replace('</body>', rating_html + '\n</body>')

# 3. Replace the submitRating function and add the popup logic
old_rating_js = '''    function submitRating(stars) {
        const starsEl = document.getElementById('rating-stars');
        let display = '';
        for (let i = 1; i <= 5; i++) {
            display += `<span onclick="submitRating(${i})" style="color:${i <= stars ? 'var(--accent)' : 'var(--muted)'}">${i <= stars ? '★' : '☆'}</span>`;
        }
        starsEl.innerHTML = display;
        
        setTimeout(() => {
            const waText = encodeURIComponent(`Hello Asad Tech Concepts! ⭐️⭐️⭐️⭐️⭐️\\n\\nI just used the ${settings.businessName} POS app and I rate it ${stars} out of 5 stars!\\n\\nFeedback: `);
            const devPhone = "2348000000000"; // <-- Replace with your actual WhatsApp number
            window.open(`https://wa.me/${devPhone}?text=${waText}`, '_blank');
        }, 400);
    }'''

new_rating_js = '''    function checkRatingPrompt() {
        if (!localStorage.getItem('asad:rated')) {
            setTimeout(() => {
                // Only show if user is still on the login screen
                if (document.getElementById('login-view').classList.contains('active')) {
                    document.getElementById('rating-modal').classList.add('active');
                }
            }, 3000);
        }
    }

    function submitRating(stars) {
        const starsEl = document.getElementById('rating-stars-main');
        let display = '';
        for (let i = 1; i <= 5; i++) {
            display += `<span onclick="submitRating(${i})" style="color:${i <= stars ? 'var(--accent)' : 'var(--muted)'}">${i <= stars ? '★' : '☆'}</span>`;
        }
        starsEl.innerHTML = display;
        
        localStorage.setItem('asad:rated', 'true');
        
        setTimeout(() => {
            document.getElementById('rating-modal').classList.remove('active');
            showToast('Thank you for your feedback!', 'success');
        }, 600);
    }

    function closeRating() {
        document.getElementById('rating-modal').classList.remove('active');
    }'''

html = html.replace(old_rating_js, new_rating_js)

# 4. Trigger checkRatingPrompt on load
html = html.replace('restoreSession();\n</script>', 'restoreSession();\n    checkRatingPrompt();\n</script>')

with open('index.html', 'w') as f: f.write(html)
