from __future__ import annotations
import os
import requests
from typing import Optional
from .schemas import ValuationInputs, ValuationMetrics, ValuationResult
import config.settings  # Ensure we load environment variables


# =====================================================
# FETCH FUNDAMENTALS (PRICE + CORE METRICS)
# =====================================================

def fetch_fundamentals_finnhub(ticker: str) -> ValuationInputs:
    """
    Fetch real stock price and financial metrics from Finnhub.
    """

    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError("FINNHUB_API_KEY not set.")

    base_url = "https://finnhub.io/api/v1"

    # Current price
    quote_resp = requests.get(
        f"{base_url}/quote",
        params={"symbol": ticker, "token": api_key}
    )
    quote_resp.raise_for_status()
    quote_data = quote_resp.json()
    current_price = quote_data.get("c")

    # Financial metrics
    metric_resp = requests.get(
        f"{base_url}/stock/metric",
        params={"symbol": ticker, "metric": "all", "token": api_key}
    )
    metric_resp.raise_for_status()
    metric_data = metric_resp.json().get("metric", {})

    eps = metric_data.get("epsTTM")
    revenue_per_share = metric_data.get("revenuePerShareTTM")
    shares = metric_data.get("sharesOutstanding")
    market_cap = metric_data.get("marketCapitalization")
    debt = metric_data.get("totalDebt")
    equity = metric_data.get("totalEquity")

    # Convert revenue per share to total revenue
    total_revenue = None
    if revenue_per_share and shares:
        total_revenue = revenue_per_share * shares

    return ValuationInputs(
        price=current_price,
        eps_ttm=eps,
        revenue_ttm=total_revenue,
        market_cap=market_cap * 1_000_000 if market_cap else None,
        shares_outstanding=shares,
        total_debt=debt,
        total_equity=equity,
    )


# =====================================================
# FETCH 5-YEAR REVENUE CAGR
# =====================================================

def fetch_5y_revenue_cagr_finnhub(ticker: str) -> Optional[float]:
    """
    Fetch last 5 years of annual revenue and compute CAGR.
    Returns percentage value.
    """

    api_key = os.getenv("FINNHUB_API_KEY")
    if not api_key:
        raise ValueError("FINNHUB_API_KEY not set.")

    response = requests.get(
        "https://finnhub.io/api/v1/stock/financials-reported",
        params={"symbol": ticker, "freq": "annual", "token": api_key}
    )

    response.raise_for_status()
    data = response.json()
    reports = data.get("data", [])

    def extract_revenue_from_ic(ic) -> Optional[float]:
        concepts = {
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            "Revenues",
            "Revenue",
            "TotalRevenue",
        }

        if isinstance(ic, dict):
            for concept in concepts:
                value = ic.get(concept)
                if isinstance(value, (int, float)):
                    return float(value)
            return None

        if isinstance(ic, list):
            for item in ic:
                if not isinstance(item, dict):
                    continue
                concept = item.get("concept") or item.get("name") or item.get("label")
                if concept not in concepts:
                    continue
                value = item.get("value")
                if isinstance(value, (int, float)):
                    return float(value)
            return None

        return None

    year_to_revenue: dict[int, float] = {}
    for report in reports:
        report_obj = report.get("report", {}) if isinstance(report, dict) else {}
        ic = report_obj.get("ic")

        year_raw = report.get("year") if isinstance(report, dict) else None
        if year_raw is None:
            year_raw = report_obj.get("year")
        try:
            year = int(year_raw) if year_raw is not None else None
        except (TypeError, ValueError):
            year = None

        revenue = extract_revenue_from_ic(ic)
        if year is not None and revenue is not None:
            year_to_revenue[year] = revenue

    if len(year_to_revenue) < 5:
        return None

    years_desc = sorted(year_to_revenue.keys(), reverse=True)
    years_desc = years_desc[:5]
    revenue_latest = year_to_revenue[years_desc[0]]
    revenue_oldest = year_to_revenue[years_desc[-1]]

    if revenue_oldest <= 0:
        return None

    periods = max(1, len(years_desc) - 1)
    cagr = (revenue_latest / revenue_oldest) ** (1 / periods) - 1
    return round(cagr * 100, 2)


# =====================================================
# RATING FUNCTIONS
# =====================================================

def rate_pe(pe: Optional[float]) -> str:
    if pe is None:
        return "NA"
    if pe <= 20:
        return "Good"
    if pe <= 35:
        return "Neutral"
    return "Bad"


def rate_ps(ps: Optional[float]) -> str:
    if ps is None:
        return "NA"
    if ps <= 3:
        return "Good"
    if ps <= 7:
        return "Neutral"
    return "Bad"


def rate_de(de: Optional[float]) -> str:
    if de is None:
        return "NA"
    if de <= 0.8:
        return "Good"
    if de <= 2.0:
        return "Neutral"
    return "Bad"


def rate_growth(cagr_percent: Optional[float]) -> str:
    if cagr_percent is None:
        return "NA"
    if cagr_percent >= 15:
        return "Good"
    if cagr_percent >= 5:
        return "Neutral"
    return "Bad"


def score_from_rating(rating: str) -> int:
    mapping = {
        "Good": 100,
        "Neutral": 60,
        "Bad": 25,
        "NA": 50,
    }
    return mapping[rating]


# =====================================================
# MAIN DETERMINISTIC VALUATION FUNCTION
# =====================================================

def compute_valuation_deterministic(ticker: str) -> ValuationResult:

    inputs = fetch_fundamentals_finnhub(ticker)
    growth_5y = fetch_5y_revenue_cagr_finnhub(ticker)

    quality_flags = []

    # -----------------------------
    # Compute P/E
    # -----------------------------
    pe_ratio = None
    if inputs.price and inputs.eps_ttm and inputs.eps_ttm > 0:
        pe_ratio = inputs.price / inputs.eps_ttm
    else:
        quality_flags.append("INVALID_PE_DATA")

    # -----------------------------
    # Compute P/S
    # -----------------------------
    ps_ratio = None
    if inputs.market_cap and inputs.revenue_ttm and inputs.revenue_ttm > 0:
        ps_ratio = inputs.market_cap / inputs.revenue_ttm
    else:
        quality_flags.append("INVALID_PS_DATA")

    # -----------------------------
    # Compute Debt-to-Equity
    # -----------------------------
    de_ratio = None
    if inputs.total_debt and inputs.total_equity and inputs.total_equity > 0:
        de_ratio = inputs.total_debt / inputs.total_equity
    else:
        quality_flags.append("INVALID_DE_DATA")

    metrics = ValuationMetrics(
        pe_ttm=round(pe_ratio, 4) if pe_ratio else None,
        ps_ttm=round(ps_ratio, 6) if ps_ratio else None,
        debt_to_equity=round(de_ratio, 4) if de_ratio else None,
    )

    pe_rating = rate_pe(metrics.pe_ttm)
    ps_rating = rate_ps(metrics.ps_ttm)
    de_rating = rate_de(metrics.debt_to_equity)
    growth_rating = rate_growth(growth_5y)

    ratings = {
        "pe_ttm": pe_rating,
        "ps_ttm": ps_rating,
        "debt_to_equity": de_rating,
        "revenue_5y_growth": growth_rating,
    }

    # Weighting philosophy (balanced growth + valuation)
    weight_pe = 0.30
    weight_ps = 0.20
    weight_de = 0.20
    weight_growth = 0.30

    overall_score = (
        weight_pe * score_from_rating(pe_rating) +
        weight_ps * score_from_rating(ps_rating) +
        weight_de * score_from_rating(de_rating) +
        weight_growth * score_from_rating(growth_rating)
    )

    return ValuationResult(
        inputs=inputs,
        metrics=metrics,
        ratings=ratings,
        overall_score=int(round(overall_score)),
        quality_flags=(quality_flags if quality_flags else ["OK"]),
    )