"""
File: data_handling.py
Description: Contains functions for loading and preprocessing historical stock and options data from polygon.io API.
"""
import os
from dotenv import load_dotenv
import requests
import numpy as np

load_dotenv()
api_key = os.getenv('POLYGON_API_KEY')

def load_stock_option_data(ticker, start_date, end_date):
    link = f'https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}?apiKey={api_key}'
    response = requests.get(link)
    data = response.json()
    return data

def get_options_list(underlying_ticker, date):
    link = f'https://api.polygon.io/v3/reference/options/contracts?underlying_ticker={underlying_ticker}&as_of={date}&apiKey={api_key}'
    response = requests.get(link)
    data = response.json()
    return data['results']

def fetch_option_prices(ticker, start_date, end_date):
    options_list = get_options_list(ticker, start_date)

    # Create an array to store the results
    num_days = (end_date - start_date).days + 1
    num_options = len(options_list)
    result_array = np.zeros((num_days, num_options), dtype=object)

    # Iterate through each option and fetch prices
    for option_index, option in enumerate(options_list):
        option_symbol = option['ticker']
        option_prices = load_stock_option_data(option_symbol, start_date, end_date)

        # Extract OCLH data and store in the result array
        for day_index, day_data in enumerate(option_prices):
            result_array[day_index, option_index] = np.array([day_data['o'], day_data['c'], day_data['l'], day_data['h']])

    return result_array

# print(get_options_list('SAP', '2022-01-01'))
print(load_stock_option_data('O:SAP220121C00115000', '2022-01-01', '2022-01-05'))
