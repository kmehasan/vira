from glob import glob
import pandas as pd
import os
files = glob('v2/v2_products/*.xlsx')

print(len(files))
i = 0
for file in files:
    p_name = file.split('/')[-1].split('.')[0].replace('_description','').replace('_', ' ')
    print(p_name)
    folder_name = f'v2/final_folder/{p_name}'
    os.makedirs(folder_name, exist_ok=True)
    os.system(f'cp "{file}" "{folder_name}"')
    df = pd.read_excel(file)
    for index, d in df.iterrows():
        urls = d['images_links'].split('\n')
        product_name = d['product_name']
        shape = d['shape_name']
        metal = d['metal_name']
        band = d['band_name']
        side_stone_shape = d['side_stone_shape_name']
        side_stone_weight = d['side_stone_weight_name']
        folder_name = f'v2/final_folder/{product_name}/{shape}/{metal}/{band}/{side_stone_weight}/{side_stone_shape}'
        folder_name = folder_name.replace('/nan', '')
        print(folder_name)
        os.makedirs(folder_name, exist_ok=True)
        for url in urls:
            url = url.strip()
            name = url.split('/')[-1]
            local_path = os.path.join('/home/kme/vria/all/', name)
            # Copy the file from local_path to folder_name
            print(local_path)
            print(folder_name)
            os.system(f'cp "{local_path}" "{folder_name}"')


