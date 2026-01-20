import requests
import sys
import os

# Add parent directory to path so we can test this file
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import ALPHAVANTAGE_API_KEY

class MarketDataService:
    def __init__(self):
        self.api_key = ALPHAVANTAGE_API_KEY

    def search_position(self, ticker):
        """Search ticker"""
        # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
        url = f'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={ticker}&apikey={self.api_key}'
        r = requests.get(url)
        data = r.json()
        return data
    
    def search_for_dropdown(self, search_term):
        """
        Formats search results for dropdown display
        Returns: List of strings like "AAPL - Apple Inc."
        """
        if not search_term: # if nothing in search, return empty list
            return []

        results = self.search_position(search_term)

        # check for valid results
        if "bestMatches" not in results or len(results["bestMatches"]) == 0:
            return []
        
        # Format results for dropdown
        options = []
        for match in results["bestMatches"]:
            ticker = match["1. symbol"]
            name = match["2. name"]
            options.append(f"{ticker} - {name}")

        return options

# This only runs when you execute: python services/market_data.py
# It WON'T run when you do: from services.market_data import MarketDataService
# This is basically only for testing.
if __name__ == "__main__":
    service = MarketDataService()
    result = service.search_position("TSCO")
    print(result)