import requests
import os
import zipfile
import time
os.chdir(r'/Users/guo_tingyu/Downloads/github/class_university/房價趨勢預測/data/實登資料庫')

year = 112
seasons = [1,2,3,4]

for season in seasons:
    res = requests.get("https://plvr.land.moi.gov.tw//DownloadSeason?season="+str(year)+"S"+str(season)+"&type=zip&fileName=lvr_landcsv.zip")
    fname = str(year)+'Q'+str(season)+'.zip'
    open(fname, 'wb').write(res.content)

    folder = 'real_estate' + str(year) +'Q'+ str(season)
    if not os.path.isdir(folder):
        os.mkdir(folder)
    with zipfile.ZipFile(fname, 'r') as zip_ref:
        zip_ref.extractall(folder)
    os.remove(fname)
    print(f'{year}Q{season}已完成')