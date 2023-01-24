import json
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.http_request import HttpRequests

class TTFModel:
    @staticmethod
    def fetch_ttf_data():
        url = 'https://www.theice.com/marketdata/DelayedMarkets.shtml?getContractsAsJson=&productId=4331&hubId=7979'
        response = HttpRequests.get(url)

        # Parse the response body as JSON
        response_data = json.loads(response.text)

        # Create a list to store the market data
        market_data = []

        # Iterate through the list of dictionaries in the response data
        for item in response_data[:10]:
            # Extract the marketStrip and lastPrice values
            market_strip = item['marketStrip']
            last_price = item['lastPrice']

            # Add the values to the market data list
            market_data.append({'Futures: ': market_strip, 'Last Price: ': last_price})

        return market_data
