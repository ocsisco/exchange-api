import datetime
import requests
from colorama import Fore
from bs4 import BeautifulSoup

from sources import *


class Coin:

    def __init__(self):
        self.name = "Coin"
        self.valueInDollars = float
        self.datetime = None

    def get_value(self,source):

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

            self.name = name_coin
            self.valueInDollars = value
            self.datetime = datetime.datetime.now()

        except:

            if __name__ == "__main__":
                print (Fore.RED+(str("This source with id:") + str(id_source) + " not contain valid value"))
                print ("this value is " +Fore.YELLOW+ str(value) +Fore.RED+ " this is not a float" +Fore.RESET)



def wrongValuesFilter(coins,name_coin,average,tolerance):
    tolerance = tolerance
    okaycoins = []

    for coin in coins:
        if coin.name == name_coin:
            if coin.valueInDollars < average + tolerance and coin.valueInDollars > average - tolerance:
                okaycoins.append(coin)

    return okaycoins



def average(nameCoinSource):
    all_eur_values = []
    coin = Coin()
    for source in nameCoinSource:
        coin.get_value(source)
        all_eur_values.append(coin.valueInDollars)

    total_value = 0.0
    for value in all_eur_values:
        total_value = total_value + value
    value = total_value/len(all_eur_values)

    coin.valueInDollars = value
    return coin


eur = average(EUR)
gbp = average(GBP)






#print(coin.valueInDollars)


"""average_eur = average(source_coins,"EUR")
#print(average_eur)
okaycoins_eur = wrongValuesFilter(source_coins,"EUR",average_eur,0.05)
#print(okaycoins_eur)
newaverage = average(okaycoins_eur,"EUR")
print(newaverage)

coin = Coin()
coin.name = "EUR"
coin.valueInDollars = newaverage
coin.datetime = datetime.datetime.now()
"""