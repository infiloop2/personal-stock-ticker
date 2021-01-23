from coinbase.wallet.client import Client
import yahoo_fin.stock_info as si
import time
import json

with open('config.json', 'r') as f:
    config = json.load(f)

key = config["key"]
secret = config["secret"]

sum = 0.0
client = Client(key, secret)
accounts = client.get_accounts()

for i in range(0, len(accounts.data)):
    sum += float(str(accounts.data[i].native_balance)[4:])

while accounts.pagination.next_starting_after is not None:
    accounts = client.get_accounts(
        starting_after=accounts.pagination.next_starting_after)

    for i in range(0, len(accounts.data)):
        sum += float(str(accounts.data[i].native_balance)[4:])

# Use this to convert to a currency different from your coinbase native currency
gbpusd = si.get_live_price("gbpusd=x")
total = int(sum * gbpusd)
timestamp = int(time.time())

print(timestamp, total)
