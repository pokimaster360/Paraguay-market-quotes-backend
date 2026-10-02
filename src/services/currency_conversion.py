from enum import Enum

from src.models.currency import Currency
from src.models.Trend import Trend

from dataclasses import asdict



def ConvertCurrencies(data: dict):
    '''
    Convert an Diccionary into an obj Currency
    example:
    'soup' = {
        "name" = ...    -->   'soup' = Currrency(...)
    }
    '''
    currencies = {}


    # "CambiosChaco": {
    #     "USD": {
    #         "name": "USD",
    #         "buy": "5870",
    #         "sell": "5940",
    #         "buy_trend": 1,
    #         "sell_trend": 0
    #     }
    # },


    
    # Source -> Casa =  "cambiosChaco"
    # Data -> Casa.Currencies =  {USD, RLS...}

    for source, data in data.items():
        currencies[source] = {}

        if data is None:
            continue
        

        for key in data:
            data_currency = data[key]

            currencies[source][key] = Currency(
                name=           data_currency['name'],
                buy=            data_currency['buy'],
                sell=           data_currency['sell'],
                buy_trend=      (Trend(data_currency['buy_trend'])          if data_currency['buy_trend'] is not None else None),
                sell_trend=     (Trend(data_currency['sell_trend'])         if data_currency['sell_trend'] is not None else None),
                exchange_type=           data_currency['exchange_type'],
                house= data_currency['house']
            )

    return currencies


def Currencies_To_Dic(data: list[Currency] | Currency) -> list[dict] | dict:
    final_data = []


    if type(data) is Currency:
        final_data = {}

        final_data = {
            "house": data.house,
            "name": data.name,
            "buy": data.buy,
            "sell": data.sell,
            "buy_trend": data.buy_trend,
            "sell_trend": data.sell_trend,
            "created_at": data.created_at,
            "exchange_type": data.exchange_type.value,
        }
        

        
        

    elif type(data) is list:
        for currency in data:
            final_data.append({
                "house": currency.house,
                "name": currency.name,
                "buy": currency.buy,
                "sell": currency.sell,
                "buy_trend": currency.buy_trend,
                "sell_trend": currency.sell_trend,
                "created_at": currency.created_at,
                "exchange_type": currency.exchange_type,
            })

    return final_data