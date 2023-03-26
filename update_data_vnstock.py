from datetime import datetime, timedelta
import time
import pandas as pd
from google.cloud import storage
import requests

PATH_KEY = 'vnstock-381809-22dc568a0a39.json'
BUCKET_NAME = 'vnstock-data'

today_val = datetime.now()

headers = {
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'DNT': '1',
        'sec-ch-ua-mobile': '?0',
        'X-Fiin-Key': 'KEY',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Fiin-User-ID': 'ID',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'X-Fiin-Seed': 'SEED',
        'sec-ch-ua-platform': 'Windows',
        'Origin': 'https://iboard.ssi.com.vn',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://iboard.ssi.com.vn/',
        'Accept-Language': 'en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7'
        }

def api_request(url, headers=headers):
    r = requests.get(url, headers).json()
    return r

def listing_companies ():
    """
    This function returns the list of all available stock symbols.
    """
    url = 'https://fiin-core.ssi.com.vn/Master/GetListOrganization?language=vi'
    r = api_request(url)
    df = pd.DataFrame(r['items']).drop(columns=['organCode', 'icbCode', 'organTypeCode', 'comTypeCode']).rename(columns={'comGroupCode': 'group_code', 'organName': 'company_name', 'organShortName':'company_short_name'})
    return df

def stock_historical_data (symbol, start_date, end_date):
    """
    This function returns the stock historical daily data.
    Args:
        symbol (:obj:`str`, required): 3 digits name of the desired stock.
        start_date (:obj:`str`, required): the start date to get data (YYYY-mm-dd).
        end_date (:obj:`str`, required): the end date to get data (YYYY-mm-dd).
    Returns:
        :obj:`pandas.DataFrame`:
        | tradingDate | open | high | low | close | volume |
        | ----------- | ---- | ---- | --- | ----- | ------ |
        | YYYY-mm-dd  | xxxx | xxxx | xxx | xxxxx | xxxxxx |

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
    """ 
    fd = int(time.mktime(time.strptime(start_date, "%Y-%m-%d")))
    td = int(time.mktime(time.strptime(end_date, "%Y-%m-%d")))
    data = requests.get('https://apipubaws.tcbs.com.vn/stock-insight/v1/stock/bars-long-term?ticker={}&type=stock&resolution=D&from={}&to={}'.format(symbol, fd, td)).json()
    df = json_normalize(data['data'])
    df['tradingDate'] = pd.to_datetime(df.tradingDate.str.split("T", expand=True)[0])
    df.columns = df.columns.str.title()
    df.rename(columns={'Tradingdate':'TradingDate'}, inplace=True)
    return df

def last_xd (day_num): # return the date of last x days
    """
    This function returns the date that X days ago from today in the format of YYYY-MM-DD.
    Args:
        day_num (:obj:`int`, required): numer of days.
    Returns:
        :obj:`str`:
            2022-02-22
    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid.
    """  
    last_xd = (today_val - timedelta(day_num)).strftime('%Y-%m-%d')
    return last_xd

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

