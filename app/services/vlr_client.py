from functools import cached_property
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from config.constants import API_HEADERS

class VlrClient:
    def __init__(self, session: ClientSession = None):
        self.session = session or ClientSession()

    async def get_html(self, url: str, params: dict = None) -> ClientResponse:
        async with self.session.get(url, params=params, headers=API_HEADERS) as response:
            response.raise_for_status()
            return await response.text()
    
    async def soupify(self, url: str, params: dict = None) -> BeautifulSoup:
        html = await self.get_html(url, params)
        return BeautifulSoup(html, "html.parser")
        
    async def close(self):
        await self.session.close()