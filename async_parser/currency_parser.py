from os import getenv
from dotenv import load_dotenv
from typing import Final

from aiohttp import ClientSession
from bs4 import BeautifulSoup


load_dotenv()

SITE_URL: Final = getenv("SITE_URL")

CITY_1: Final = getenv("CITY_1")
CITY_2: Final = getenv("CITY_2")
CITY_3: Final = getenv("CITY_3")
CITY_4: Final = getenv("CITY_4")
CITY_5: Final = getenv("CITY_5")

CODE_CITY_1: Final = getenv("CODE_CITY_1")
CODE_CITY_2: Final = getenv("CODE_CITY_2")
CODE_CITY_3: Final = getenv("CODE_CITY_3")
CODE_CITY_4: Final = getenv("CODE_CITY_4")
CODE_CITY_5: Final = getenv("CODE_CITY_5")

ELEMENT_1: Final = getenv("ELEMENT_1")
SUB_ELEMENT_1: Final = getenv("SUB_ELEMENT_1")

ELEMENT_2: Final = getenv("ELEMENT_2")
SUB_ELEMENT_2: Final = getenv("SUB_ELEMENT_2")

VAL_ELEMENT_1: Final = getenv("VAL_ELEMENT_1")
VAL_ELEMENT_2: Final = getenv("VAL_ELEMENT_2")


async def async_send_get_request(url: str) -> str:
    """
    Returns the site's response to a get request at the specified url.
    If the site is unavailable, a ConnectionError is raised.
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html: str = await response.text()
                return html
            raise ConnectionError("The site does not respond to the request")


async def async_parser(currency: str, city: str) -> str:
    """
    Parses data from a website containing information on prices for purchasing currency in different banks and cities
    :param currency: Currency code - inserted into the url
    :param city: City name - must be a key in the 'city_decode' dictionary
    :return: Response in the form of a string, indicating the passed parameters, current time and lists of banks with the purchase price  # noqa
    """
    # Dictionary used to substitute the city in the URL address, since they are indicated there in a distorted form
    city_decode: dict = {
        CITY_1: CODE_CITY_1,
        CITY_2: CODE_CITY_2,
        CITY_3: CODE_CITY_3,
        CITY_4: CODE_CITY_4,
        CITY_5: CODE_CITY_5
    }

    url: str = f"{SITE_URL}/{currency.lower()}/{city_decode[city]}/"

    html: str = await async_send_get_request(url)

    soup = BeautifulSoup(html, "lxml")
    banks: list = soup.find_all(ELEMENT_1,{SUB_ELEMENT_1: VAL_ELEMENT_1})[1:]
    prices: list = soup.find_all(ELEMENT_2, {SUB_ELEMENT_2: VAL_ELEMENT_2})

    bot_answer: str = ""

    for i in range(len(prices)):
        bot_answer += banks[i].text + ": " + prices[i].text + "\n"

    return bot_answer

# if __name__ == "__main__":
#     from asyncio import run as asyncio_run
#     print(asyncio_run(async_parser("eur", "Moscow")))
