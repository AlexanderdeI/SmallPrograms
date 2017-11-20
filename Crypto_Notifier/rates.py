from bs4 import BeautifulSoup
import requests


def fetch_bitcoin():
    # URL с актуальным курсом
    url = "https://www.coingecko.com/en/price_charts/bitcoin/usd"
    headers = {'User-Agent': 'Mozila/5.0'}
    bitcoin_file = requests.get(url)

    # Создаем soup-объект
    soup = BeautifulSoup(bitcoin_file.text, "html.parser")

    bitcoin_li = []

    # Извлекаем необходимые дынные из тегов
    for table in soup.find_all("table", attrs={"class": "table table-responsive mt-2"}):
        for td in table.find_all("td"):
            bitcoin_li.append(td.text)

    del bitcoin_li[3:]

    # Убираем ненужные символы из элемента списка
    bitcoin_li = list(map(lambda s: s.strip(), bitcoin_li))
    return bitcoin_li
