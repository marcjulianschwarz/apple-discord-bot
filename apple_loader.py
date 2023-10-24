import asyncio
import aiohttp
from lxml import html

url = "https://www.apple.com/de/newsroom/"


async def get_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            if r.status == 200:
                text = await r.text()
                return text


async def get_news():
    data = await get_data()
    tree = html.fromstring(data)

    dates = tree.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " tile__timestamp ")]/text()')
    descriptions = tree.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " tile__headline ")]/text()')
    links = tree.xpath('//ul[@class="section-tiles"]/li/a/@href')

    return [dates, descriptions, links]


async def save():
    news = await get_news()
    data_txt = news[0][0] + "\n" + news[1][0] + "\n" + "https://www.apple.com" + news[2][0]
    file = open("data.txt", "w")
    file.write(data_txt)
    file.close()
    return data_txt
