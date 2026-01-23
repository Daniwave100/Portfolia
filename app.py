import streamlit as st

pg = st.navigation({
    "Portfolia" : [
        st.Page("pages/1_Dashboard.py", title="Dashboard", icon="📊"), 
        st.Page("pages/2_StockAnalyst.py", title="Stock Analyst", icon="🧐"),
        st.Page("pages/3_news.py", title="Daily Digest", icon="📰")
    ]
})
pg.run()