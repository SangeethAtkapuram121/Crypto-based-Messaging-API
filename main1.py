import json
import pandas as pd
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
import os

from databaselink import write_to_excel

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '7',
    'convert': 'INR',
    'price_max': '10000000',
    'sort_dir': 'desc',
    'sort': 'price',
    'cryptocurrency_type': 'coins',
    'aux': 'cmc_rank'

}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '851e76ed-c973-428f-850d-6498e7bf6983',
}

session = Session()
session.headers.update(headers)
no = int(parameters['limit'])
try:
    response = session.get(url, params=parameters)
    datas = json.loads(response.text)
    allrecord = []
    for i in range(no):
        record = [i + 1, datas['data'][i]['cmc_rank'], datas['data'][i]['name'],
                  datas['data'][i]['quote']['INR']['price'], datas['data'][i]['last_updated'][:10],
                  datas['data'][i]['last_updated'][11:19]]
        allrecord.append(record)
        No = i + 1
        Rank = datas['data'][i]['cmc_rank']
        Name = datas['data'][i]['name']
        Price = datas['data'][i]['quote']['INR']['price']
        DateUpdate = datas['data'][i]['last_updated'][:10]
        TimeUpdate = datas['data'][i]['last_updated'][11:19]
        write_to_excel(No, Rank, Name, Price, DateUpdate, TimeUpdate)
    record = []
    with open('dateno.txt', 'r') as no:
        num = no.readline()
        pds = pd.read_excel(f"data{int(num) - 1}.xlsx")
        df_sorted = pds.sort_values(by='Rank', ascending=True)
        for index, row in df_sorted.iterrows():
            record.append(row[1:])
    message_starting = f"Hello User\nHere you go the top 7 CryptoTokens with prices$$\n\n\n{record}\n\nThank you so much for taking your time\nRegards Sangeeth"
    account_sid = 'ACfa631ec16730c78dfa925036a1152c8f'
    auth_token = '11e10760154eab3fea072f96d74378f3'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
            body=message_starting,
            from_="+13613219044",#"whatsapp:+1(415)523-8886",#
            to="+919381347095"
    )
    print(message.sid)
    print('The message has been sent to the user.')

except Exception as e:
    print(e)
#(ConnectionError, Timeout, TooManyRedirects)