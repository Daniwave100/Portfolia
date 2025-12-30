import streamlit as st



pg = st.navigation({
    "Portfolia" : [st.Page("Dashboard", title="Dashboard", icon="D"), st.Page("Stock Analyst.py", title="Stock Analyst", icon="📊")]
})
pg.run()