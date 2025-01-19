import aiohttp
import os
from dotenv import load_dotenv
import logging

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Define the API endpoint and headers
url = 'https://mapi.boomfi.xyz/v1/subscriptions?status=Active'
headers = {
    'X-API-KEY': API_KEY,
    'accept': 'application/json',
}

async def fetch_customer_ids():
    """
    Fetches the customer IDs from the external API and returns them as a list.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                logging.error(f"Failed to fetch data: {response.status}")
                return []

            fetched_data = await response.json()

            if 'data' not in fetched_data or 'items' not in fetched_data['data']:
                logging.error("Invalid data structure received from the API.")
                return []

            fetched_data_items = fetched_data['data']['items']
            customers_list = [item["customer"]["reference"] for item in fetched_data_items]

            for customer_id in customers_list:
                logging.info(customer_id)

            return customers_list

if __name__ == '__main__':
    import asyncio
    asyncio.run(fetch_customer_ids())