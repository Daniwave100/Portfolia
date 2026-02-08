import streamlit as st
import sys
import os
from datetime import datetime, time
from zoneinfo import ZoneInfo

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app_agents.digest_agent import DigestAgent
from services.digest_service import DigestService

st.title("📰 Daily Digest")

ET = ZoneInfo("America/New_York")
digest_service = DigestService()
digest_body = digest_service.s3_to_client()

st.markdown(digest_body["LLM digest"])