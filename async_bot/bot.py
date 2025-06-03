"""
A module responsible for the Telegram bot, which processes user messages and responds to them.
"""

from asyncio import run as asyncio_run
from logging import basicConfig as logging_basicConfig, INFO
from sys import stdout
from os import getenv
from dotenv import load_dotenv
from typing import Final

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.bot import DefaultBotProperties

from aiohttp.client_exceptions import ClientConnectorError

from bot_requests import async_get

load_dotenv()
TOKEN: Final = getenv("BOT_TOKEN")

CITIES_CODE: tuple = (getenv("CITY_1"),
                      getenv("CITY_2"),
                      getenv("CITY_3"),
                      getenv("CITY_4"),
                      getenv("CITY_5"))

CITIES: tuple = (CITIES_CODE[0].replace("_", " "),
                 CITIES_CODE[1].replace("_", " "),
                 CITIES_CODE[2].replace("_", " "),
                 CITIES_CODE[3].replace("_", " "),
                 CITIES_CODE[4].replace("_", " "))

dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("/start - Start\n"
                         "/get_prices - Get prices in your city\n"
                         "/options - Accessible cities and banks\n"
                         "/help - Get detailed information about the bot")


@dp.message(Command("get_prices"))
async def get_prices_handler(message: Message) -> None:
    """
    This handler receives messages with `/get_prices` command
    At this stage the user selects a city
    :param message: required to return a response to the user
    :return: None
    """
    buttons: list = [
        InlineKeyboardButton(text=f"{CITIES[0]}", callback_data=f"city_{CITIES_CODE[0]}"),
        InlineKeyboardButton(text=f"{CITIES[1]}", callback_data=f"city_{CITIES_CODE[1]}"),
        InlineKeyboardButton(text=f"{CITIES[2]}", callback_data=f"city_{CITIES_CODE[2]}"),
        InlineKeyboardButton(text=f"{CITIES[3]}", callback_data=f"city_{CITIES_CODE[3]}"),
        InlineKeyboardButton(text=f"{CITIES[4]}", callback_data=f"city_{CITIES_CODE[4]}")
    ]

    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

    await message.answer("Select city:", reply_markup=keyboard)


@dp.callback_query()
async def callback_select_currency(callback: types.CallbackQuery) -> None:
    """
    This handler receives callback messages with data from the user (the inline button that he clicked)
    :param callback: Contains from whom and what message came
    :return: None
    """
    if callback.data.startswith("city_"):  # The user selects a city - we process the request
        city_code: str = callback.data.split('city_')[1]
        city_currency: str = city_code  # If the string doesn't change, it will continue to have the same reference
        if "_" in city_currency:  # For city names consisting of several words
            city_currency: list = city_currency.split("_")
            city_currency: str = " ".join(city_currency)

        buttons: list = [
            InlineKeyboardButton(text="Dollar $", callback_data=f"currency_USD_{city_code}"),
            InlineKeyboardButton(text="Euro €", callback_data=f"currency_EUR_{city_code}")
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])  # user choice of currency

        # Change the current message without sending a new one
        await callback.message.edit_text(
            text=f"City: {city_currency}\n"
                 f"Select currency:",
            reply_markup=keyboard
        )

    elif callback.data.startswith("currency_"):  # The user selects a currency after specifying the city
        currency_code: str = callback.data.split('_')[1]
        city_code: str = callback.data.split(f'currency_{currency_code}_')[1]

        try:
            response_json: dict = await async_get(f"http://async_api:8000/get_prices?currency={currency_code}&city={city_code}")  # accessed over the network inside Docker # noqa

        except (ConnectionError, ClientConnectorError, ValueError):
            # If your microservice is not responding or the site you are getting data from
            await callback.message.edit_text(text="Error. Please try again later :(")

        else:
            city_currency: str = response_json["city_currency"]
            if "_" in city_currency:  # For city names consisting of several words
                city_currency: list = city_currency.split("_")
                city_currency: str = " ".join(city_currency)

            date_time: str = response_json["date_time"]  # Current date and time -> HH:MM DD/MM/YYYY
            prices_with_banks: str = response_json["res"]  # Contains bank names, price and selected currency

            # The service is not responsible for the accuracy of the information
            denial_of_responsibility: str = ("The author is not responsible for the accuracy of the provided data on exchange rates.\n"  # noqa
                                             "The information provided does not constitute an advertisement or individual investment recommendation.\n"  # noqa
                                             "Please remember that actual prices and bank names may vary!")

            # Concatenation of strings into a single text
            res_text: str = city_currency + "\n" + date_time + "\n\n" + prices_with_banks + "\n\n" + denial_of_responsibility  # noqa

            # Change the current message without sending a new one
            await callback.message.edit_text(text=res_text)


@dp.message(Command("options"))
async def options_handler(message: Message) -> None:
    """
    Sending a message with a list of cities and currencies available in the bot
    :param message: required to return a response to the user
    :return: None
    """
    response_json: dict = await async_get("http://async_api:8000/options")  # accessed over the network inside Docker
    cities: str = ', '.join(response_json["cities"])
    currencies: str = ', '.join(response_json["currencies"])
    await message.answer(f"List of supported cities and currencies:\n"
                         f"Cities: {cities}.\n"
                         f"Currencies: {currencies}.")


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    """
    # Brief information about your service
    :param message: required to return a response to the user
    :return: None
    """
    await message.answer("This bot is designed to compare prices for the purchase of cash currency in different banks and cities.\n"   # noqa
                         "We do not collect, store or process your personal data!\n"
                         "The user uses the service at his own risk. The service is provided “as is”. "
                         "The author does not accept any responsibility.")


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)  # run events dispatching


if __name__ == "__main__":
    # logging_basicConfig(level=INFO, stream=stdout)  # output logs to console
    asyncio_run(main())
