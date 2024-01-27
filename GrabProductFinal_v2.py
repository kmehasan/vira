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
import csv


# base_url = "https://www.vrai.com/engagement-rings/single-shared-prong-ring"
rotation_btn = "css-2tk4lu"
diamondTypeOption = "//button[contains(@class,'diamondTypeOption')]//parent::li//button"
metal = "//div[@aria-labelledby='metal-options-desktop']//button"
band = "//div[@data-cy='band-accent-options-desktop']//button"
side_stone_weight = "//div[@data-cy='side-stone-carat-options-desktop']//button"
side_stone_shape = "//div[@aria-labelledby='side-stone-shape-options-desktop']//button"
required_metal = ["N/A","14k Yellow Gold","14k White Gold","14k Rose gold"]

def clickElement(element):
    if element != None:
        try:
            browser.execute_script("arguments[0].click();", element)
        except:
            return False
    return True

# chromedriver_autoinstaller.install()
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

from selenium.webdriver.chrome.service import Service

service = Service(executable_path='./chromedriver')

browser = webdriver.Chrome(service=service,options=options)
def getShapes():
    shapes = browser.find_elements(By.XPATH,diamondTypeOption)
    if len(shapes) == 0:
        shapes = browser.find_elements(By.CLASS_NAME ,"diamondTypeOption")
    
    for s in getSideStoneShapes():
        if s in shapes:
            shapes.remove(s)
    if len(shapes) == 0:
            shapes.append(None)
    return shapes

def getMetalTypes():
    metal_types = browser.find_elements(By.XPATH,metal)

    # for m in metal_types[:]:
    #     if m.get_attribute("aria-label") not in required_metal:
    #         metal_types.remove(m)

    if len(metal_types) == 0:
        metal_types.append(None)
    return metal_types

def getBandTypes():
    band_types = browser.find_elements(By.XPATH,band)
    if len(band_types) == 0:
        band_types = browser.find_elements(By.XPATH,"//div[@data-cy='band-stone-style-options']")
        if(len(band_types)!=0):
            band_types = band_types[0].find_elements(By.TAG_NAME,"input")
        if len(band_types) == 0:
            band_types.append(None)
    return band_types
def getSideStonesWeight():
    side_stones_weight = browser.find_elements(By.XPATH,side_stone_weight)
    if len(side_stones_weight) == 0:
        side_stones_weight.append(None)
    return side_stones_weight

def getSideStoneShapes():
    side_stone_shapes = browser.find_elements(By.XPATH,side_stone_shape)
    if len(side_stone_shapes) == 0:
        side_stone_shapes.append(None)
    return side_stone_shapes

def getSorted(inp_list = []):
    res = []
    dict = {}
    none_index = -1
    for d in inp_list:
        if d["list"][0] == None:
            dict[none_index] = d
            none_index -= 1
        else:
            dict[d["list"][0].location['y']] = d
    for key in sorted(dict.keys()):
        res.append(dict[key])
    return res

def getProductData(base_url, debug=False, comb = 1):
    import pandas as pd

    dataframe = pd.DataFrame(columns=[
        'product_name', 
        'rotation_name', 
        'shape_name', 
        'metal_name', 
        'band_name', 
        'side_stone_shape_name',
        'side_stone_weight_name', 
        'side_stone_shape_name', 
        'product_price', 
        'images_links', 
        'product_description',
        'product_url'
        ])
    browser.get(base_url)
    time.sleep(1)
    i = 0
    shapes = getShapes()
    metal_types = getMetalTypes()
    band_types = getBandTypes()
    side_stones_weight = getSideStonesWeight()
    side_stone_shapes = getSideStoneShapes()
    
    print("URL",browser.current_url)
    print("Shape", len(shapes))
    print("metal_types", len(metal_types))
    print("band_types", len(band_types))
    print("side_stons", len(side_stones_weight))
    print("side_stone_shapes", len(side_stone_shapes))
    if(debug):
        combV = len(shapes)*len(metal_types)*len(band_types)*len(side_stones_weight)*len(side_stone_shapes)
        print("URL = ",base_url,"\n","Combination",combV, "Expected",comb, "valid", combV >= comb)
        return
    rotation_name = "normal"
    product_name = browser.find_element(By.CLASS_NAME,"secondary").get_attribute("innerText")
    print(product_name)
    file_product_name = product_name.replace(" ","_")
    if(not os.path.exists(f"products/{file_product_name}_description.csv")):    
        with open(f"products/{file_product_name}_description.csv", "w") as f:
            f.write("product_name,rotation_name,shape_name,metal_name,band_name,side_stone_shape_name,side_stone_weight_name,product_price,images_links,product_description,url\n")
    list_of_elements = [
        {"list":shapes,"name":"shapes","function":getShapes},
        {"list":metal_types,"name":"metal_types","function":getMetalTypes},
        {"list":band_types,"name":"band_types","function":getBandTypes},
        {"list":side_stones_weight,"name":"side_stones_weight","function":getSideStonesWeight},
        {"list":side_stone_shapes,"name":"side_stone_shapes","function":getSideStoneShapes}
    ]
    for _ in range(2):
        shapes = getShapes()
        for shape in shapes:
            if clickElement(shape) == False:
                continue
            # if shape != None: browser.execute_script("arguments[0].click();", shape)
            side_stone_shapes = getSideStoneShapes()
            for side_shape in side_stone_shapes:
                if clickElement(side_shape) == False:
                    continue
                side_stones_weight = getSideStonesWeight()
                for side in side_stones_weight:
                    if clickElement(side) == False:
                        continue
                
                    # if band_type != None: browser.execute_script("arguments[0].click();", band_type)
                    metal_types = getMetalTypes()
                    for metal_type in metal_types:
                        if clickElement(metal_type) == False:
                            continue
                
                        # if side_shape != None: browser.execute_script("arguments[0].click();", side_shape)
                        band_types = getBandTypes()
                        for band_type in band_types:
                            if clickElement(band_type) == False:
                                continue
                            # if side != None: browser.execute_script("arguments[0].click();", side)
                            # for _ in range(10):
                            #     browser.execute_script("window.scrollTo(0, 200)")
                            #     time.sleep(1)
                            # for _ in range(10):
                            #     browser.execute_script("window.scrollTo(0, -200)")
                            #     time.sleep(1)
                            
                            # browser.execute_script("window.scrollTo(0, 2500)")
                            
                            browser.execute_script("window.scrollBy({top: 2500, behavior: 'smooth'});")
                            time.sleep(2.5)
                            
                            browser.execute_script("window.scrollBy({top: -2500, behavior: 'smooth'});")
                            time.sleep(2.5)
                            
                            # names = browser.find_elements(By.CLASS_NAME,"css-qcxoy1")
                            
                            shape_name = "N/A"
                            metal_name = "N/A"
                            band_name = "N/A"
                            side_stone_weight_name = "N/A"
                            side_stone_shape_name = "N/A"
                            

                            shape_name_elements = browser.find_elements(By.XPATH,"//div[@data-cy='diamond-type-options']//strong/parent::div")
                            metal_name_elements = browser.find_elements(By.XPATH,"//*[@id='metal-options-desktop']/parent::div")
                            band_name_elements = browser.find_elements(By.XPATH,"//*[@id='band-accent-options-desktop']/parent::div")
                            side_stone_weight_name_elements = browser.find_elements(By.XPATH,"//*[@id='side-stone-carat-options-desktop']/parent::div")
                            side_stone_shape_name_elements = browser.find_elements(By.XPATH,"//*[@id='side-stone-shape-options-desktop']/parent::div")

                            if len(shape_name_elements) != 0:
                                shape_name = shape_name_elements[0].get_attribute("innerText").replace("Shape:","").strip()
                            if len(metal_name_elements) != 0:
                                metal_name = metal_name_elements[0].get_attribute("innerText").replace("Metal:","").strip()
                            if len(band_name_elements) == 0:
                                band_name_elements = browser.find_elements(By.XPATH,"//div[@data-cy='band-stone-style-options']//strong/parent::div")
                            if len(band_name_elements) != 0:
                                band_name = band_name_elements[0].get_attribute("innerText").replace("Band:","").strip()
                            
                            if len(side_stone_weight_name_elements) != 0:
                                side_stone_weight_name = side_stone_weight_name_elements[0].get_attribute("innerText").replace("Side stone carat weight:","").strip()
                            if len(side_stone_shape_name_elements) != 0:
                                side_stone_shape_name = side_stone_shape_name_elements[0].get_attribute("innerText").replace("Side stone carat weight:","").strip()
                            
                            # if metal_name not in required_metal:
                            #     continue
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

                            with open("v2/image_db.csv","a") as f_db:
                                for index,img in enumerate(imgs):
                                    # if img.size['height'] < 30: continue
                                    src = img.get_attribute("src").split("?")[0]

                                    image_name = src.split("/")[-1]
                                    f_db.write(f"{image_name},{src}\n")

                                    images_links.append(src)
                                    
                            print(shape_name, metal_name, band_name, side_stone_weight_name,side_stone_shape_name_elements)
                            with open(f"v2_products/{file_product_name}_description.csv","a",newline='') as f:
                                writer = csv.writer(f, delimiter=',')
                                writer.writerow([product_name,rotation_name,shape_name,metal_name,band_name,side_stone_shape_name,side_stone_weight_name,side_stone_shape_name,product_price,','.join(images_links),product_description,browser.current_url])
                                new_row = pd.Series(
                                    {
                                        'product_name': product_name,
                                        'rotation_name': rotation_name,
                                        'shape_name': shape_name,
                                        'metal_name': metal_name,
                                        'band_name': band_name,
                                        'side_stone_shape_name': side_stone_shape_name,
                                        'side_stone_weight_name': side_stone_weight_name,
                                        'side_stone_shape_name': side_stone_shape_name,
                                        'product_price': product_price,
                                        'images_links': '\n'.join(images_links),
                                        'product_description': product_description,
                                        'product_url': browser.current_url
                                    }
                                )
                                dataframe.loc[len(dataframe)] = new_row
                                print("Write to csv", [product_name,rotation_name,shape_name,metal_name,band_name,side_stone_shape_name,side_stone_weight_name,side_stone_shape_name,product_price,','.join(images_links),product_description,browser.current_url])
                                # f.write(f"\"{product_name}\",\"{rotation_name}\",\"{shape_name}\",\"{metal_name}\",\"{band_name}\",\"{product_price}\",\"{','.join(images_links)}\",\"{product_description}\"\n")
        try:
            browser.find_element(By.CLASS_NAME,rotation_btn).click()
            rotation_name = "rotated_90_degrees"
        except:

            break
    dataframe.to_excel(f"v2/v2_products/{file_product_name}_description.xlsx")
    with open("v2/done_v2.txt","a") as f:
        f.write(url)

urls = [

]
failed_urls = [
"https://www.vrai.com/jewelry/earrings/duo-drop-earring",
# "https://www.vrai.com/wedding-bands/alternating-shapes-band?metal=white-gold&diamondType=round-brilliant&goldPurity=18k&ringSize=6&bandStyle=half",
"https://www.vrai.com/jewelry/necklaces/halo-diamond-pendant?metal=white-gold&diamondType=pear&ringSize=0.25ct",
# "https://www.vrai.com/jewelry/necklaces/arc-diamond-necklace?metal=yellow-gold&diamondType=round-brilliant&diamondCount=5&diamondSize=original&ringSize=16-18",
"https://www.vrai.com/jewelry/necklaces/petite-pave-bar-necklace?metal=yellow-gold&diamondType=round-brilliant&ringSize=16-18",
# "https://www.vrai.com/jewelry/earrings/pave-cluster-stud?metal=white-gold&paveCluster=round",
"https://www.vrai.com/wedding-bands/pave-dome-band?bandAccent=pave&metal=yellow-gold&goldPurity=18k&ringSize=6",
"https://www.vrai.com/jewelry/rings/trellis-ring",
"https://www.vrai.com/jewelry/rings/perennial-ring",
"https://www.vrai.com/jewelry/earrings/perennial-stud?metal=yellow-gold&goldPurity=14k&side=left&qty=2",
"https://www.vrai.com/jewelry/necklaces/perennial-necklace",
"https://www.vrai.com/jewelry/rings/orion-ring?diamondType=round-brilliant%2Bbaguette%2Bmarquise",
"https://www.vrai.com/jewelry/earrings/orion-stud?diamondType=round-brilliant%2Bbaguette%2Bmarquise&metal=yellow-gold&goldPurity=14k&side=left&qty=2",
"https://www.vrai.com/jewelry/necklaces/duo-drop-necklace?metal=white-gold&diamondType=round-brilliant%2Bpear&ringSize=16-18",
"https://www.vrai.com/jewelry/bracelets/orion-bracelet?diamondType=round-brilliant%2Bbaguette%2Bmarquise",
"https://www.vrai.com/jewelry/necklaces/orion-necklace?diamondType=round-brilliant%2Bbaguette%2Bmarquise",
"https://www.vrai.com/jewelry/bracelets/linked-tennis-bracelet?metal=white-gold&diamondType=round-brilliant&ringSize=6.5-7",
"https://www.vrai.com/jewelry/necklaces/linked-tennis-necklace?metal=yellow-gold&diamondType=round-brilliant&ringSize=16-18",
]

dict_data = {
"https://www.vrai.com/wedding-bands/alternating-shapes-band?metal=white-gold&diamondType=round-brilliant&goldPurity=18k&ringSize=6&bandStyle=half":6,
# "https://www.vrai.com/jewelry/necklaces/arc-diamond-necklace?metal=yellow-gold&diamondType=round-brilliant&diamondCount=5&diamondSize=original&ringSize=16-18":15,
# "https://www.vrai.com/jewelry/earrings/pave-cluster-stud?metal=white-gold&paveCluster=round":6,
}
print(len(failed_urls))
for d in dict_data.keys():
    url = d
    comb = dict_data[d]
    getProductData(url,True,comb)
# for url in failed_urls[:]:
#     getProductData(url,True)