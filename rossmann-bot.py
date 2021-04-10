import json
import requests
import pandas as pd

#loading test dataset
df10 = pd.read_csv('C:/Users/Henrique/data_science_producao/test.csv')
df_store_raw = pd.read_csv('C:/Users/Henrique/data_science_producao/store.csv')

#merge test dataset + store
df_test = pd.merge(df10, df_store_raw, how='left', on='Store')

#choose store for prediction
df_test = df_test[df_test['Store'] = 22]

#remove closed days
df_test = df_test[df_test['Open'] != 0]
df_test = df_test[~df_test['Open'].isnull()]
df_test = df_test.drop('Id', axis=1)

#convert dataframe to json
data = json.dumps(df_test.to_dict(orient='records'))

url = 'https://rossmann-modelv1.herokuapp.com/rossmann/predict'
header = {'Content-type':'application/json'}
data = data

r = requests.post(url, data=data, headers=header)
print('Status Code {}'.format(r.status_code))

d1 = pd.DataFrame(r.json(),columns=r.json()[0].keys())

d2 = d1[['store', 'prediction']].groupby('store').sum().reset_index()