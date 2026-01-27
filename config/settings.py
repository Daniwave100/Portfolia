from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")
ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
MARKET_AUX_KEY = os.getenv("MARKETAUX_KEY")
AWS_ACCESS_KEY = os.get("AWS_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = os.get("AWS_SECRET_ACCESS_KEY")
