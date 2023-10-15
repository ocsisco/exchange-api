from scrap import *
import pytest

def test_value():
    eur = Coin()
    eur = eur.get_value(EUR,5)
    assert type(eur.valueInDollars) == float

def test_name():
    namecoins = [EUR,GBP]
    namecoins1 = ["EUR","GBP"]
    for namecoin in namecoins:
        coin = Coin()
        coin = coin.get_value(namecoin,5)
        assert coin.name in namecoins1