from aiohttp import ClientSession


async def async_get(url) -> dict:
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                response_json: dict = await response.json()
                return response_json
            raise ConnectionError("The site does not respond to the request")
