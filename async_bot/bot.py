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
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer("/start - Start\n"
                         "/get_prices - Get prices in your city\n"
                         "/options - Accessible cities and banks\n"
                         "/help - Get detailed information about the bot")


@dp.message(Command("get_prices"))
async def select_city(message: Message) -> None:
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
async def select_currency(callback: types.CallbackQuery) -> None:
    if callback.data.startswith("city_"):
        city_code: str = callback.data.split('city_')[1]
        city_currency: str = city_code  # If the string doesn't change, it will continue to have the same reference
        if "_" in city_currency:  # For city names consisting of several words
            city_currency: list = city_currency.split("_")
            city_currency: str = " ".join(city_currency)

        buttons: list = [
            InlineKeyboardButton(text="Dollar $", callback_data=f"currency_USD_{city_code}"),
            InlineKeyboardButton(text="Euro €", callback_data=f"currency_EUR_{city_code}")
        ]

        keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])

        await callback.message.edit_text(
            text=f"City: {city_currency}\n"
                 f"Select currency:",
            reply_markup=keyboard
        )

    elif callback.data.startswith("currency_"):
        currency_code: str = callback.data.split('_')[1]
        city_code: str = callback.data.split(f'currency_{currency_code}_')[1]

        try:
            response_json: dict = await async_get(f"http://async_api:8000/get_prices?currency={currency_code}&city={city_code}")  # noqa
            city_currency: str = response_json["city_currency"]
            if "_" in city_currency:  # For city names consisting of several words
                city_currency: list = city_currency.split("_")
                city_currency: str = " ".join(city_currency)
            date_time: str = response_json["date_time"]
            prices_with_banks: str = response_json["res"]
            denial_of_responsibility: str = ("The author is not responsible for the accuracy of the provided data on exchange rates.\n"  # noqa
                                             "The information provided does not constitute an advertisement or individual investment recommendation.")  # noqa
            res_text: str = city_currency + "\n" + date_time + "\n\n" + prices_with_banks + "\n\n\n" + denial_of_responsibility  # noqa
            await callback.message.edit_text(text=res_text)
        except (ConnectionError, ClientConnectorError, ValueError) as err:
            print(err)
            await callback.message.edit_text(text="Error. Please try again later :(")


@dp.message(Command("options"))
async def get_prices(message: Message) -> None:
    response_json: dict = await async_get("http://async_api:8000/options")
    cities: str = ', '.join(response_json["cities"])
    currencies: str = ', '.join(response_json["currencies"])
    await message.answer(f"List of supported cities and currencies:\n"
                         f"Cities: {cities}.\n"
                         f"Currencies: {currencies}.")


@dp.message(Command("help"))
async def get_prices(message: Message) -> None:
    await message.answer("This bot is designed to compare prices for the purchase of cash currency in different banks and cities.\n"   # noqa
                         "We do not collect, store or process your personal data!\n"
                         "The user uses the service at his own risk. The service is provided “as is”. "
                         "The author does not accept any responsibility.")


async def main() -> None:
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)  # run events dispatching


if __name__ == "__main__":
    # logging_basicConfig(level=INFO, stream=stdout)
    asyncio_run(main())
