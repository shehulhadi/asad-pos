import re
with open('index.html', 'r') as f: html = f.read()

# 1. Fix the broken CSS for .modal
html = re.sub(r'\.modal \{.*?\}', '.modal { display: none !important; position: fixed !important; inset: 0 !important; background: rgba(11,18,32,.6) !important; z-index: 1000 !important; align-items: flex-end; justify-content: center; backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }', html, flags=re.DOTALL)
html = re.sub(r'\.modal\.active \{.*?\}', '.modal.active { display: flex !important; }', html, flags=re.DOTALL)

# 2. Completely remove the old rating modal
html = re.sub(r'<!-- RATING & FEEDBACK MODAL -->.*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="rating-modal" class="modal".*?</div>\s*</div>\s*</div>', '', html, flags=re.DOTALL)

# 3. Inject the new Feedback & Rating Modal before </body>
modal_html = '''
    <!-- RATING & FEEDBACK MODAL -->
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
html = html.replace('</body>', modal_html + '\n</body>')

# 4. Add Backup button to the header (next to Refresh)
old_hdr = '''<button class="icon-btn" id="btn-refresh" onclick="nav('dashboard')" title="Refresh Dashboard"></button>'''
new_hdr = '''<button class="icon-btn" id="btn-refresh" onclick="nav('dashboard')" title="Refresh Dashboard"></button>
                <button class="icon-btn show" onclick="exportJSON()" title="Backup Data" id="ib-backup"></button>'''
html = html.replace(old_hdr, new_hdr)

# 5. Ensure the Backup button icon loads
html = html.replace("document.getElementById('ib-logout').innerHTML = ico('logout');", "document.getElementById('ib-logout').innerHTML = ico('logout');\n        document.getElementById('ib-backup').innerHTML = ico('update');")

with open('index.html', 'w') as f: f.write(html)
