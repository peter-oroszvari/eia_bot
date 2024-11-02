import requests
from bs4 import BeautifulSoup
from utils.logger import get_logger

logger = get_logger(__name__)


def get_natgasweather():
    try:
        url = "http://www.natgasweather.com"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        headline = soup.find("h1", class_="entry-title").text.strip()
        daily_update = soup.find("div", class_="entry-content").p.text.strip()

        return {"headline": headline, "daily_update": daily_update}

    except Exception as e:
        logger.error(f"Error fetching natgasweather data: {str(e)}")
        return {
            "headline": "Error fetching data",
            "daily_update": "Please try again later.",
        }
