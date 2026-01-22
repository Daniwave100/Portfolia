import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from openai import OpenAI
from agents import Agent, Runner, FunctionTool, function_tool
from config.settings import OPENAI_API_KEY, MARKET_AUX_KEY
from services.portfolio_service import PortfolioService
import http.client, urllib.parse
import json

class DigestAgent:
    def __init__(self):
        self.prompt = """
        You are a stock portfolio news summarizer.
        You will have access to a person's portfolio information, including stock positions, number of stocks, and more.
        You will write up 1-2 paragraph general important world news as it relates to the market.
        You will then include 2-4 paragraphs on important news related to each stock.
        You will return the sources you used for your output.
        """
        self.portfolio_service = PortfolioService("test")

    def get_positions(self):
        positions = self.portfolio_service.sync_positions_with_alpaca()
        tickers = ""
        for position in positions:
            tickers += position["ticker"] + ","

        tickers = tickers[:-1]
        return tickers

    # tool to search web
    def search_web_for_news(self, tickers):
        # just following marketaux documentation for this
        conn = http.client.HTTPSConnection("api.marketaux.com")
        params = urllib.parse.urlencode({
            "api_token": MARKET_AUX_KEY,
            "symbols": tickers,
            "limit": 3
        })
        conn.request("GET", "/v1/news/all?{}".format(params))
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    # run agent
    def run_agent(self):
        tickers = self.get_positions()
        digest_agent = Agent(name="Digest Agent", instructions=self.prompt, tools=[self.search_web_for_news(tickers)])
        tickers = self.get_positions()
        result = Runner.run_sync(digest_agent, tickers)
        print(result)
        return result
    
if __name__ == "__main__":
    
    agent = DigestAgent()

    data = agent.search_web_for_news("ASTS,FCX")
    test = json.dumps(data, indent=4)
    print(test)

# okay so far we are getting 3 news articles for the stocks we have in our portfolio
# i have to look into i tmore because it seems like we're only getting news on the first stock
# it might be because the search performs on the first ticker and then the second one comes up after but we are limited to 3 artciles per call
# explore how to fix this. maybe a loop and do one ticker at a time
# maybe we have to pay?

# tomorrow we will have to extract the data in here and organize it to pass into the LLM
# the tool will have to be an agent tool
# then we refine the prompt and let the agent handle the LLM summarizing

