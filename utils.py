import requests
import json
from bs4 import BeautifulSoup

def query_steam_market(params):
    """
    Query the Steam Community Market for a particular item.
    
    :param item_name: Name of the item to search for.
    :return: JSON response of the query.
    """
    # Define the Steam Market search URL
    base_url = "https://steamcommunity.com/market/search/render/"
    response = requests.get(base_url, params=params)
    # Make sure the request was successful
    if response.status_code != 200:
        print(f"Error: Unable to fetch data. HTTP Status Code: {response.status_code}")
        return None
    # Convert the response text to JSON
    return json.loads(response.text)

def parse_market_results_html(results_html, params):
    soup = BeautifulSoup(results_html, 'html.parser')
    # Find all listing links, which will contain the desired data
    listings = soup.find_all('a', class_='market_listing_row_link')
    parsed_data = []
    for listing in listings:
        data = {'unusual_effect':params['query']}
        # Extracting the item name
        item_name_element = listing.find('span', class_='market_listing_item_name')
        if item_name_element:
            data['item_name'] = item_name_element.text
        # Extracting the game name
        game_name_element = listing.find('span', class_='market_listing_game_name')
        if game_name_element:
            data['game_name'] = game_name_element.text
        # Extracting the item image link
        item_img_element = listing.find('img', class_='market_listing_item_img')
        if item_img_element and 'src' in item_img_element.attrs:
            data['item_img'] = item_img_element['src'] 
        # Extracting the item price details
        price_element = listing.find('span', class_='normal_price')
        if price_element:
            data['normal_price'] = price_element.text.strip()
        sale_price_element = listing.find('span', class_='sale_price')
        if sale_price_element:
            data['sale_price'] = sale_price_element.text.strip() 
        # Extracting the quantity available
        qty_element = listing.find('span', class_='market_listing_num_listings_qty')
        if qty_element:
            data['quantity_available'] = qty_element.text
        parsed_data.append(data)
    return parsed_data

def market_search(params):
    results = query_steam_market(params)
    return parse_market_results_html(results['results_html'], params) if results else None
