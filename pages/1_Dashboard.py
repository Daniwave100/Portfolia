import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.portfolio_service import PortfolioService
portfolio_service = PortfolioService("hi")

st.title("📊 Portfolio Dashboard")

positions = portfolio_service.sync_positions_with_alpaca()

for position in positions:
    df = portfolio_service.get_day_chart(position["ticker"])

    row = st.container(border=True, width="stretch", height="stretch")
    col1, col2 = row.columns(2)
    col1.markdown(f"##  {position['ticker']}")
    col1.markdown(f"###### {position["shares"]}")
    print(position["change_today"])
    col2.line_chart(df, x="timestamp", y="close", color= "#00ff00" if (position["change_today"] > 0) else "#ff0000")
    # hi