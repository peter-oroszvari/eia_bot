import requests
import pandas as pd
import matplotlib.pyplot as plt
from utils.logger import get_logger

logger = get_logger(__name__)


class RigCountController:
    def __init__(self):
        self.url = "https://rigcount.bakerhughes.com/na-rig-count"

    def display_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            df = pd.read_html(response.text)[0]

            # Process the dataframe as needed
            df = df.set_index("Week")
            df = df.drop(columns=["Unnamed: 5", "Unnamed: 6"])

            # Create a plot
            plt.figure(figsize=(12, 6))
            df.plot(kind="bar")
            plt.title("Baker Hughes Rig Count Overview")
            plt.xlabel("Week")
            plt.ylabel("Count")
            plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
            plt.tight_layout()
            plt.savefig("dataframe.png")
            plt.close()

        except Exception as e:
            logger.error(f"Error fetching or processing rig count data: {str(e)}")
