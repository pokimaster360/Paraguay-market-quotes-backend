import json

from src.models.currency import Currency
from src.data.connection import get_connection

from src.models.Trend import Trend


debugging = False









   


class CurrencyRepository:
    def save(self, currency: Currency):
        with get_connection() as conn:
            if debugging: print(currency)

            # 1. Search / create the Currency
            conn.execute(
                '''
                INSERT OR IGNORE INTO currencies (name)
                VALUES (?)
                ''',
                (currency.name,)
            )
            conn.execute(
                '''
                INSERT OR IGNORE INTO exchange_houses (name)
                VALUES (?)
                ''',
                (currency.house,)
            )

            # 2. Get ID
            cursor = conn.execute(
                '''
                SELECT id
                FROM currencies
                WHERE name = ?
                ''',
                (currency.name,)
            )

            
            row = cursor.fetchone()

            if row is None:
                raise ValueError(f'Moneda No Encontrada: {currency.name} Casa: {currency.house}')
            
            currency_id = row[0]



            # 3. Get House ID
            cursor = conn.execute(
                '''
                SELECT id
                FROM exchange_houses
                WHERE name = ?
                ''',
                (currency.house,)
            )

            row = cursor.fetchone()

            if row is None:
                raise ValueError(f'House Id Not found from House name: {currency.house}' f'\f TraceBack: {__file__}')


            house_id = row[0]

            if debugging: print(currency.exchange_type, currency.exchange_type.value)
            # 3. Save Currecny

            conn.execute(
                '''
                INSERT INTO currency_quotes
                (   
                    currency_id,
                    house_id,
                    buy,
                    sell,
                    buy_trend,
                    sell_trend,
                    exchange_type
                )
                VALUES (?,?,?,?,?,?,?)
                ''',
                (
                    currency_id,
                    house_id,
                    currency.buy,
                    currency.sell,
                    currency.buy_trend.value
                    if currency.buy_trend else None,
                    currency.sell_trend.value
                    if currency.sell_trend else None,
                    currency.exchange_type.value if currency.exchange_type else 'cash'
                )
            )

    def get_all(self) -> list[Currency]:
        with get_connection() as conn:
            # # ¿Hay cotizaciones?
            # print(conn.execute("SELECT * FROM currency_quotes LIMIT 5").fetchall())

            # # ¿Hay monedas?
            # print(conn.execute("SELECT * FROM currencies LIMIT 5").fetchall())

            # # ¿Hay casas?
            # print(conn.execute("SELECT * FROM exchange_houses LIMIT 5").fetchall())

            rows = conn.execute(
                '''
                SELECT
                    e.name,
                    c.name,
                    q.buy,
                    q.sell,
                    q.buy_trend,
                    q.sell_trend,
                    q.created_at,
                    q.exchange_type

                FROM currency_quotes q
                JOIN currencies c
                    ON c.id = q.currency_id
                JOIN exchange_houses e
                    ON e.id = q.house_id
                '''
            ).fetchall()


            currencies = []


            for row in rows:
                # print(row)
                currencies.append(
                    Currency(
                            house= row[0],
                            name = row[1],
                            buy = row[2],
                            sell = row[3],
                            buy_trend= Trend(row[4] if row[4] is not None else Trend.EQUAL),
                            sell_trend= Trend(row[5] if row[5] is not None else Trend.EQUAL),
                            created_at= row[6],
                            exchange_type= row[7]
                        )
                )

            
            return currencies

    def get_current(self) -> list[Currency]:
        with get_connection() as conn:


            # It gets The earliest Currencies in the Data, No repetiton
            rows = conn.execute(
                '''
                SELECT
                    e.name,
                    c.name,
                    q.buy,
                    q.sell,
                    q.buy_trend,
                    q.sell_trend,
                    q.created_at,
                    q.exchange_type
                
                FROM currency_quotes q
                JOIN currencies c
                    ON c.id = q.currency_id
                JOIN exchange_houses e
                    ON e.id = q.house_id

                WHERE q.created_at = (
                    SELECT MAX(q2.created_at)
                    FROM currency_quotes q2
                    WHERE q2.currency_id = q.currency_id
                        AND q2.house_id = q.house_id
                )
                '''
            ).fetchall()

            data: list[Currency] = []

            
            for row in rows:
                # print(row)
                data.append(Currency(
                        house= row[0],
                        name = row[1],
                        buy = row[2],
                        sell = row[3],
                        buy_trend= Trend(row[4] if row[4] is not None else Trend.EQUAL),
                        sell_trend= Trend(row[5] if row[5] is not None else Trend.EQUAL),
                        created_at= row[6],
                        exchange_type= row[7],
                ))

            # print(data)

            return data
