import requests
from utils.logger import get_logger

logger = get_logger(__name__)


class NGController:
    def __init__(self):
        self.api_url = "https://api.eia.gov/v2/natural-gas/stor/wkly/data/"
        self.api_key = "YOUR_EIA_API_KEY"  # Replace with your actual EIA API key

    def get_formatted_data(self):
        try:
            params = {
                "api_key": self.api_key,
                "frequency": "weekly",
                "data[0]": "value",
                "facets[series][]": "NW2_EPG0_SWO_R48_BCF",
                "sort[0][column]": "period",
                "sort[0][direction]": "desc",
                "offset": 0,
                "length": 5,
            }
            response = requests.get(self.api_url, params=params)
            response.raise_for_status()
            data = response.json()["response"]["data"]

            formatted_data = "Weekly Natural Gas Storage Report:\n\n"
            for entry in data:
                formatted_data += f"{entry['period']}: {entry['value']} Bcf\n"

            return formatted_data

        except requests.RequestException as e:
            logger.error(f"Error fetching natural gas storage data: {str(e)}")
            return "Error fetching natural gas storage data. Please try again later."
