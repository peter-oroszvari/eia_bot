import json, re
from modules.http_request import HttpRequests

class NGModel:
    @staticmethod
    def fetch_nagtas_storage_data():
        url = 'https://ir.eia.gov/ngs/wngsr.json'
        response = HttpRequests.get(url)
        try:
            data = json.loads(re.sub('ï»¿', '', response.text))
        except json.decoder.JSONDecodeError:
            # The response is not a valid JSON object
            print("Error: the server did not return a valid JSON object")
        return data