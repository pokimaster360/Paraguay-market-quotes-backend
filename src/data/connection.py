import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'market-history.db'



def get_connection():
    return sqlite3.connect(DB_PATH)



# id
# name


# currency_quotes
# id | currency_id | buy | sell | trend

def initialize_database():
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS currencies (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')

        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS exchange_houses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
            '''
        )


        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS currency_quotes (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_id     INTEGER NOT NULL,
                house_id    INTEGER NOT NULL,
                buy     TEXT,
                sell    TEXT,
                buy_trend   INTEGER,
                sell_trend  INTEGER,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (currency_id)
                    REFERENCES currencies(id)
                FOREIGN KEY (house_id)
                    REFERENCES exchange_houses(id)
            )
            '''
        )