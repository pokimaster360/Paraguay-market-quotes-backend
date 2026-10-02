import requests
from bs4 import BeautifulSoup
import re
import json
from pprint import pprint

# import os
# import sys

# print("Archivo:", __file__)
# print("Working directory:", os.getcwd())
# print("Python path:")

# for path in sys.path:
#     print("  ", path)

from src.models.currency import Currency
from src.models import Trend






def get_cotization(url= 'https://www.cambioschaco.com.py/'):
    '''
    Gets the actual cotizations of Cambios Chaco
    '''

    try:
        # Make request
        response = requests.get(url)
        response.raise_for_status()

        # Get into the HTML
        soup = BeautifulSoup(response.text, 'html.parser')


        exchanges = soup.select('#main-exchange-content tr')




        currencys = {}

        for exchange in exchanges:
            currency = str(exchange['id']).replace('exchange-','')
            name = exchange.select_one('td a')

            buy_value = exchange.select_one('.purchase')
            sell_value = exchange.select_one('.sale')


            buy_trend = exchange.select_one('.pTrend')
            sell_trend = exchange.select_one('.sTrend')

            # Full name designation
            if name is not None:
                name = name.get_text(strip= True)
            else:
                print("Name didnt found -- exchange.select_one('td a') = None")
            #Full buy_value and sell_value designation
            if buy_value is not None:
                buy_value = buy_value.get_text(strip= True)

                buy_value = buy_value.replace('.', '')
            else:
                print("buy_value == None ----  buy_value = exchange.select_one('.purchase')")
            if sell_value is not None:
                sell_value = sell_value.get_text(strip= True)

                sell_value = sell_value.replace('.', '')
            else:
                print("sell_value == None ----  sell_value = exchange.select_one('.sale')")


            # Buy trend
            if buy_trend is not None:
                buy_trend = buy_trend.get('class')
                buy_trend = buy_trend[-1] if buy_trend else None

            # Sell trend
            if sell_trend is not None:
                sell_trend = sell_trend.get('class')
                sell_trend = sell_trend[-1] if sell_trend else None
            



            currency = currency.upper()


            
            # currencys[currency_id] = {
            #     'name': currency_id,
            #     'buy': buy_value,
            #     'sell': sell_value,
            #     'buy_trend': buy_trend,
            #     'sell_trend': sell_trend
            # }

            buy_trend = Trend.normalize_trend(buy_trend)
            sell_trend = Trend.normalize_trend(sell_trend)


            currencys[currency] = Currency(
                house= 'CambiosChaco',
                name= currency,
                buy= buy_value,
                sell= sell_value,
                buy_trend= buy_trend,
                sell_trend= sell_trend
            )


        return currencys


    except requests.RequestException as e:
        print(f'Error to get the page: {e}')
        return None
    except Exception as e:
        print(f'Error: {e}')
        return None