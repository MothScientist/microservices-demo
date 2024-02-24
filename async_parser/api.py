from fastapi import FastAPI
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
    return datetime.now(timezone(timedelta(hours=3))).strftime("%H:%M %d/%m/%Y")


@app.get("/get_prices")
async def get_prices_route(currency: str, city: str) -> dict:
    curr_datetime: str = await get_datetime()
    res: str = await async_parser(currency, city)
    return {"city_currency": f"{city} | {currency}",
            "date_time": curr_datetime,
            "res": res}


@app.get("/options")
async def options_route() -> dict:
    return {"cities": [CITY_1,
                       CITY_2,
                       CITY_3,
                       CITY_4,
                       CITY_5],

            "currencies": ["USD",
                           "EUR"]
            }
