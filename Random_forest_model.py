import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor

def series_to_series(data ,n_in=30,n_out=5,dropna=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols= list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
    agg = pd.concat(cols,axis=1)
    if dropna:
        agg.dropna(inplace=True)
    return agg.values

dataset = pd.read_csv('/Users/guo_tingyu/Downloads/github/class_university/房價趨勢預測/data/dataset.csv')
value = dataset[['price']].values
train = series_to_series(value)
trainX , trainY = train[:,:-5] , train[:,-5:]
model = RandomForestRegressor(n_estimators=100)
model.fit(trainX, trainY)

row = value[1:31].flatten()
yhat = model.predict(np.asarray([row]))