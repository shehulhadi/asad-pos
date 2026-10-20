with open('app.js', 'r') as f: js = f.read()

# 1. Replace hardcoded value="0" with empty value and placeholder="0"
js = js.replace('value="0"', 'value="" placeholder="0"')

# 2. Fix specific default values in Settings
js = js.replace('value="${settings.defaultPrices[\'4\'] || 0}"', 'value="${settings.defaultPrices[\'4\'] || \'\'}" placeholder="0"')
js = js.replace('value="${settings.defaultPrices[\'6\'] || 0}"', 'value="${settings.defaultPrices[\'6\'] || \'\'}" placeholder="0"')
js = js.replace('value="${settings.defaultPrices[\'9\'] || 0}"', 'value="${settings.defaultPrices[\'9\'] || \'\'}" placeholder="0"')
js = js.replace('value="${settings.marginAlertPct}"', 'value="${settings.marginAlertPct || \'\'}" placeholder="0"')
js = js.replace('value="${settings.fixedCostsMonthly}"', 'value="${settings.fixedCostsMonthly || \'\'}" placeholder="0"')
js = js.replace('value="${settings.lowCement}"', 'value="${settings.lowCement || \'\'}" placeholder="0"')
js = js.replace('value="${settings.lowSand}"', 'value="${settings.lowSand || \'\'}" placeholder="0"')
js = js.replace('value="${settings.mixCement}"', 'value="${settings.mixCement || \'\'}" placeholder="0"')
js = js.replace('value="${settings.mixSand}"', 'value="${settings.mixSand || \'\'}" placeholder="0"')

# 3. Fix edit forms to remove 0 values when empty
js = js.replace('value="${s.quantity}"', 'value="${s.quantity || \'\'}" placeholder="0"')
js = js.replace('value="${s.pricePerBlock}"', 'value="${s.pricePerBlock || \'\'}" placeholder="0"')
js = js.replace('value="${s.deliveryCharge}"', 'value="${s.deliveryCharge || \'\'}" placeholder="0"')
js = js.replace('value="${s.amountPaidAtSale}"', 'value="${s.amountPaidAtSale || \'\'}" placeholder="0"')

js = js.replace('value="${b.blocksProduced}"', 'value="${b.blocksProduced || \'\'}" placeholder="0"')
js = js.replace('value="${b.totalCost}"', 'value="${b.totalCost || \'\'}" placeholder="0"')
js = js.replace('value="${b.breakages}"', 'value="${b.breakages || \'\'}" placeholder="0"')
js = js.replace('value="${b.curingLoss}"', 'value="${b.curingLoss || \'\'}" placeholder="0"')

js = js.replace('value="${e.amount}"', 'value="${e.amount || \'\'}" placeholder="0"')

js = js.replace('value="${p.qty}"', 'value="${p.qty || \'\'}" placeholder="0"')
js = js.replace('value="${p.cost}"', 'value="${p.cost || \'\'}" placeholder="0"')
js = js.replace('value="${p.amountPaid || 0}"', 'value="${p.amountPaid || \'\'}" placeholder="0"')

# 4. Fix default quantity of 1 to be a placeholder
js = js.replace('id="s-qty" value="1" min="1"', 'id="s-qty" value="" min="1" placeholder="1"')
js = js.replace('id="r-qty" value="1" min="1"', 'id="r-qty" value="" min="1" placeholder="1"')

with open('app.js', 'w') as f: f.write(js)
