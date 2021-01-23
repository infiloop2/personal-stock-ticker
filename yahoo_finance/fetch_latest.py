import yahoo_fin.stock_info as si
import time
import json

with open('config.json', 'r') as f:
    config = json.load(f)

sum = 0

for holding in config['portfolio']:
    qty = int(holding['quantity'])
    price = si.get_live_price(holding['ticker'])
    print(holding['ticker'], qty, price, qty * price)
    sum += qty * price

timestamp = int(time.time())
print(timestamp, sum)
