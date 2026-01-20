import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.market_data import MarketDataService

class PortfolioService:
    def __init__(self, db_connection):
        self.db = db_connection
        self.market_data = MarketDataService()
    
    def add_position(self, ticker, shares=0, purchase_price=0):
        """Add stock position to portfolio"""
        # search up stock using API
        # add to database
        pass
    
    def get_portfolio_summary(self):
        """Calculate total value, gains/losses"""
        pass
    
    def calculate_risk_metrics(self):
        """Portfolio risk analysis"""
        pass

# This only runs when you execute: python services/market_data.py
# It WON'T run when you do: from services.market_data import MarketDataService
# This is basically only for testing.
if __name__ == "__main__":
    
    portfolio = PortfolioService("hi")
    portfolio.add_position("tesco")