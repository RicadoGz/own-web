import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import certifi

url = "https://companiesmarketcap.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

async def fetch(session, url):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        return await response.text()

async def fetch_company_codes():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find_all('div', class_='company-code')
        return [code.text.strip() for code in title]

async def main():
    company_codes = await fetch_company_codes()
    return company_codes
def get_company_codes():
    return asyncio.run(main())

company_codes = get_company_codes()



