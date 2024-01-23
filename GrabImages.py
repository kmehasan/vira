from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import chromedriver_autoinstaller

from datetime import datetime, timedelta
import time
import pandas as pd
import os
import shutil
import pytz


base_url = "https://www.vrai.com/wedding-rings"
product_class_name = "category-product"

already_grabed = []

log_file = f'links/{base_url.split("/")[-1]}.txt'
if os.path.exists(log_file):
    with open(log_file,'r') as f:
        for line in f.readlines():
            already_grabed.append(line.strip())

chromedriver_autoinstaller.install()
# shutil.rmtree('chrome_user_dir',ignore_errors=True)
isExist = os.path.exists('chrome_user_dir')
if not isExist:
    os.makedirs('chrome_user_dir')
    print("Create new session for chromes")
options = Options()
# options.headless = True
options.add_argument('--user-data-dir=chrome_user_dir')
options.add_argument('--no-sandbox')
# options.add_argument('--headless')
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)
browser.get(base_url)
time.sleep(1)
i = 0
while True:
    try:
        load_more = browser.find_element(By.CLASS_NAME,'viewMoreButton')
        browser.execute_script("arguments[0].click();", load_more.find_element(By.TAG_NAME,'button'))
        # time.sleep(1)
        # load_more.click()
        # load_more.find_element(By.TAG_NAME,'button').click()
        time.sleep(1)
        i += 1
        if i > 100:
            break
        print(i)
    except Exception as e:
        print(e)
        break
products = browser.find_elements(By.CLASS_NAME,product_class_name)
print(len(products))
with open(log_file,'a') as f:
    for product in products:
        product_link = product.find_element(By.TAG_NAME,'a').get_attribute('href')
        if product_link not in already_grabed:
            f.write(product_link+'\n')