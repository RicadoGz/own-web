import aiohttp
import asyncio
from bs4 import BeautifulSoup
import ssl
import certifi
#  the website we want access
url = "https://companiesmarketcap.com/" 
# this will mock an laptop to acess
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

async def fetch(session, url):
    # this will generate the ssl certificate to make sure can access the website
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    async with session.get(url, headers=headers, ssl=ssl_context) as response:
        #  this will get the element from the website
        return await response.text()

async def fetch_company_codes():
    async with aiohttp.ClientSession() as session:
        # this was call the fetch function to get the element from the html
        html = await fetch(session, url)
        # change to the data can be handel
        soup = BeautifulSoup(html, "html.parser")
        #  find all comapny name
        title = soup.find_all('div', class_='company-code')
        # return whole the list
        return [code.text.strip() for code in title]

async def main():
    #  get the company code and return
    company_codes = await fetch_company_codes()
    return company_codes
def get_company_codes():
    return asyncio.run(main())

company_codes = get_company_codes()



