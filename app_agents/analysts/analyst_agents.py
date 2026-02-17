"""
Docstring for app_agents.analyst_agent
"""

"""
source: https://www.finra.org/investors/investing/investment-products/stocks/evaluating-stocks
Input stock
Stock/company summary

Overall questions:
    - How does the company make money?
    - Are its products/services in demand?
    - What is the competitive landscape like?
    - How much debt?

Revenue & Growth -> Look at revenue growth 3-5-10 year trend. 
    - Is it accelerating or slowing?
    - How much growth over the last 3-5-10 years? Assign metric to this.

Profitability -> Look at profit margins, return on equity, return on assets, etc.
    - Are margins improving or declining? and why

Balance Sheet Strength
    - Positive free cash flow is positive
    - How much cash does the company have on hand?
    - Cash buffer

Valuation:
    - EPS, earnings per share, calculated by dividing a company's total earnings by the number of shares, a company's earnings per share 
    allows you to compare the financial results of companies of different sizes. A higher EPS indicates greater profitability.
    
    - P/E ratio, price-to-earnings ratio, calculated by dividing the market price per share by the earnings per share, 
    helps assess whether a stock is overvalued or undervalued. 
    This ratio can be used to compare a company's valuation to its historical P/E ratio, 
    the P/E ratios of other companies in the same industry, or the overall market P/E ratio. A higher P/E ratio may indicate that a stock is overvalued, while a lower P/E ratio may suggest it is undervalued.
    
    - Price to sales ratio (P/S) calculated by dividing the market capitalization of a company by its revenue.
    This in turn can help with evaluating comanies that have not yet made a profit. 
   
    - Debt to equity ration: Calculated by dividing a company's total liabilities by total shareholder equity (total assets minus total liabilities)
    The D/E ratio allows investors to evaluate a company's leverage and how much it uses debt to fund its operations. A lower D/E ratio generally indicates a more financially stable company, 
    while a higher D/E ratio may indicate higher risk.

    
Agents:

Financial Analysis Agent
    - Input: Stock ticker
    - Output: Analysis of the stock based on the above criteria, with a final recommendation to buy, sell, or hold.

"""



"""
"news": {
  "window_days": 14,
  "raw_headlines": [...],
  "sentiment_label": "Negative",
  "sentiment_strength": "Medium",
  "themes": [
    "Guidance cut",
    "Increased competition",
    "Regulatory pressure"
  ],
  "risk_flags": [
    "SEC investigation"
  ],
  "key_points": [
    "Company lowered forward guidance.",
    "Analysts concerned about margins."
  ]
}
"""

import sys
from pathlib import Path

if __package__ in (None, ""):
  repo_root = Path(__file__).resolve().parents[2]
  sys.path.insert(0, str(repo_root))

import config.settings  # noqa: F401  (loads .env)

from app_agents.analysts.tools import compute_valuation_deterministic

if __name__ == "__main__":
    ticker = "AAPL"
    
    result = compute_valuation_deterministic(ticker)

    print("\n--- RAW STRUCTURED OUTPUT ---\n")
    print(result.model_dump())

    print("\n--- CLEAN DISPLAY ---\n")
    print(f"Ticker: {ticker}")
    print(f"P/E: {result.metrics.pe_ttm} → {result.ratings['pe_ttm']}")
    print(f"P/S: {result.metrics.ps_ttm} → {result.ratings['ps_ttm']}")
    print(f"D/E: {result.metrics.debt_to_equity} → {result.ratings['debt_to_equity']}")
    print(f"Overall Score: {result.overall_score}")
    print(f"Flags: {result.quality_flags}")