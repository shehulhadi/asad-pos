import re
with open('app.js', 'r') as f: js = f.read()

# 1. Rename the button text in the Sales Modal
js = js.replace('>🔄 Trade-In</button>', '>🔄 Kakara</button>')

# 2. Rename the Modal title in openAddDeviceModal
js = js.replace('<h3>Add New Device / Trade-In</h3>', '<h3>Add New Device / Kakara</h3>')

# 3. Rename the alert text in startTradeIn
js = js.replace('alert(\'Enter the Trade-In device details below. Customer info has been pre-filled as the Seller.\');', 'alert(\'Enter the Kakara device details below. Customer info has been pre-filled as the Seller.\');')

with open('app.js', 'w') as f: f.write(js)
print("Trade-In renamed to Kakara successfully.")
