import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime
from tabulate import tabulate


url = 'https://rigcount.bakerhughes.com/rig-count-overview/'

try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except requests.exceptions.HTTPError as errh:
    print ("HTTP Error:",errh)
    sys.exit(1)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
    sys.exit(1)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
    sys.exit(1)
except requests.exceptions.RequestException as err:
    print ("Something went wrong:",err)
    sys.exit(1)


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

cleaned_result = []
for row in result:
    row['Last Count'] = row['Last Count'].replace('\n', ' ').replace('\t', '')
    row['Date of Prior Count'] = row['Date of Prior Count'].replace('\n', ' ').replace('\t', '')
    row["Date of Last Year's Count"] = row["Date of Last Year's Count"].replace('\n', ' ').replace('\t', '')
    cleaned_result.append(row)



print(cleaned_result)
print(tabulate(cleaned_result, headers='keys', tablefmt='fancy_grid', maxheadercolwidths=15))



