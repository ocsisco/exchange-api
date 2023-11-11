
from multiprocessing import Process
import json
import sqlite3
import datetime
from fastapi import FastAPI
from fastapi import requests

from scrap import loop,Coin

# Create ddbb
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS currency_exchange(id INTEGER PRIMARY KEY AUTOINCREMENT,name_coin varchar(255),datetime,coinvalue float(255));")
connection.commit()
connection.close()

# Download value from ddbb
def from_db_get_value(name_coin):

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT MAX(id),name_coin,datetime,coinvalue FROM currency_exchange WHERE name_coin=? ",
        (name_coin,),
        )
    cursor = cursor.fetchall()
    connection.commit()
    connection.close()
    return cursor

# All possible ways
def all_ways(base,result):

    if base == "USD" and result == "USD":

        coin = Coin()
        coin.name = base
        coin.datetime = datetime.datetime.now()
        coin.valueInDollars = 1.0

    if base == "USD" and result != "USD":

        cursor = from_db_get_value(result)
        coin = Coin()
        coin.name = cursor[0][1]
        coin.datetime = cursor[0][2]
        coin.valueInDollars = float(cursor[0][3])

    if base != "USD" and result == "USD":

        cursor = from_db_get_value(base)
        value = float(cursor[0][3])
        value = 1/value
        coin = Coin()
        coin.name = cursor[0][1]
        coin.datetime = cursor[0][2]
        coin.valueInDollars = value

    if base != "USD" and result != "USD":

        cursor = from_db_get_value(base)
        valueBase = float(cursor[0][3])
        valueBase = 1/valueBase

        cursor = from_db_get_value(result)
        valueResult = float(cursor[0][3])
        valueResult = valueResult

        value = valueBase*valueResult

        coin = Coin()
        coin.name = cursor[0][1]
        coin.datetime = cursor[0][2]
        coin.valueInDollars = value
        
    return coin

# Run the loop
obtain_currency = Process(target=loop)
obtain_currency.start()

# Web server
app = FastAPI()
app.title = "Exchange api"
app.version = "1.0"


@app.get("/fetch-one",tags=["Tasa de conversión"])
async def fetch_one(From:str,To:str):

    base = From
    result = To

    coin = all_ways(base,result)

    return {
        "From": From,
        "To":{"Coin":To,"Value":round(coin.valueInDollars,3)}
        }


@app.get("/fetch-multi",tags=["Tasa de conversion múltiple"])
async def fetch_multi(From:str,To:str):

    base = From
    results = To.split(",")
    value_results = []

    for result in results:

        coin = all_ways(base,result) 
        value_results.append({"Coin":result,"Value":round(coin.valueInDollars,3)})

    return {
        "From": From,
        "To": value_results
        }
 

@app.get("/fetch-all",tags=["Tasa de conversión para todas las monedas disponibles"])
async def fetch_all(From:str):

    base = From
    value_results = []
    currencies = ["USD"]

    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()

    cursor.execute("SELECT DISTINCT name_coin FROM currency_exchange")
    cursor = cursor.fetchall()

    connection.commit()
    connection.close()

    for currency in cursor:
        currencies.append(currency[0])

    for result in currencies:

        coin = all_ways(base,result)   
        value_results.append({"Coin":result,"Value":round(coin.valueInDollars,3)})

    return {
        "From": From,
        "To": value_results
        }


@app.get("/convert",tags=["Convertir valor de una moneda a otra"])
async def convert(From:str,To:str,Amount:float):

    base = From
    result = To
    amount = Amount

    coin = all_ways(base,result)
    value = coin.valueInDollars * amount

    return {
    "From": From,
    "Amount": Amount,
    "To":{"Coin":To,"Value":round(value,3)}
    }


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



