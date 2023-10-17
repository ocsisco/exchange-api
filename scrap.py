import datetime
import requests
from colorama import Fore
from bs4 import BeautifulSoup
import time
import sqlite3

from sources import *


# Put in coins, the currencies avaiable in this api
all_sources = [EUR,GBP]
# Put here the tolerance of values, wrong values from the sources be discarted.
tolerance = 2 #%


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

                print("-" + str(name_coin) + " " + str(value))

                all_values.append(value)

            except:
                print (Fore.RED+(str("-This source with id:") + str(id_source) + " not contain valid value"))
                print ("this value is " +Fore.YELLOW+ str(value) +Fore.RED+ " this is not a float" +Fore.RESET)


        # Extract the preaverage of the all eur values list
        total_value = 0.0
        for value in all_values:
            total_value = total_value + value
        preaverage = total_value/len(all_values)

        # Extract only coherent values, inside of the tolerance range
        all_values_normalized = []
        tolerancePerCent = (tolerancePerCent*preaverage)/100
        for value in all_values:
            if value < preaverage + tolerancePerCent and value > preaverage - tolerancePerCent:
                all_values_normalized.append(value)

        # Extract the average of the all eur values normalized
        total_value = 0.0
        average = 0.0
        for value in all_values_normalized:
            total_value = total_value + value
        try:
            average = total_value/len(all_values_normalized)

            coin = Coin()
            coin.name = name_coin
            coin.valueInDollars = average
            coin.datetime = datetime.datetime.now()
            
            for value in all_values:
                if value not in all_values_normalized:
                    print(Fore.LIGHTMAGENTA_EX+"Value: " + str(value) + " discarted, (out of tolerance)"+Fore.RESET)

            print("The average of " + str(coin.name) + " is: " + str(coin.valueInDollars))
            return coin
        
        except ZeroDivisionError:
            print(Fore.RED+"The tolerance in "+ name_coin +" is too small or one of its sources is ridiculously over or under value \nThe algorithm eliminate values outside the tolerance range, but if a value is extremely large, the average is too far from the true average and all values will be out of range; consult these sources."+Fore.RESET)

    def to_database(self):

        # Put coin in database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        cursor.execute("INSERT INTO currency_exchange(name_coin,datetime,coinvalue) VALUES(?,?,?);", (self.name,self.datetime,self.valueInDollars))
        print(Fore.GREEN+"")
        print("-Upload to database")
        print("Coin: " + str(self.name))
        print("Date: " + str(self.datetime))
        print(str("Value in dollars: ") + str(self.valueInDollars))
        print(Fore.RESET + "--------------")

        connection.commit()
        connection.close()


def loop():
    while 1:

        for sources in all_sources:
            # Check if can create value before upload to database
            try:
                coin = Coin()
                coin:Coin = coin.get_value(sources,tolerance)
                coin.to_database()
            except AttributeError: pass

        time.sleep(60)


if __name__=="__main__":
    for sources in all_sources:
        coin = Coin()
        coin.get_value(sources,5)