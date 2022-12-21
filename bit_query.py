import json
import requests
import pandas as pd

from datetime import datetime 
from dateutil.parser import parse


class BitQuery(object):


    def date_ISO8601(self, date):
        dt = parse(date, fuzzy=True)
        dt = dt.strftime("%Y-%m-%dT%H:%M:%S")
        return dt


    def __init__(self, api_key):

        self.url = "https://graphql.bitquery.io"

        self.headers = {
                'Content-Type': 'application/json',
                'X-API-KEY': api_key
                }

        self.query = ''.join([
                "query ",
                "($network: EthereumNetwork!, $token: String!, ", 
                "$limit: Int!, $offset: Int!, $before: ISO8601DateTime) ",
                "{\nethereum(network: $network) {\ndexTrades(\noptions: {desc: ",
                "[\"block.height\", \"tradeIndex\"], limit: $limit, offset: $offset}",
                "\ndate: {}\nbaseCurrency: {is: $token}\n) {\nblock(time: {before: $before}) ",
                "{\ntimestamp {\ntime(format: \"%Y-%m-%d %H:%M:%S\")\n}\nheight\n}",
                "\nbaseAmount\nbaseCurrency {\nsymbol\n}\nbase_amount_usd: baseAmount(in: USD)",
                "\nquoteAmount\nquoteCurrency {\naddress\nsymbol\n}\nquote_amount_usd:",
                "quoteAmount(in: USD)\ntradeIndex\n}\n}\n}\n",
                ])


    def set_var(self, token_address, date):

        date = self.date_ISO8601(date)

        self.variables = {
                "limit": 1,
                "offset": 0,
                "network": "bsc",
                "token": token_address,
                "before": date,
                "dateFormat": "%Y-%m-%d"
            }


    def send_req(self):

        payload = json.dumps({
           "query": self.query,
           "variables": self.variables
        })

        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        response = response.json()
        return response


    def strip_data(self, response_data):

        response = response_data['data']['ethereum']['dexTrades'][0]
        trade_amount = float(response['baseAmount'])
        quote_amount = float(response['quote_amount_usd'])

        usd_value = quote_amount / trade_amount

        data  = {
            'timestamp' : response['block']['timestamp']['time'],
            'symbol' : response['baseCurrency']['symbol'],
            'usd_price' : usd_value
            }

        return data 


    def dex_price(self, token, date=None):

        if date == None:
            dt = datetime.now()
            dt = dt.strftime("%Y-%m-%dT%H:%M:%S")
        else:
            dt = self.date_ISO8601(date)

        self.set_var(token, dt)
        data = self.strip_data(self.send_req())

        print('{} : {} ${:.20f}'.format(
            data['timestamp'],
            data['symbol'],
            data['usd_price']
            ))

        return data

        
    def add_price_csv(self, csv, token):

        print('\nFormatting CSV File {}\n'.format(csv))

        df = pd.read_csv(csv)
        new_column = []

        for index, row in df.iterrows():
          element = row['DateTime'] # Column Header
          data = self.dex_price(token, element)
          new_column.append(data['usd_price'])
    
        df['{} Price USD'.format(data['symbol'])] = new_column
        df.to_csv('*{}.csv'.format(csv))

        print('\nFile *{} Created\n'.format(csv))