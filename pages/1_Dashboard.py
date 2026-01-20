import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.market_data import MarketDataService
from services.portfolio_service import PortfolioService
from streamlit_searchbox import st_searchbox

st.title("📊 Portfolio Dashboard")

portfolio = PortfolioService("temp")
market_data = MarketDataService()

with st.sidebar:

    st.header("Add positions to your portfolio")
    selected_stock = st_searchbox(
        search_function=market_data.search_for_dropdown,
        placeholder="Search a ticker symbol",
        key="stock_Search"
    )
    number_of_shares = st.number_input("Number of shares:", min_value=0.0, step=1.0)
    purchase_price = st.number_input("Purchase Price:", min_value=0.0, step=1.0)

    # splitting stock to get string before first " " space character
    portfolio.add_position(selected_stock.split()[0], number_of_shares, purchase_price)
