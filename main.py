from multiprocessing import Process
import json
import sqlite3
from fastapi import FastAPI
from fastapi import requests

from scrap import loop,Coin

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

    if base == "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (result,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        coin = Coin()
        coin.name = cursor[0][1]
        coin.datetime = cursor[0][2]
        coin.valueInDollars = float(cursor[0][3])

    if base != "USD":

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute(
            "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
            (base,),
        )
        cursor = cursor.fetchall()

        connection.commit()
        connection.close()

        coin = Coin()
        coin.valueInDollars = float(cursor[0][3])

        coin = Coin()
        coin.name = cursor[0][1]
        coin.datetime = cursor[0][2]

    return {
        "From": From,
        "To":{"Coin":To,"Value":round(coin.valueInDollars,3)}
        }


@app.get("/fetch-multi",tags=["tasa de conversion multiple"])
async def fetch_multi(From:str,To:str):

    base = From
    result = To.split(",")
    pass
 

@app.get("/fetch-all",tags=["tasa de conversion todas monedas ddisponibles"])
async def fetch_all(From:str):
    base = From
    pass


@app.get("/convert",tags=["convertir valor de una moneda a otra"])
async def convert(From:str,To:str,Amount:float):

    base = From
    result = To
    amount = Amount

    pass


@app.get("/currencies",tags=["All currencies avaiable"])
async def currencies():

    all_currencies = open('all_currencies.json')
    all_currencies = json.load(all_currencies)
    
    avaiable_currencies = {}

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name_coin FROM currency_exchange")
    cursor = cursor.fetchall()

    connection.commit()
    connection.close()

    for currency in cursor:
        currency = currency[0]

        if currency in all_currencies:
            avaiable_currencies[currency] = all_currencies[currency]

    avaiable_currencies["USD"] = all_currencies["USD"]

    return avaiable_currencies



