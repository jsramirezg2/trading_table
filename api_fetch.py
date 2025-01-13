import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Define the API endpoint and headers
url = 'https://mapi.boomfi.xyz/v1/customers'
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
}

# Make the GET request
response = requests.get(url, headers=headers)

fetched_data = response.json()

fetched_data_items = fetched_data['data']['items']
customers_list = []


for item in fetched_data_items:
    customers_list.append(item['customer_ident'])

    print(item['customer_ident'])

customer_ident = fetched_data['data']['items'][0]['customer_ident']
print(customers_list)


print(response.text)

