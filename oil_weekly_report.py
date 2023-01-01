import requests
import io
import re
import PyPDF2

def extract_oil_weekly_text():

    # Use requests to download the PDF
    url = "https://ir.eia.gov/wpsr/wpsrsummary.pdf"
    response = requests.get(url)

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