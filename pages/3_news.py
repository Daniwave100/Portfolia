import streamlit as st
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_agents.digest_agent import DigestAgent

st.title("Daily News")

digest_agent = DigestAgent()
result = digest_agent.run_agent()
st.markdown(result)