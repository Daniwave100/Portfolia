import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import altair as alt

from services.portfolio_service import PortfolioService
portfolio_service = PortfolioService("hi")

st.title("📊 Portfolio Dashboard")

# Period selector
period = st.radio(
    "Time Period",
    ["1W", "1M", "3M", "1A", "all"],
    horizontal=True,
    index=4
)

# Portfolio summary
data = portfolio_service.get_portfolio_summary(period=period, timeframe="1D")
summary = data["summary"]
history_df = data["history"]

# Metrics
st.metric(
    "Total Value",
    f"${summary['total_equity']:,.2f}",
    f"${summary['day_gain_loss']:,.2f} ({summary['day_gain_loss_pct']:.2f}%)"
)

# Portfolio chart
color = "#00ff00" if summary['total_gain_loss'] >= 0 else "#ff0000"

# Clean data and calculate bounds
history_df = history_df.dropna()
y_min = history_df["equity"].min()
y_max = history_df["equity"].max()
pad = (y_max - y_min) * 0.05 if y_max > y_min else 1

chart = (
    alt.Chart(history_df)
    .mark_line(color=color)
    .encode(
        x=alt.X("timestamp:T", title="Date"),
        y=alt.Y("equity:Q", title="Portfolio Value ($)", scale=alt.Scale(domain=[y_min - pad, y_max + pad]))
    )
    .properties(height=300)
)

st.altair_chart(chart, use_container_width=True)
st.divider()

# Positions
st.markdown("### Positions")
positions = portfolio_service.sync_positions_with_alpaca()

for i in range(0, len(positions), 2):
    cols = st.columns(2)

    for j, col in enumerate(cols):
        if i + j < len(positions):
            position = positions[i + j]
            df = portfolio_service.get_day_chart(position["ticker"])

            with col:
                container = st.container(border=True)
                with container:
                    st.markdown(f"### {position['ticker']}")
                    st.markdown(f"**Shares:** {position['shares']}")
                    st.markdown(f"**Avg Entry:** ${position['avg_entry_price']:,.2f}")
                    st.markdown(f"**Current Price:** ${position['current_price']:,.2f}")
                    st.markdown(f"**Total Value:** ${position['shares'] * position['current_price']:,.2f}")

                    y_min = df["close"].min()
                    y_max = df["close"].max()
                    pad = (y_max - y_min) * 0.05 if y_max > y_min else 1

                    chart = (
                        alt.Chart(df)
                        .mark_line(color="#00ff00" if (position["change_today"] >= 0) else "#ff0000")
                        .encode(
                            x=alt.X("timestamp:T", title="Time"),
                            y=alt.Y("close:Q", title="Value ($)", scale=alt.Scale(domain=[y_min - pad, y_max + pad]))
                        )
                        .properties(height=200)
                    )

                    st.altair_chart(chart, use_container_width=True)