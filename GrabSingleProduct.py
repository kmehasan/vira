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
import requests

base_url = "https://www.vrai.com/engagement-rings/single-shared-prong-ring"
rotation_btn = "css-2tk4lu"
diamondTypeOption = "diamondTypeOption"
metal = "//div[@data-cy='metal-options-desktop']//button"
band = "//div[@data-cy='band-accent-options-desktop']//button"

required_metal = ["N/A","18k Yellow gold","18k White gold","14k Rose gold"]



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
shapes = browser.find_elements(By.CLASS_NAME,diamondTypeOption)
metal_types = browser.find_elements(By.XPATH,metal)
band_types = browser.find_elements(By.XPATH,band)

if len(shapes) == 0:
    shapes.append(None)
if len(metal_types) == 0:
    metal_types.append(None)
if len(band_types) == 0:
    band_types = browser.find_elements(By.XPATH,"//div[@data-cy='band-stone-style-options']")
    if(len(band_types)!=0):
        band_types = band_types[0].find_elements(By.TAG_NAME,"input")
    if len(band_types) == 0:
        band_types.append(None)


print("Shape", len(shapes))
print("metal_types", len(metal_types))
print("band_types", len(band_types))

rotation_name = "normal"
product_name = browser.find_element(By.CLASS_NAME,"secondary").get_attribute("innerText")
print(product_name)
for _ in range(2):
    for shape in shapes:
        if shape != None: browser.execute_script("arguments[0].click();", shape)
        for metal_type in metal_types:
            if metal_type != None: browser.execute_script("arguments[0].click();", metal_type)
            for band_type in band_types:
                if band_type != None: browser.execute_script("arguments[0].click();", band_type)
                time.sleep(2)
                # names = browser.find_elements(By.CLASS_NAME,"css-qcxoy1")
                
                shape_name = "N/A"
                metal_name = "N/A"
                band_name = "N/A"

                shape_name_elements = browser.find_elements(By.XPATH,"//div[@data-cy='diamond-type-options']//strong/parent::div")
                metal_name_elements = browser.find_elements(By.XPATH,"//*[@id='metal-options-desktop']/parent::div")
                band_name_elements = browser.find_elements(By.XPATH,"//*[@id='band-accent-options-desktop']/parent::div")
                
                if len(shape_name_elements) != 0:
                    shape_name = shape_name_elements[0].get_attribute("innerText").replace("Shape:","").strip()
                if len(metal_name_elements) != 0:
                    metal_name = metal_name_elements[0].get_attribute("innerText").replace("Metal:","").strip()
                if len(band_name_elements) == 0:
                    band_name_elements = browser.find_elements(By.XPATH,"//div[@data-cy='band-stone-style-options']//strong/parent::div")
                if len(band_name_elements) != 0:
                    band_name = band_name_elements[0].get_attribute("innerText").replace("Band:","").strip()

                if metal_name not in required_metal:
                    continue
                price_element = browser.find_elements(By.CLASS_NAME,"css-yiumrc")
                if len(price_element) == 0:
                    price_element = browser.find_elements(By.CLASS_NAME,"css-1j526tz")
                product_price = price_element[0].get_attribute("innerText").replace("Starting at $","").replace(",","")
                product_description = browser.find_element(By.CLASS_NAME,"css-ge5w1a").get_attribute("innerText")
                product_description += "\n"+browser.find_element(By.CLASS_NAME,"css-zwtnw5").get_attribute("innerText")
                imgs = browser.\
                    find_elements(By.XPATH,"//div[@name='thumbnail-media-0']/parent::div//img")
                # folder_name = f"images/{product_name}/{rotation_name}/{shape_name}/{metal_name}/{band_name}"
                # if not os.path.exists(folder_name):
                #     os.makedirs(folder_name)
                
                images_links = []
                imgs.remove(imgs[1]) # remove the icon image
                for index,img in enumerate(imgs):
                    src = img.get_attribute("src").split("?")[0]
                    image_name = src.split("/")[-1]
                    print(shape_name, metal_name, band_name, src)
                    images_links.append(src)
                    # response = requests.get(src)
                    # with open(f"{folder_name}/{image_name}", "wb") as f:
                    #     f.write(response.content)
                with open(f"products/description.csv","a") as f:
                    f.write(f"\"{product_name}\",\"{rotation_name}\",\"{shape_name}\",\"{metal_name}\",\"{band_name}\",\"{product_price}\",\"{','.join(images_links)}\",\"{product_description}\"\n")

    browser.find_element(By.CLASS_NAME,rotation_btn).click()
    rotation_name = "rotated_90_degrees"