import requests
from bs4 import BeautifulSoup


def get_natgasweather():
    url = 'https://natgasweather.com/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    headline = soup.find('h5')
    ''''
    if headline:
       print(headline.text)
    else:
       print("No headline found.")
    '''

    daily_update = soup.select_one("div:nth-of-type(5) article div div section:nth-of-type(3) div div:nth-of-type(1) div:nth-of-type(3) div p")
    
    ''''
    if daily_update:
        print(daily_update.text)
     else:
        print("No daily update found.")
    '''
    return {'headline': headline.text, 'daily_update':daily_update.text}


