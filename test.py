from glob import glob
from pandas import read_csv
import pandas as pd
import shutil

files = glob('products/*.csv')
main = "/home/kme/Downloads/main.xlsx"
df = pd.read_excel(main)
dict = df.to_dict('records')
def findTotalNum(url):
    for i in dict:
        if i['URL'].strip() in url:
            return i['total_number'], i['URL'], i['isDone']
    return 0,"",""

for file in files:
    data = read_csv(file)
    url = data['url'][0]
    url = url.split("?")[0]
    file_size = len(data)
    # df get total_num where url contains df['url']
    total_num, main_url, isDone = findTotalNum(url)
    if isDone == "Done":
        continue
    # if(file_size == 12):
    #     print("File", file, "\n",url, main_url)
    # continue
    if total_num == file_size and total_num != 0:
        # shutil.copy(file, 'ok_files/')
        print(main_url, total_num, file_size, file.split("/")[-1])
    #  print(url, file_size, file.split("/")[-1])