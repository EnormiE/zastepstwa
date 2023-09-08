import requests
from bs4 import BeautifulSoup
import re
import time

url = 'https://zstk.lublin.eu/zastepstwa/index.php'
headers = {
    'Host': 'zstk.lublin.eu',
    'Authorization': 'Basic enN0LWs6WnN0a19SMTg=',
    'Sec-Ch-Ua': '',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://zstk.lublin.eu/zastepstwa/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'close'
}
baza = {}

klasa = '2 RP'

while True:
    page = requests.get(url, headers=headers)
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    dni = parsed_page.find_all(string=re.compile('Zastępstwa w dniu'))
    for dzien in dni:
        dzien = re.search('dniu (.+?)\n', dzien).group(1)
        baza[dzien] = {}
        parsed_klasa = parsed_page.find_all(string=re.compile(klasa))
        for zastepstwo in parsed_klasa:
            zastepstwo = zastepstwo.parent.parent.contents
            lekcja = ' '.join(zastepstwo[1].text.split())
            baza[dzien][lekcja] = {}
            opis = ' '.join(zastepstwo[3].text.split())
            baza[dzien][lekcja]['opis'] = opis
            zastepca = ' '.join(zastepstwo[5].text.split())
            baza[dzien][lekcja]['zastepca'] = zastepca
            uwagi = ' '.join(zastepstwo[7].text.split())
            baza[dzien][lekcja]['uwagi'] = uwagi
    print(baza)
    time.sleep(300)
