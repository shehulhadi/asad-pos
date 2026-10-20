import re
with open('app.js', 'r') as f: js = f.read()

# 1. Fix the calculation in renderDashboard (the main Stock tile)
old_dash_calc = '''    const emptyBagsProduced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const emptyBagsSold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
    const emptyBagsAdj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
    const emptyBagsStock = emptyBagsProduced - emptyBagsSold + emptyBagsAdj;'''

new_dash_calc = '''    const emptyBagsPurchased = purchases.filter(p=>p.material==='empty_bag').reduce((s,p)=>s+p.qty,0);
    const emptyBagsProduced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
    const emptyBagsSold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
    const emptyBagsAdj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
    const emptyBagsStock = emptyBagsPurchased + emptyBagsProduced - emptyBagsSold + emptyBagsAdj;'''
js = js.replace(old_dash_calc, new_dash_calc)

# 2. Fix the calculation in openStockItem (the detail modal)
old_item_calc = '''        } else {
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const sold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
            currentStock = produced - sold + adj;
        }'''

new_item_calc = '''        } else {
            const purchased = purchases.filter(p=>p.material==='empty_bag').reduce((s,p)=>s+p.qty,0);
            const produced = batches.reduce((s,b)=>s+(b.cementBags||0),0);
            const sold = sales.reduce((s,v)=>s+(v.emptyBagQty||0),0);
            const adj = stockAdjustments.filter(a=>a.material==='empty_bag').reduce((s,a)=>s+a.qty,0);
            currentStock = purchased + produced - sold + adj;
        }'''
js = js.replace(old_item_calc, new_item_calc)

with open('app.js', 'w') as f: f.write(js)
print("Empty bag calculation fixed.")
