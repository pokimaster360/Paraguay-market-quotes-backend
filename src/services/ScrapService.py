from pathlib import Path
import importlib.util
# from dataclasses import dataclass, asdict


# from app.services.currency_conversion import Currencies_To_Dic
from src.repositories.currency_repository import CurrencyRepository



debugging = False




CURRENT_DIR = Path(__file__)
BASE_DIR =  CURRENT_DIR.parent.parent
DATA_DIR = BASE_DIR / 'data' / 'market-rates.json'
SCRAPERS_DIR = BASE_DIR / 'scrapers'






repository = CurrencyRepository()


ALLOWED_CURRENCIES = {'USD','EUR'}


def UpdteData():
    houses = {}

    for archivo in SCRAPERS_DIR.glob('*.py'):
        if archivo.name == '__init__.py':
            continue

        spec = importlib.util.spec_from_file_location(archivo.stem, archivo)
        if spec is None or spec.loader is None:
            print('Spec is None', __file__)
            continue

        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)

        if not hasattr(modulo, 'get_cotization'):
            print(f'{modulo} no tiene get_cotization')
            continue

        currencies = modulo.get_cotization()

        if currencies is None:
            print(f'Empty: {archivo}')
            houses[archivo.stem] = []
            continue

        # print(currencies)

        # Filtrar acá, en un solo lugar
        if type(currencies) is dict:
            filtered = [c for c in currencies.values() if c.name in ALLOWED_CURRENCIES]
        else:
            # print(type(currencies))
            filtered = [c for c in currencies if c.name in ALLOWED_CURRENCIES]

        houses[archivo.stem] = filtered

    # Guardar todo
    for currencies in houses.values():
        for currency in currencies:
            repository.save(currency)
            # print(currency)
            # pass