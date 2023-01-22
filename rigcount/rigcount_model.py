import requests
from bs4 import BeautifulSoup

class RigCountModel:
    def __init__(self):
        self.url = 'https://rigcount.bakerhughes.com/rig-count-overview/'
    
    def get_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.HTTPError as errh:
            raise ValueError("HTTP Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            raise ValueError("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            raise ValueError("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            raise ValueError("Something went wrong:",err)
        
        # Extract the data from the <tr> elements
        table_data = []
        for row in soup.find('table').find_all('tr')[1:]:
            data = [cell.text for cell in row.find_all('td')]
            table_data.append(data)

        # Extract the headers from the <thead> element
        headers = [th.text for th in soup.find('thead').find_all('th')]

        # Create a dictionary with headers as keys and table data as values
        result = []
        for data in table_data:
            result.append(dict(zip(headers, data)))

        return result 

    def clean_data(self, data):
        cleaned_result = []
        for row in data:
            row['Last Count'] = row['Last Count'].replace('\n', ' ').replace('\t', '')
            row['Date of Prior Count'] = row['Date of Prior Count'].replace('\n', ' ').replace('\t', '')
            row["Date of Last Year's Count"] = row["Date of Last Year's Count"].replace('\n', ' ').replace('\t', '')
            cleaned_result.append(row)

        
        columns_to_keep = ['Area', 'Last Count', 'Count', 'Change from Prior Count']
        filtered_data = [{k: v for k, v in row.items() if k in columns_to_keep} for row in cleaned_result]

        return filtered_data