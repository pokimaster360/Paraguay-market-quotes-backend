from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import json


from src.repositories.currency_repository import CurrencyRepository
from src.services.currency_conversion import Currencies_To_Dic
from src.services.ScrapService import UpdteData

from src.schemas.history import HistoryPoint

DATA_RESPOSITORY = CurrencyRepository()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/api/currencies/recent')
def get_recent():
    return Currencies_To_Dic(DATA_RESPOSITORY.get_current())


# @app.get('/api/currencies/history' response_model= list[HistoryPoint])
# def get_history():
#     return Currencies_To_Dic(DATA_RESPOSITORY.get_current())