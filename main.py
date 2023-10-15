from multiprocessing import Process
import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from scrap import loop

# Create ddbb
connection = sqlite3.connect("database.db")
cursor = connection.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS currency_exchange(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_coin varchar(255),
        datetime ,
        coinvalue float(255)
    );
    """
    )
connection.commit()
connection.close()


# Run the loop
obtain_currency = Process(target=loop)
obtain_currency.start()

# Web server
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
