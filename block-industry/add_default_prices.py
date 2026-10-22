import re
with open('app.js', 'r') as f: js = f.read()

# 1. Add defaults to settings object
html_default = '''    if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};'''
new_default = '''    if(!settings.defaultPrices) settings.defaultPrices = {'4': 0, '6': 0, '9': 0};
    if(settings.defaultCementPrice === undefined) settings.defaultCementPrice = 0;
    if(settings.defaultEmptyBagPrice === undefined) settings.defaultEmptyBagPrice = 0;'''
js = js.replace(html_default, new_default)

# 2. Update openSettings to include the new inputs
old_settings = '''            <div class="eyebrow">Default Selling Prices (₦)</div>
            <div class="row">
                <div class="form-group"><label>4" Block</label><input type="number" id="set-price-4" value="${settings.defaultPrices['4'] || ''}" placeholder="0"></div>
                <div class="form-group"><label>6" Block</label><input type="number" id="set-price-6" value="${settings.defaultPrices['6'] || ''}" placeholder="0"></div>
                <div class="form-group"><label>9" Block</label><input type="number" id="set-price-9" value="${settings.defaultPrices['9'] || ''}" placeholder="0"></div>
            </div>'''

new_settings = '''            <div class="eyebrow">Default Selling Prices (₦)</div>
            <div class="row">
                <div class="form-group"><label>6" Block</label><input type="number" id="set-price-6" value="${settings.defaultPrices['6'] || ''}" placeholder="0"></div>
            </div>
            <div class="row">
                <div class="form-group"><label>Cement (per Bag)</label><input type="number" id="set-price-cement" value="${settings.defaultCementPrice || ''}" placeholder="0"></div>
                <div class="form-group"><label>Empty Bag (per pc)</label><input type="number" id="set-price-emptybag" value="${settings.defaultEmptyBagPrice || ''}" placeholder="0"></div>
            </div>'''
js = js.replace(old_settings, new_settings)

# 3. Update saveSettings to save the new inputs
old_save = '''        settings.defaultPrices = {
            '4': parseFloat(document.getElementById('set-price-4').value) || 0,
            '6': parseFloat(document.getElementById('set-price-6').value) || 0,
            '9': parseFloat(document.getElementById('set-price-9').value) || 0
        };'''

new_save = '''        settings.defaultPrices = {
            '4': 0, // Deprecated
            '6': parseFloat(document.getElementById('set-price-6')?.value) || 0,
            '9': 0  // Deprecated
        };
        settings.defaultCementPrice = parseFloat(document.getElementById('set-price-cement')?.value) || 0;
        settings.defaultEmptyBagPrice = parseFloat(document.getElementById('set-price-emptybag')?.value) || 0;'''
js = js.replace(old_save, new_save)

# 4. Update renderAnalytics to use these default prices for Stock Value
old_stock_val = '''    // Blocks Value
    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const producedBlocks = readyBatches.reduce((s,b)=>s+(N(b.blocksProduced) - N(b.breakages)),0);
    const soldBlocks = sales.filter(s => s.size === '6').reduce((s,v)=>s+N(v.quantity),0);
    const brokenBlocks = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+N(v.blocks),0);
    const returnedBlocks = returns.filter(r => r.size === '6').reduce((s, r) => s + N(r.quantity), 0);
    const remainingBlocks = Math.max(0, producedBlocks - soldBlocks - brokenBlocks + returnedBlocks);
    
    unsoldValue += remainingBlocks * getAvgCost('6');
    
    // Raw Materials Value
    unsoldValue += cementData.stock * cementData.cost;
    unsoldValue += sandData.stock * sandData.cost;
    unsoldValue += ebData.stock * ebData.cost;'''

new_stock_val = '''    // Blocks Value (Use Default Selling Price if set, else fallback to cost)
    const readyBatches = batches.filter(b => b.size === '6' && b.status === 'ready');
    const producedBlocks = readyBatches.reduce((s,b)=>s+(N(b.blocksProduced) - N(b.breakages)),0);
    const soldBlocks = sales.filter(s => s.size === '6').reduce((s,v)=>s+N(v.quantity),0);
    const brokenBlocks = breakagesLog.filter(b => b.size === '6').reduce((s,v)=>s+N(v.blocks),0);
    const returnedBlocks = returns.filter(r => r.size === '6').reduce((s, r) => s + N(r.quantity), 0);
    const remainingBlocks = Math.max(0, producedBlocks - soldBlocks - brokenBlocks + returnedBlocks);
    
    const blockValPrice = N(settings.defaultPrices['6']) || getAvgCost('6');
    unsoldValue += remainingBlocks * blockValPrice;
    
    // Raw Materials Value (Use Default Selling Price if set, else fallback to avg cost)
    const cementValPrice = N(settings.defaultCementPrice) || cementData.cost;
    const ebValPrice = N(settings.defaultEmptyBagPrice) || ebData.cost;

    unsoldValue += cementData.stock * cementValPrice;
    // Sand omitted as requested
    unsoldValue += ebData.stock * ebValPrice;'''
js = js.replace(old_stock_val, new_stock_val)

with open('app.js', 'w') as f: f.write(js)
print("Default prices for stock value added.")
