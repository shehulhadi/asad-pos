with open('index.html', 'r') as f: html = f.read()

# 1. Add rating UI to the Settings modal
old_settings_btns = '''            <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>
            <button class="btn btn-danger" style="margin-top:22px;" onclick="clearAllData()">${t.clearData}</button>'''

new_settings_btns = '''            <button class="btn btn-outline" style="margin-top:10px;" onclick="closeModal()">Cancel</button>
            <button class="btn btn-danger" style="margin-top:22px;" onclick="clearAllData()">${t.clearData}</button>
            
            <div class="eyebrow" style="margin-top:24px; text-align:center;">Rate this App</div>
            <div style="display:flex; justify-content:center; gap:10px; font-size:28px; cursor:pointer; margin-bottom:10px;" id="rating-stars">
                <span onclick="submitRating(1)">☆</span>
                <span onclick="submitRating(2)">☆</span>
                <span onclick="submitRating(3)">☆</span>
                <span onclick="submitRating(4)">☆</span>
                <span onclick="submitRating(5)">☆</span>
            </div>
            <p style="text-align:center; font-size:11px; color:var(--muted);">Built by Asad Tech Concepts</p>'''

html = html.replace(old_settings_btns, new_settings_btns)

# 2. Add the submitRating function
rating_func = '''
    function submitRating(stars) {
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
    }
'''
html = html.replace('// --- Clear Cache ---', rating_func + '\n// --- Clear Cache ---')

with open('index.html', 'w') as f: f.write(html)
