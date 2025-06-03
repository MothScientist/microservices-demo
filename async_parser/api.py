"""
API module that allows you to connect the parser application with the client application
"""

from fastapi import FastAPI, HTTPException
from os import getenv
from dotenv import load_dotenv
from typing import Final
from currency_parser import async_parser
from datetime import datetime, timezone, timedelta

app = FastAPI()

load_dotenv()

CITY_1: Final = getenv("CITY_1").replace("_", " ")
CITY_2: Final = getenv("CITY_2").replace("_", " ")
CITY_3: Final = getenv("CITY_3").replace("_", " ")
CITY_4: Final = getenv("CITY_4").replace("_", " ")
CITY_5: Final = getenv("CITY_5").replace("_", " ")


async def get_datetime() -> str:
    """
    Returns date and time in UTC+0 (GMT)
    :return: Time and date format HH:MM dd/mm/YYYY as a string
    """
    res: str = datetime.now(timezone(timedelta())).strftime("%H:%M %d/%m/%Y") + " " + "GMT - UTC+0"
    return res


@app.get("/get_prices")
async def get_prices_route(currency: str, city: str) -> dict:
    """
    Accepts a get request with parameters specified in the url
    :param currency:
    :param city:
    :return: data in JSON format (dictionary)
    """
    curr_datetime: str = await get_datetime()
    try:
        res: str = await async_parser(currency, city)
    except ConnectionError:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"city_currency": f"{city} | {currency}",
            "date_time": curr_datetime,
            "res": res}


@app.get("/options")
async def options_route() -> dict:
    """
    Returns static data
    :return: data in JSON format (dictionary)
    """
    return {
        "cities": [CITY_1, CITY_2, CITY_3, CITY_4, CITY_5],
        "currencies": ["USD", "EUR"]
    }
