from scrap import *


def test_values():
    for sources in all_sources:
        coin = Coin()
        # Check if can create value before upload to database
        try:
            coin = coin.get_value(sources,tolerance)
            coin.coin_to_database()
        except AttributeError: pass
        assert type(coin.valueInDollars) == float
        assert coin.name == sources[0][1]

def test_name():
    namecoins = [EUR,GBP]
    for namecoin in namecoins:
        coin = Coin()
        coin = coin.get_value(namecoin,5)
        assert coin.name in namecoin[1]

def test_format_sources():
    for namecoin in all_sources:
        for source in namecoin:
            assert len(source) == 6
            assert type(source[0]) == int
            assert type(source[1]) == str
            assert len(source[1]) == 3
            assert "http" in source[2] 
            assert type(source[3]) == str
            assert type(source[4]) and type(source[5]) == int
