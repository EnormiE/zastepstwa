import requests
from bs4 import BeautifulSoup
# from unidecode import unidecode
# import json
import re
# from datetime import datetime
# import urllib.parse

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
page = requests.get(url, headers= headers)
parsed_page = BeautifulSoup(page.text, 'html.parser')
klasa = '2 LPa'
parsed_klasa = parsed_page.find_all(string=re.compile(klasa))
for zastepstwo in parsed_klasa:
    zastepstwo = zastepstwo.parent.parent.contents
    print('Lekcja: ' + ' '.join(zastepstwo[1].text.split()))
    print('Opis: ' + ' '.join(zastepstwo[3].text.split()))
    print('Zastępca: ' + ' '.join(zastepstwo[5].text.split()))
    print('Uwagi: ' + ' '.join(zastepstwo[7].text.split()))
# script = parsed_page.find('script', type='application/ld+json')