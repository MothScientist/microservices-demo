from aiohttp import ClientSession


async def async_get(url) -> dict:
    """
    Sends a get request to the specified url and if the response code is 200, it returns a dictionary with data,
    otherwise it raises a ConnectionError.
    :param url: URL of your API service
    :return: response in JSON (dictionary) format
    """
    async with ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:  # Checking http status code
                response_json: dict = await response.json()  # Converting response to dict data type
                return response_json
            raise ConnectionError("The site does not respond to the request")
