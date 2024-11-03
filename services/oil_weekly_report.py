import requests
from PyPDF2 import PdfReader
from io import BytesIO
import re
from utils.logger import get_logger

logger = get_logger(__name__)


def extract_oil_weekly_text():
    url = "https://ir.eia.gov/wpsr/wpsrsummary.pdf"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        pdf = PdfReader(BytesIO(response.content))
        text = "".join(page.extract_text() for page in pdf.pages)

        # Clean up the text
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except requests.RequestException as e:
        logger.error(f"Error downloading PDF from {url}: {str(e)}")
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")

    return "Error extracting oil weekly report. Please try again later."
