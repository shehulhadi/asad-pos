import re
with open('index.html', 'r') as f: html = f.read()

# 1. Add defaults to settings
html = html.replace(
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: []",
    "marginAlertPct: 20, fixedCostsMonthly: 0, lowCement: 50, lowSand: 5, lowFuel: 20, customExpenses: [], streak: 0, lastOpenDate: '', bestDayAmount: 0"
)
if "if(!settings.customExpenses)" in html:
    html = html.replace(
        "if(!settings.customExpenses) settings.customExpenses = [];",
        "if(!settings.customExpenses) settings.customExpenses = [];\n    if(settings.streak === undefined) settings.streak = 0;\n    if(settings.lastOpenDate === undefined) settings.lastOpenDate = '';\n    if(settings.bestDayAmount === undefined) settings.bestDayAmount = 0;"
    )

# 2. Add Confetti, Streak, and Haptic functions
addictive_js = '''
    // --- Gamification Features ---
    function triggerConfetti() {
        const canvas = document.createElement('canvas');
        canvas.style.position = 'fixed'; canvas.style.top = '0'; canvas.style.left = '0';
        canvas.style.width = '100vw'; canvas.style.height = '100vh';
        canvas.style.pointerEvents = 'none'; canvas.style.zIndex = '99999';
        document.body.appendChild(canvas);
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth; canvas.height = window.innerHeight;
        
        let particles = [];
        for(let i = 0; i < 120; i++) {
            particles.push({
                x: canvas.width / 2, y: canvas.height / 2,
                vx: (Math.random() - 0.5) * 20, vy: (Math.random() - 0.5) * 20 - 5,
                color: `hsl(${Math.random() * 360}, 100%, 60%)`,
                size: Math.random() * 8 + 4, life: 100
            });
        }
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(p => {
                p.x += p.vx; p.y += p.vy; p.vy += 0.4; p.life -= 1;
                ctx.fillStyle = p.color;
                ctx.fillRect(p.x, p.y, p.size, p.size);
            });
            particles = particles.filter(p => p.life > 0);
            if(particles.length > 0) requestAnimationFrame(draw); else canvas.remove();
        }
        draw();
        if (navigator.vibrate) navigator.vibrate([100, 50, 100, 50, 200]);
    }

    function checkStreak() {
        const today = new Date().toISOString().split('T')[0];
        if (!settings.lastOpenDate) {
            settings.lastOpenDate = today;
            settings.streak = 1;
            saveData('settings', settings);
            return;
        }
        if (settings.lastOpenDate === today) return;
        
        const last = new Date(settings.lastOpenDate);
        const now = new Date(today);
        const diffDays = Math.round((now - last) / (1000 * 60 * 60 * 24));
        
        if (diffDays === 1) {
            settings.streak += 1;
            setTimeout(() => showToast(`🔥 ${settings.streak} Day Streak! Keep it up!`, 'success'), 1500);
        } else if (diffDays > 1) {
            settings.streak = 1; 
        }
        settings.lastOpenDate = today;
        saveData('settings', settings);
    }

    // --- Details & Edit Modals ---
'''
html = html.replace('// --- Details & Edit Modals ---', addictive_js)

# 3. Trigger streak check on load
html = html.replace(
    "if(settings.darkMode) document.body.classList.add('dark');",
    "checkStreak();\n    if(settings.darkMode) document.body.classList.add('dark');"
)

# 4. Add Streak & Best Day to Dashboard Hero
old_hero = '''            <div class="hero">
                <div class="lbl">${t.netProfit}</div>
                <div class="big ${netProfit < 0 ? 'neg' : ''}">${formatNaira(netProfit)}</div>
                <div class="meta">
                    <div>${t.revenue}<strong>${formatNaira(allRevenue)}</strong></div>
                    <div>${t.expenses}<strong>${formatNaira(allExpenses)}</strong></div>
                </div>
            </div>'''
new_hero = '''            <div class="hero">
                <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                        <div class="lbl">${t.netProfit}</div>
                        <div class="big ${netProfit < 0 ? 'neg' : ''}">${formatNaira(netProfit)}</div>
                    </div>
                    <div style="background:rgba(255,255,255,0.1); padding:6px 12px; border-radius:20px; font-size:12px; font-weight:800; color:#f59e0b; display:flex; align-items:center; gap:4px;">
                        🔥 ${settings.streak} Day Streak
                    </div>
                </div>
                <div class="meta">
                    <div>${t.revenue}<strong>${formatNaira(allRevenue)}</strong></div>
                    <div>${t.expenses}<strong>${formatNaira(allExpenses)}</strong></div>
                    <div>Best Day<strong>${formatNaira(settings.bestDayAmount)}</strong></div>
                </div>
            </div>'''
html = html.replace(old_hero, new_hero)

# 5. Add Haptic & Best Day logic to saveSale
old_save_logic = '''        sales.push(sale); saveData('sales', sales);
        const waText = buildWhatsAppReceipt(sale);'''
new_save_logic = '''        sales.push(sale); saveData('sales', sales);
        
        if (navigator.vibrate) navigator.vibrate(50); // Haptic feedback
        
        // Best Day Ever Check
        const todayStr = new Date().toISOString().split('T')[0];
        const todayTotal = sales.filter(s => s.date === todayStr).reduce((sum, s) => sum + s.totalAmount, 0);
        if (todayTotal > (settings.bestDayAmount || 0)) {
            settings.bestDayAmount = todayTotal;
            saveData('settings', settings);
            triggerConfetti();
            showToast(`🏆 NEW BEST DAY! ${formatNaira(todayTotal)}`, 'success');
        }

        const waText = buildWhatsAppReceipt(sale);'''
html = html.replace(old_save_logic, new_save_logic)

with open('index.html', 'w') as f: f.write(html)
