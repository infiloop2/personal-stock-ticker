from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium import webdriver
import yahoo_fin.stock_info as si
import time

import json

with open('config.json', 'r') as f:
    config = json.load(f)

username = config["username"]
password = config["password"]

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

driver = Firefox(firefox_options=fireFoxOptions)
driver.get("https://ig.com/uk")
print("Browser Opened")
driver.find_element_by_link_text('Log in').click()
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.ID, 'account_id')))
driver.find_element_by_id('account_id').send_keys(username)
driver.find_element_by_id(
    'nonEncryptedPassword').send_keys(password + Keys.ENTER)
print("Password entered")
WebDriverWait(driver, 60).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'value-amount')))
WebDriverWait(driver, 60).until(
    EC.text_to_be_present_in_element((By.CLASS_NAME, 'value-amount'), "£"))

nav = driver.find_element_by_class_name('value-amount').get_attribute("title")
print("Value fetched")
val = float(re.sub('[^0-9]','', nav))/100
timestamp = int(time.time())
# Use this to convert to a currency different from your coinbase native currency
gbpusd = si.get_live_price("gbpusd=x")
total = int(val * gbpusd)

driver.find_element_by_class_name('network-profile-button').click()
driver.find_element_by_link_text('Logout').click()
driver.quit()

# Cleanup process, otherwise it becomes a zombie
os.system("pkill -f \"firefox\"")

print(timestamp, total)
