from multiprocessing import Process
import sqlite3
from fastapi import FastAPI
from fastapi import requests

from scrap import loop

# Create ddbb
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS currency_exchange(id INTEGER PRIMARY KEY AUTOINCREMENT,name_coin varchar(255),datetime,coinvalue float(255));")
connection.commit()
connection.close()

# Run the loop
obtain_currency = Process(target=loop)
obtain_currency.start()

# Web server
app = FastAPI()

@app.get("/fetch-one",tags=["tasa de conversion"])
async def fetch_one(From:str,To:str):

    base = From
    result = To

    date_values = {}
    date_value = "null"

    values = {}

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (result,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

    return 




 

    return (From,To)


