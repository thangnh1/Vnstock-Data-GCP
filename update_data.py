from vnstock import listing_companies, stock_historical_data, last_xd
from datetime import datetime
import pandas as pd
from google.cloud import storage

PATH_KEY = 'vnstock-381809-22dc568a0a39.json'
BUCKET_NAME = 'vnstock-data'

tiker = listing_companies()['ticker'].tolist()

today = datetime.today().strftime('%Y-%m-%d')
print(last_xd(1))

data = pd.DataFrame()
index = 0
for item in tiker:
    try:
        index+=1
        print('Process item {} : {}'.format(index,item))
        item_data = stock_historical_data(item,last_xd(4),today)
        item_data['Ticker'] = item
        item_data = item_data.set_index('Open')
        data = pd.concat([data, item_data])
    except:
        continue

if (data.empty==False):
    data.to_csv('data-{}.csv'.format(last_xd(1)), header=False)
# 23/03/2023

try:
    storage_client = storage.Client.from_service_account_json(PATH_KEY)
    bucket = storage_client.get_bucket(BUCKET_NAME)
    bucket.blob('data-{}.csv'.format(last_xd(1))).upload_from_filename('data-{}.csv'.format(last_xd(1)))
    print('Added new data!')
except:
    print('No new data!')

