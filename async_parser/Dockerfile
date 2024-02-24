FROM python:3.12.2-alpine3.18

LABEL description="This application parses the site (bs4) and sends this data through the FastAPI interface"

COPY requirements.txt api.py currency_parser.py .env /main/

WORKDIR /main

RUN python -m pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000