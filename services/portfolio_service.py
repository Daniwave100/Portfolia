import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alpaca.trading.client import TradingClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame
from alpaca.data.historical.stock import StockHistoricalDataClient
from datetime import datetime, timedelta, timezone, time
from alpaca.data.enums import DataFeed
from zoneinfo import ZoneInfo
from config.settings import ALPACA_API_KEY, ALPACA_SECRET_KEY
import pandas as pd
import requests

class PortfolioService:
    def __init__(self, db_connection):
        self.db = db_connection
        self.trading_client = TradingClient(ALPACA_API_KEY, ALPACA_SECRET_KEY, paper=True)
        self.data_client = StockHistoricalDataClient(ALPACA_API_KEY, ALPACA_SECRET_KEY)
        self.headers = {
            "accept": "application/json",
            "APCA-API-KEY-ID": "PK3Q4WTORNNWXYWEBDPMTICPVI",
            "APCA-API-SECRET-KEY": "2ivo5K7TVJJSnJ7PJFSHWA3GzwcdYaJPkP7HHCU9U2ND"
        }

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

    # utilized GPT-5.2 to fix this function 
    def get_day_chart(self, ticker: str, lookback_days: int = 5, include_extended: bool = False):
        """
        1D mini chart using 1-minute bars.
        Fetches the last few days and then keeps only the latest trading session.
        """
        symbol = (ticker or "").strip().upper()
        if not symbol:
            return pd.DataFrame(columns=["timestamp", "open", "low", "high", "close", "volume"])
        end = datetime.now(timezone.utc)
        start = end - timedelta(days=lookback_days)
        request = StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=TimeFrame.Minute,
            start=start,
            end=end,
            feed=DataFeed.IEX,  # change to DataFeed.SIP if you have it
        )
        stock_bars = self.data_client.get_stock_bars(request)
        try:
            bars = stock_bars[symbol]
        except KeyError:
            bars = []
        if not bars:
            return pd.DataFrame(columns=["timestamp", "open", "low", "high", "close", "volume"])
        df = pd.DataFrame(
            [
                {
                    "timestamp": bar.timestamp,
                    "open": float(bar.open),
                    "low": float(bar.low),
                    "high": float(bar.high),
                    "close": float(bar.close),
                    "volume": int(bar.volume),
                }
                for bar in bars
            ]
        )
        # Convert to market timezone and keep only the latest session's minutes
        ny = ZoneInfo("America/New_York")
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert(ny)
        latest_day = df["timestamp"].dt.date.max()
        df = df[df["timestamp"].dt.date == latest_day]
        if include_extended:
            # Extended hours approx 4:00–20:00 ET
            start_t, end_t = time(4, 0), time(20, 0)
        else:
            # Regular session 9:30–16:00 ET
            start_t, end_t = time(9, 30), time(16, 0)
        df = df[(df["timestamp"].dt.time >= start_t) & (df["timestamp"].dt.time <= end_t)]
        return df
    
    def get_portfolio_summary(self, period="1M", timeframe="1D"):
        """Get portfolio summary with historical data for charting"""
        account = self.trading_client.get_account()

        url = f"https://paper-api.alpaca.markets/v2/account/portfolio/history?period={period}&timeframe={timeframe}"
        response = requests.get(url, headers=self.headers)
        data = response.json()

        # Build history dataframe
        history_df = pd.DataFrame({
            "timestamp": pd.to_datetime(data["timestamp"], unit="s"),
            "equity": data["equity"]
        })

        # Calculate stats
        current = float(account.equity)
        previous = float(account.last_equity)
        starting = history_df["equity"].iloc[0] if len(history_df) > 0 else current

        summary = {
            "total_equity": current,
            "cash": float(account.cash),
            "buying_power": float(account.buying_power),
            "total_gain_loss": current - starting,
            "total_gain_loss_pct": ((current - starting) / starting * 100) if starting > 0 else 0,
            "day_gain_loss": current - previous,
            "day_gain_loss_pct": ((current - previous) / previous * 100) if previous > 0 else 0
        }

        return {"summary": summary, "history": history_df}
        
    
    def calculate_risk_metrics(self):
        """Portfolio risk analysis"""
        pass

# This only runs when you execute: python services/market_data.py
# It WON'T run when you do: from services.market_data import MarketDataService
# This is basically only for testing.
if __name__ == "__main__":
    
    portfolio = PortfolioService("hi")
    chart_data = portfolio.sync_positions_with_alpaca()
    # print(chart_data)
    # print(portfolio.trading_client.get_account())

    print("summary: ", portfolio.get_portfolio_summary())
    
