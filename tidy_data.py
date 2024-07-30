import pandas as pd
import numpy as np
import os
os.chdir(r'/Users/guo_tingyu/Downloads/github/class_university/房價趨勢預測/data/實登資料庫')


year = 112
seasons = [1,2,3,4]

df = pd.DataFrame()

for season in seasons:
    df_year = pd.read_csv(r'./real_estate{}Q{}/a_lvr_land_a.csv'.format(year, season), parse_dates=['交易年月日'])
    df = pd.concat([df, df_year])

df = df[~df['交易標的'].isin(['車位','土地'])]
df = df[~df['建物型態'].isin(['公寓(5樓含以下無電梯)','住宅大樓(11層含以上有電梯)'])]
df = df.dropna(subset=['建物移轉總面積平方公尺']).reset_index(drop=True)
df = df.dropna(subset=['交易年月日']).reset_index(drop=True)

df['交易年月日'] = pd.to_datetime(pd.to_numeric(df['交易年月日'],errors='coerce')+19110000,format='%Y%m%d',errors='coerce')
df['總價元'] = pd.to_numeric(df['總價元'] ,errors='coerce')

dataset = df[['交易年月日','總價元']]
dataset.columns = ['date', 'price']

df_index = pd.date_range('2023-01-01',periods = 334 ).to_frame()
df_index.columns=['date']

dataset=dataset.set_index('date')
day_avg = dataset['price'].resample('D').mean()
day = pd.DataFrame({'price':day_avg})
day = day.reset_index(drop=False)

series = pd.merge(df_index,day,on='date',how='left')
series = series.set_index('date')
series['price'] = series.groupby([series.index.month, series.index.year])['price'].transform(lambda x: x.fillna(x.mean()))

series.to_csv(r'../dataset.csv')

