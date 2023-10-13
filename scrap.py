import datetime
import requests
from bs4 import BeautifulSoup

from sources import *


class Coin:

    def __init__(self):
        self.name = "Coin"
        self.valueInDollars = float
        self.datetime = None



def scrapping_sources():

    sources = []

    for source in SOURCES:

        try:
            id_source= source[0]
            name_coin= source[1]
            url= source[2]
            keyword= source[3]
            init= source[4]
            end= source[5]

            r = requests.get(url)
            datos = r.text
            soup = BeautifulSoup(datos, "lxml")
            soup = str(soup)

            keyword_position = soup.find(keyword)
            value = soup[keyword_position + init : keyword_position + end]

            if "," in value:
                value = float(value.replace(",", "."))
            else:
                value = float(value)

            print(str(value))

            temporalcoin = Coin()
            temporalcoin.name = name_coin
            temporalcoin.valueInDollars = value
            temporalcoin.datetime = datetime.datetime.now()

            sources.append(temporalcoin)

        except: print(str("This source (")+ str(id_source)+"  "+ str(value) +"    "+ url+(") not contain valid value"))

    coins = sources

    return coins



def average(coins,name_coin):
    """
    From a list of objects Coin, extract the average

    """
    
    amount = []
    for coin in coins:
        if coin.name == name_coin:
            amount.append(float(coin.valueInDollars))

    total= 0.0
    for value in amount:
        total= total + value
    average = total/(int(len(amount)))

    return average



def wrongValuesFilter(coins,name_coin,average,tolerance):
    tolerance = average/(tolerance/100)
    okaycoins = []

    for coin in coins:
        if coin.name == name_coin:
            if coin.valueInDollars < average + tolerance and coin.valueInDollars > average - tolerance:
                okaycoins.append(coin)

    return okaycoins











source_coins = scrapping_sources()
print(source_coins)



average_eur = average(source_coins,"EUR")
print(average_eur)

okaycoins_eur = wrongValuesFilter(source_coins,"EUR",average_eur,100)
print(okaycoins_eur)

newaverage = average(okaycoins_eur,"EUR")
print(newaverage)
