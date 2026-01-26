import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai import OpenAI
from agents import Agent, Runner, FunctionTool, function_tool
from config.settings import OPENAI_API_KEY, MARKET_AUX_KEY
from services.portfolio_service import PortfolioService
import http.client, urllib.parse
import json
from datetime import datetime
from zoneinfo import ZoneInfo

class DigestAgent:
    def __init__(self):
        self.portfolio_service = PortfolioService("test")
        self.tickers = [position["ticker"] for position in self.portfolio_service.sync_positions_with_alpaca()]
        self.model = "gpt-5.2"
        self.prompt = f"""
        You are a stock portfolio news summarizer.
        You will have access to a person's portfolio information, including stock positions, number of stocks, and more.
        You will write up 1-2 paragraph general important world news as it relates to the market.
        You will then include 2-4 paragraphs on important news related to each stock.
        You will return the sources you used for your output.

        The stocks in the portfolio you will evaluate are {self.tickers}
        """

    # tool to search web
    # @function_tool
    def search_web_for_news(self):
        all_news = ""
        i = 0
        for ticker in self.tickers:
            # just following marketaux documentation for this
            conn = http.client.HTTPSConnection("api.marketaux.com")
            params = urllib.parse.urlencode({
                "api_token": MARKET_AUX_KEY,
                "symbols": ticker,
                "limit": 3
            })
            conn.request("GET", "/v1/news/all?{}".format(params))
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            all_news += f"Article {i}:\n {data}" 
            i += 1
        return all_news

    # run agent
    def run_agent(self):
        all_news = self.search_web_for_news()
        digest_agent = Agent(name="Digest Agent", 
                             instructions=self.prompt, 
                             model=self.model)
        result = Runner.run_sync(digest_agent, all_news)
        # convert result into string. “If result has an attribute named final_output, return it”
        digest_text = getattr(result, "final_output", None)
        # get EST time
        now_et = datetime.now(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %H:%M:%S %Z")
        return {"Time": now_et, "Model": self.model,"Tickers": self.tickers, "LLM digest": digest_text}

    
if __name__ == "__main__":
    agent = DigestAgent()
    print(agent.tickers)

    result = agent.run_agent()
    print(result)
    print(type(result))



