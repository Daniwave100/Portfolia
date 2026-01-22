import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import StockHistoricalDataClient
from datetime import datetime, timedelta
from config.settings import ALPACA_API_KEY, ALPACA_SECRET_KEY
import streamlit as st
import pandas as pd

class PortfolioService:
    def __init__(self, db_connection):
        self.db = db_connection
        self.trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        self.data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)

    def sync_positions_with_alpaca(self):
        """
        Fetch positions from alpaca for dashboard display
        """
        raw_positions = self.trading_client.get_all_positions()
        positions = []
        # portfolio chart on top, name, num. of shares, small daily chart, total gain/loss all time (customizable like robinhood)
        for position in raw_positions:
            clean_position = {
                "ticker": position.symbol,
                "company_name": position.symbol,
                'shares': float(position.qty),
                'current_price': float(position.current_price),
                'cost_basis': float(position.cost_basis),
                'market_value': float(position.market_value),
                'unrealized_pl': float(position.unrealized_pl),
                'unrealized_pl_percent': float(position.unrealized_plpc) * 100,
                'avg_entry_price': float(position.avg_entry_price),
                "change_today": float(position.change_today)
            }
            positions.append(clean_position)
        
        return positions
    
    def get_day_chart(self, ticker, hours=6):
        """
        Get data for the day to make daily chart
        """
        request = StockBarsRequest(
            symbol_or_symbols = ticker,
            timeframe=TimeFrame.Hour, # basically TimeFrame.Day is Alpaca's way of saying day timeframe
            start = datetime.now() - timedelta(hours=hours), # look up what this does
            end = datetime.now()
        )

        stock_bars = self.data_client.get_stock_bars(request)
        print(stock_bars)
        chart_data = []
        for bar in stock_bars[ticker]:
            chart_data.append({
                "timestamp": bar.timestamp,
                "open": float(bar.open),
                "low": float(bar.low),
                "high": float(bar.high),
                "close": float(bar.close),
                "volume": int(bar.volume)
            })

        print()
        df = pd.DataFrame(chart_data)

        return df
    
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
    chart_data = portfolio.sync_positions_with_alpaca()
    print(chart_data)
    
