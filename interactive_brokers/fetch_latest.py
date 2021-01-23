from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium import webdriver
import yahoo_fin.stock_info as si
import time
import os
import json
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

username = config["username"]
password = config["password"]
account_number = config["account_number"]

while True:
    print("Attempting to start IBKR gateway")

    os.system(
        "cd clientportal && (nohup bin/run.sh root/conf.yaml &)")
    # Wait 60 sec for gateway to start. (Shot in the dark)
    time.sleep(60)
    print("Hopefully started Gateway")

    print("Attempting to Login")

    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.set_headless()
    print("Opening Browser")
    driver = Firefox(firefox_options=fireFoxOptions)
    driver.get("https://localhost:5000")
    driver.find_element_by_id('user_name').send_keys(username)
    driver.find_element_by_id('password').send_keys(
        password + Keys.ENTER)

    print("Entered username and password")
    # Wait 60 sec for login to be successful. (Shot in the dark)
    time.sleep(60)
    driver.quit()
    # Cleanup process, otherwise it becomes a zombie
    os.system("pkill -f \"firefox\"")

    print("Hopefully Logged In")

    print("Starting API Calls")
    # A startup call is needed before accessing account details
    os.system(
        "curl -k --max-time 5 https://localhost:5000/v1/portal/portfolio/accounts")

    failures = 0
    while failures < 60:
        try:
            print("Validating SSO session")
            os.system(
                "curl -k --max-time 5 https://localhost:5000/v1/portal/sso/validate | jq '.RESULT' > auth_data")
            f = open('auth_data', 'r')
            auth = f.readline().strip()
            f.close()
            print("authenticated", auth)

            print("Fetching Latest VAL")
            os.system(
                "curl -k --max-time 5 https://localhost:5000/v1/portal/portfolio/" + account_number + "/summary | jq '.netliquidation.amount' > val_data")
            f = open('val_data', 'r')
            val = f.readline().strip()
            f.close()
            print("val", val)

            if auth != "true" or val == "":
                print("Gateway not working, counting as failure")
                failures += 1

            val = float(val)
            timestamp = int(time.time())
            # Use this to convert to a currency different from your coinbase native currency
            gbpusd = si.get_live_price("gbpusd=x")
            total = int(val * gbpusd)

            print(ts, total)

            print("Sleeping for 1 sec")
            time.sleep(1)
        except:
            failures += 1

    print("Killing IBKR Gateway")
    os.system("pkill -f \"java -server\"")
