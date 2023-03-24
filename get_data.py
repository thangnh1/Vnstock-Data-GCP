from vnstock import listing_companies, stock_historical_data
from datetime import datetime
import pandas as pd

tiker = listing_companies()['ticker'].tolist()

today = datetime.today().strftime('%Y-%m-%d')

data = pd.DataFrame()
index = 0
for item in tiker:
    index+=1
    print('Process item {} : {}'.format(index,item))
    item_data = stock_historical_data(item,'1970-01-02',today)
    item_data['Ticker'] = item
    item_data = item_data.set_index('Open')
    data = pd.concat([data, item_data])

data.to_csv('data.csv')
print(data)