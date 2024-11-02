import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

logger = get_logger(__name__)


class TTFController:
    def __init__(self):
        self.url = "https://www.theice.com/products/27996665/Dutch-TTF-Gas-Futures/data"

    def get_formatted_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            table = soup.find("table", {"id": "settlePrice"})
            rows = table.find_all("tr")[1:6]  # Get first 5 rows after header

            formatted_data = "Dutch TTF Natural Gas Futures:\n\n"
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    month = cols[0].text.strip()
                    price = cols[1].text.strip()
                    formatted_data += f"{month}: {price}\n"

            return formatted_data

        except Exception as e:
            logger.error(f"Error fetching TTF futures data: {str(e)}")
            return "Error fetching TTF futures data. Please try again later."
