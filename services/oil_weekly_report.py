import requests
from PyPDF2 import PdfReader
from io import BytesIO
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_oil_weekly_text():
    try:
        url = "https://www.eia.gov/petroleum/weekly/pdf/wpsummary.pdf"
        response = requests.get(url)
        response.raise_for_status()

        pdf = PdfReader(BytesIO(response.content))
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

        return text

    except Exception as e:
        logger.error(f"Error extracting oil weekly report: {str(e)}")
        return "Error extracting oil weekly report. Please try again later."
