import io
import re
import PyPDF2
import os,sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.http_request import HttpRequests

def extract_oil_weekly_text():

    # Use requests to download the PDF
    response = HttpRequests.get('https://ir.eia.gov/wpsr/wpsrsummary.pdf')
    # url = "https://ir.eia.gov/wpsr/wpsrsummary.pdf"
    # response = requests.get(url)

    # Open the PDF file using a buffer
    buffer = io.BytesIO(response.content)

    # Create a PDF object
    pdf = PyPDF2.PdfReader(buffer)

    # Initialize an empty string to store the text
    text = ""

    # Iterate over all pages
    for page in range(len(pdf.pages)):
        text += pdf.pages[page].extract_text()

    # Clean up the text
    text = re.sub(r"\s+", " ", text)

    return text