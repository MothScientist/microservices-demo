[![Docker Compose](https://github.com/MothScientist/microservices-demo/actions/workflows/build.yml/badge.svg)](https://github.com/MothScientist/microservices-demo/actions/workflows/build.yml)

## Disclaimer:
### The site URL, city names and class names of the html elements used on the site are hidden in the .env file for the author's own reasons.

#### If you want to replicate the project, then you just need to replace all parts of the code to suit your purposes.

#### The described functionality of this code is just an example and nothing more.

### What does this code do?
Using parsing (bs4 + aiohttp), it receives data from open sources about exchange rates in different cities and banks and, through an API service (FastAPI), provides this data upon request. 
The Telegram bot microservice (aiogram) receives data (aiohttp) and sends it to the user.</br></br>
You configure where and how to receive data yourself.


### For developers:
In this repository you can find for yourself:
- Organizing the structure of a microservices project
- Setting up the operation of 2 completely asynchronous microservices via FastAPI/aiohttp
- Setting up Dockerfile for each service and docker-compose.yml
- Setting up CI/CD
- Availability of bash scripts
- The code has detailed comments

### MIT License
