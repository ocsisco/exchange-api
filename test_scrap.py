from scrap import *

def test_value():
    eur = Coin()
    eur = eur.get_value(EUR,5)
    assert type(eur.valueInDollars) == float

def test_name():
    namecoins = [EUR,GBP]
    for namecoin in namecoins:
        coin = Coin()
        coin = coin.get_value(namecoin,5)
        assert coin.name in namecoin[1]

def test_format_sources():
    for source in EUR:
        assert len(source) == 6

