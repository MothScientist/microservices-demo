FROM python:3.12.2-alpine3.18

LABEL description="This application receives data from the API using aiohttp and sends it to the user via a Telegram bot on aiogram"

COPY requirements.txt bot.py bot_requests.py .env /main/

WORKDIR /main

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]