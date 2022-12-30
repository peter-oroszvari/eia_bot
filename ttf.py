import requests
import json

class DataFetcher:
    def fetch_ttf_data(self):
        url = 'https://www.theice.com/marketdata/DelayedMarkets.shtml?getContractsAsJson=&productId=4331&hubId=7979'
        response = requests.get(url)

        # You can access the response body using the `text` property
        response_body = response.text

        # You can also access the status code of the response using the `status_code` property
        response_status_code = response.status_code

        # If the request was successful (status code 200), you can use the response body as needed
        if response_status_code == 200:
            # Parse the response body as JSON
            response_data = json.loads(response_body)
        
        # Create a list to store the market data
            market_data = []

        # Iterate through the list of dictionaries in the response data
        for item in response_data[:10]:
            # Extract the marketStrip and lastPrice values
            market_strip = item['marketStrip']
            last_price = item['lastPrice']
            
            # Print the values
            # print(f'marketStrip: {market_strip}, lastPrice: {last_price}')
    # Add the values to the market data list
            market_data.append({'Futures: ': market_strip, 'Last Price: ': last_price})
        
        return market_data





