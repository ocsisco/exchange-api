import datetime
import requests
from colorama import Fore
from bs4 import BeautifulSoup
import sources
import time
import sqlite3

from sources import *


class Coin:

    def __init__(self):
        self.name = "Coin"
        self.valueInDollars = float
        self.datetime = None

    def __str__(self):
        return self.name + " object coin"

    def get_value(self,sources,tolerancePerCent):

        # Scrap values from sources and append in a list
        all_values = []

        for source in sources:
            print(("____________________________________________"))
            print(("")+str(source[1])+("            "))
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

                all_values.append(value)

            except:
                print (Fore.RED+(str("This source with id:") + str(id_source) + " not contain valid value"))
                print ("this value is " +Fore.YELLOW+ str(value) +Fore.RED+ " this is not a float" +Fore.RESET)


        # Extract the preaverage of the all eur values list
        total_value = 0.0
        for value in all_values:
            total_value = total_value + value
        preaverage = total_value/len(all_values)

        # Extract only coherent values, inside of the tolerance range
        all_eur_values_normalized = []
        tolerancePerCent = (tolerancePerCent*preaverage)/100
        for value in all_values:
            if value < preaverage + tolerancePerCent and value > preaverage - tolerancePerCent:
                all_eur_values_normalized.append(value)

        # Extract the average of the all eur values normalized
        total_value = 0.0
        for value in all_eur_values_normalized:
            total_value = total_value + value
        average = total_value/len(all_eur_values_normalized)

        coin = Coin()
        coin.name = name_coin
        coin.valueInDollars = average
        coin.datetime = datetime.datetime.now()

        return coin


def loop():
    while 1:


        tolerance = 5 #per cent
        coin = Coin()
        eur = coin.get_value(EUR,tolerance)
        gbp = coin.get_value(GBP,tolerance)



        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO currency_exchange(name_coin,datetime,coinvalue) VALUES(?,?,?);", str(eur.name), str(eur.datetime), float(eur.valueInDollars))

        connection.commit()
        connection.close()


        time.sleep(60)
        

if __name__=="__main__":
    loop()