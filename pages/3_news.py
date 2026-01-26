import streamlit as st
import sys
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_agents.digest_agent import DigestAgent

st.title("Daily News")

ET = ZoneInfo("America/New_York")

@st.cache_data
def get_digest(date_key: str) -> str:
    return DigestAgent().run_agent()

now = datetime.now(ET)
today_key = now.date().isoformat()

if now.time() < time(8, 0):
    st.info("Digest publishes at 8:00 AM ET. Open after 8:00 to generate today’s digest.")

if st.button("Refresh"):
    get_digest.clear()

st.markdown(get_digest(today_key))