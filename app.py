import requests
from bs4 import BeautifulSoup
import json

from _bot_token import TOKEN

APPLE_URL = 'https://www.apple.com/ca/shop/refurbished/mac/macbook-pro'

def get_available_mbps():
    html = requests.get(APPLE_URL).content
    soup = BeautifulSoup(html, "html.parser")

    clue = 'window.REFURB_GRID_BOOTSTRAP ='
    for script in soup.find_all("script"):
        if clue in script.text:
            break
    else:
        raise ValueError('No window.REFURB_GRID_BOOTSTRAP script.')

    data = script.text.split(clue)[-1].split(';')[0]
    data = json.loads(data)

    macbooks = []
    for prod in data['products']:
        prod = prod['dimensions']
        if prod['refurbClearModel'] == 'macbookpro':
            macbook = ', '.join([
                prod['dimensionRelYear'],
                prod['dimensionScreensize'],
                prod['dimensionColor'],
                prod['dimensionCapacity'],
                prod['tsMemorySize'],
            ])
            macbooks.append(macbook)
            
    return macbooks
        

def send_message(text):
    END_POINT = 'https://api.telegram.org'
    bot_url = END_POINT + '/bot' + TOKEN
    send_url = bot_url + '/sendMessage'

    chat_id = 72735008

    data = {
        'chat_id': chat_id,
        'text': text
    }
    requests.post(send_url, data=data)


def handler(event, context):
    try:
        macbooks = get_available_mbps()
        message = '\n'.join(macbooks + [APPLE_URL]) 
    except Exception as e:
        message = e
    
    send_message(message)