import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import requests
from bs4 import BeautifulSoup
import re
import time
from deepdiff import DeepDiff
import copy

def send_mail(notification):
    SCOPES = [
        "https://www.googleapis.com/auth/gmail.send"
    ]

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(notification)
    message['to'] = 'jacak.patryk04@gmail.com'
    message['subject'] = 'Zastępstwa - Powiadomienie'
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message {message}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None

def indent(string):
    counter = '\n\t'
    new_string = ''
    start = 0
    clues = [
        "}, 'type_changes'",
        "}, 'values_changed'",
        "}, 'dictionary_item_added'",
        "}, 'dictionary_item_removed'",
        "}, 'iterable_item_added'",
        "}, 'iterable_item_removed'",
        "}, 'attribute_added'",
        "}, 'attribute_removed'",
        "}, 'set_item_added'",
        "}, 'set_item_removed'",
        "}, 'repetition_change'"
    ]
    for match in re.finditer(r"({|}, |', )", string):
        end, new_start = match.span()
        new_string += string[start:end]
        if match.group(0) == '}, ':
            counter = counter[:-2]
            for clue in clues:
                if string[end: new_start + (len(clue) - 3)] == clue:
                    counter = counter[:-1]
                    continue
        if match.group(0) == "', ":
            counter = counter[:-1]
        rep = match.group(0) + str(counter)
        new_string += rep
        start = new_start
        counter += '\t'
    new_string += string[start:]
    return new_string

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
proxy_servers = {
   'https': 'http://212.160.130.70:8080'
}
baza = {}
klasa = '5 IPa'

while True:
    notification = []
    n_baza = copy.deepcopy(baza)
    page = ''
    while page == '':
        try:
            page = requests.get(url, headers=headers, allow_redirects=True, timeout=10, proxies=proxy_servers)
            break
        except requests.exceptions.ConnectTimeout:
            print("Timeout, retry in 5s")
            time.sleep(5)
            continue
        except requests.exceptions.ConnectionError:
            print("Connection refused, retry in 30s")
            time.sleep(30)
            continue
    parsed_page = BeautifulSoup(page.text, 'html.parser')
    dni = parsed_page.find_all(string=re.compile('Zastępstwa w dniu'))
    for dzien in dni:
        dzien = re.search('dniu (.+?)\n', dzien).group(1)
        n_baza[dzien] = {}
        parsed_klasa = parsed_page.find_all(string=re.compile(klasa))
        for zastepstwo in parsed_klasa:
            zastepstwo = zastepstwo.parent.parent.contents
            lekcja = ' '.join(zastepstwo[1].text.split())
            n_baza[dzien][lekcja] = {}
            opis = ' '.join(zastepstwo[3].text.split())
            n_baza[dzien][lekcja]['opis'] = opis
            zastepca = ' '.join(zastepstwo[5].text.split())
            n_baza[dzien][lekcja]['zastepca'] = zastepca
            uwagi = ' '.join(zastepstwo[7].text.split())
            n_baza[dzien][lekcja]['uwagi'] = uwagi
        diff = DeepDiff(baza, n_baza, verbose_level=2)
        if len(diff) > 0:
            diff = str(diff)
            diff = indent(diff)
            notification.append(diff)
            baza = copy.deepcopy(n_baza)
    # send_mail(str(diff))
    if len(notification) > 0:
        all_n = ''
        for n in notification:
            all_n = all_n + '\n' + n
        send_mail(all_n)
    if len(baza) > 2:
        print('Wykryto więcej niż dwa dni w bazie, usuwam najstarszy z dni')
        first_key = next(iter(baza))
        first_value = baza.pop(first_key)
    time.sleep(300)
