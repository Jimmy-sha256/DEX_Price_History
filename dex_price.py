from bit_query import BitQuery as bq

# create request client object
api_key = 'Insert BitQuery API Key Here' # BitQuery API Key
client = bq(api_key)

# print price of last trade
MREX = '0x76837d56d1105bb493cddbefeddf136e7c34f0c4'
client.dex_price(MREX)

# print price of last trade prior to date/time requested
XRX = '0xb25583e5e2db32b7fcbffe3f5e8e305c36157e54' # XRX contract address
date = '2022-12-09 09:43:56' # data/time
client.dex_price(XRX, date)


# add last dex trade price to date/time csv
# the csv file date column needs to be titled 'DateTime'
REX = '0x5e0b09b04d6990e76dfe9bf84552a940fd0be05e' # REX contract address
csv_file = 'REX-0x5e0b09b04d6990e76dfe9bf84552a940fd0be05e.csv' # csv file 
client.add_price_csv(csv_file, REX) # create new .csv