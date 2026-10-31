# Exchange API

A small currency exchange API built with [FastAPI](https://fastapi.tiangolo.com/). It scrapes several public currency sites, averages the valid values (discarding outliers), stores them in a local SQLite database, and exposes the quotes through simple HTTP endpoints.

Exchange rates are expressed in **USD** internally (`valueInDollars`), so any pair of supported currencies can be derived from the stored values.

## Features

- Scrapes multiple sources per currency and averages the results.
- Discards values outside a configurable tolerance (default `2%`).
- Refreshes the rates every 60 seconds in a background process.
- Stores a history of values in `database.db` (SQLite).
- Interactive OpenAPI docs available at `/docs`.

## Requirements

- Python 3.10+
- The dependencies listed in `requirements.txt`

## Installation

```bash
git clone https://github.com/ocsisco/exchange-api.git
cd exchange-api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running

Start the server with Uvicorn:

```bash
uvicorn main:app --reload
```

The API is then available at `http://127.0.0.1:8000`, and the interactive documentation at `http://127.0.0.1:8000/docs`.

On the first run, `database.db` is created automatically. The background scraper needs a few seconds before the first values become available.

## Endpoints

All parameters are passed as query strings. Currency codes are case-sensitive and use ISO 4217 format (e.g. `USD`, `EUR`, `GBP`).

### `GET /fetch-one`

Convert one currency into another.

```text
/fetch-one?From=USD&To=EUR
```

```json
{
  "From": "USD",
  "To": {
    "Coin": "EUR",
    "Value": 0.948
  }
}
```

### `GET /fetch-multi`

Convert one currency into several currencies at once. Separate the target codes with commas.

```text
/fetch-multi?From=EUR&To=USD,GBP
```

```json
{
  "From": "EUR",
  "To": [
    { "Coin": "USD", "Value": 1.055 },
    { "Coin": "GBP", "Value": 0.865 }
  ]
}
```

### `GET /fetch-all`

Convert one currency into every currency currently available in the database.

```text
/fetch-all?From=USD
```

```json
{
  "From": "USD",
  "To": [
    { "Coin": "USD", "Value": 1.0 },
    { "Coin": "EUR", "Value": 0.948 },
    { "Coin": "GBP", "Value": 0.82 }
  ]
}
```

### `GET /convert`

Convert a specific amount of one currency into another.

```text
/convert?From=GBP&To=USD&Amount=10
```

```json
{
  "From": "GBP",
  "Amount": 10,
  "To": {
    "Coin": "USD",
    "Value": 12.19
  }
}
```

### `GET /currencies`

List the currencies currently available in the database, with their full names (read from `all_currencies.json`).

```text
/currencies
```

```json
{
  "EUR": "Euro",
  "GBP": "British Pound Sterling",
  "USD": "United States Dollar"
}
```

## Configuration

- **Sources and supported currencies:** edit `sources.py`. Each source is a tuple of
  `(id, currency_code, url, keyword, start_offset, end_offset)` describing where the
  value lives in the scraped page.
- **Currencies to scrape:** add them to `all_sources` in `scrap.py`.
- **Tolerance:** change the `tolerance` variable in `scrap.py` (percentage).
- **Refresh interval:** change the `time.sleep(60)` value in `scrap.py`.

## Docker

Build the image:

```bash
docker build -t exchange-api .
```

Run it (the container listens on port 8000):

```bash
docker run --rm -it -p 8000:8000 exchange-api
```

## Tests

The tests hit the real sources, so an internet connection is required:

```bash
pip install pytest
pytest
```

## Project structure

```text
main.py               FastAPI application and endpoints
scrap.py              Scraper, averaging logic and background loop
sources.py            Scraping sources and parameters
all_currencies.json   Currency codes and their full names
test/test_scrap.py    Tests for the scraper and source definitions
dockerfile            Container image definition
```

## Disclaimer

This project relies on scraping third-party websites to obtain exchange rates. It is intended for learning and personal use, not for financial or trading decisions. Third-party sites may change their HTML at any time, which can break scraping until `sources.py` is updated. Use a proper licensed market-data provider for production use.

## License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
