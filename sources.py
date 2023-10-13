"""
Urls and parameters of the scrap the sources

["id","url","keyword",init,end]

id: id to identify the source
url: url of the source
keyword: keyword is a word of reference position, one and unique, i prefer select one to more near at the value is possible
init: when init the position of the value
end: when end the position of the value

USD to: (the currency of reference is USD)
"""


SOURCES = (
    [1,"EUR","https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=EUR&To=USD","USD =",6,14],
    [2,"EUR","https://themoneyconverter.com/ES/USD/EUR","USD = ",6,10],
    [3,"EUR","https://themoneyconverter.com/ES/USD/EUR","USD =",6,10],
    [4,"EUR","https://www.eleconomista.es/cruce/USDEUR","ultimo_321 last-value",20,58],
    [5,"EUR","https://wise.com/es/currency-converter/usd-to-eur-rate","text-success",14,21],

    
    
    [6,"GBP","https://www.xe.com/es/currencyconverter/convert/?Amount=1&From=GBP&To=USD","USD =",6,14],
    [7,"GBP","https://www.eleconomista.es/cruce/USDGBP","Libras Esterlinas",-5,0],
    [8,"GBP","https://themoneyconverter.com/ES/USD/GBP","1 USD",8,12],
    [9,"GBP","https://wise.com/es/currency-converter/usd-to-gbp-rate","1,00000 USD =",49,56]
)