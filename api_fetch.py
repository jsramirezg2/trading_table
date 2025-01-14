import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Define the API endpoint and headers
url = 'https://mapi.boomfi.xyz/v1/subscriptions?status=Active' # change customers to subscriptions after testing the api
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
}

def fetch_customer_ids():
    """
    Fetches the customer IDs from the external API and returns them as a list.
    """
    # Make the GET request
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code}")
        return []

    fetched_data = response.json()

    if 'data' not in fetched_data or 'items' not in fetched_data['data']:
        print("Invalid data structure received from the API.")
        return []

    fetched_data_items = fetched_data['data']['items']
    customers_list = []

    # Add customer_ident to the list
    for item in fetched_data_items:
        customers_list.append(item["customer"]["reference"])
        print(item["customer"]["reference"])

    return customers_list


if __name__ == '__main__':
    fetch_customer_ids()