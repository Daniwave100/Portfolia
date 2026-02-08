# Portfolia

A comprehensive portfolio overview and stock analysis platform built with Streamlit.

## Overview

Portfolia is an investment insights platform that combines portfolio tracking, stock analysis, and automated reporting for Alpaca paper trading accounts. Future state will incorporate live brokerage accounts compatibility.

## Features

### 📊 Portfolio Dashboard (Live)
- Streamlit-based interactive dashboard
- Real-time portfolio position tracking and summaries
- All-time equity curve chart
- Individual stock charts
- Consumes precomputed digests from S3

### 📰 Daily Market Digest (Live)
- Automated daily market and news digest generated using OpenAI GPT-5.2
- Scheduled execution via **AWS EventBridge** at **8 AM EST daily**
- Runs as a **containerized Lambda function** (Docker image stored in ECR)
- Ingests external news and market data through MarketAux API
- Pulls portfolio tickers dynamically from Alpaca
- Stores structured daily digests as JSON in Amazon S3
- Consumed by the Streamlit dashboard for display

### 📈 Stock Analysis Service (In Progress)
- Planned multi-timeframe stock analysis (short-term, long-term)
- Trend and volatility metrics
- AI-assisted investment insights
- Future integration with additional market data APIs

## Tech Stack

### Cloud & Infrastructure
- **AWS Lambda** – containerized compute for daily digest generation
- **AWS ECR** – Docker image registry for Lambda container
- **AWS EventBridge** – cron scheduler triggering Lambda at 8 AM EST
- **Amazon S3** – object storage for daily digests
- **Docker** – containerization for Lambda deployment

### Backend & AI
- **Python** – core application logic
- **OpenAI API (GPT-5.2)** – LLM-powered summarization and analysis
- **OpenAI Agents SDK** – agent framework for digest generation
- **Alpaca API (alpaca-py)** – portfolio positions, equity history, and market data
- **MarketAux API** – financial news ingestion

### Frontend
- **Streamlit** – interactive web application
- **Altair** – data visualization and charting

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          AWS Cloud                                  │
│                                                                     │
│  ┌──────────────┐    8 AM EST     ┌──────────────────────────────┐  │
│  │  EventBridge  │───────────────▶│  Lambda (Digest Processor)   │  │
│  │  (Scheduler)  │   cron trigger │  - Fetches portfolio tickers │  │
│  └──────────────┘                 │  - Pulls news (MarketAux)    │  │
│                                   │  - Generates digest (OpenAI) │  │
│                                   └──────────────┬───────────────┘  │
│                                                  │                  │
│                                                  │ writes JSON      │
│                                                  ▼                  │
│                                   ┌──────────────────────────────┐  │
│                                   │  S3 Bucket                   │  │
│                                   │  portfolia-daily-digest      │  │
│                                   │  digests/YYYY-MM-DD.json     │  │
│                                   └──────────────┬───────────────┘  │
│                                                  │                  │
│  ┌──────────────────────────────┐                │ reads JSON       │
│  │  ECR                         │                │                  │
│  │  portfolia-digest-lambda     │                │                  │
│  │  (Docker image for Lambda)   │                │                  │
│  └──────────────────────────────┘                │                  │
│                                                  │                  │
└──────────────────────────────────────────────────┼──────────────────┘
                                                   │
                                                   ▼
                                    ┌──────────────────────────────┐
                                    │  Streamlit App (Local / EC2) │
                                    │  - Portfolio dashboard       │
                                    │  - Equity curve charts       │
                                    │  - Daily digest viewer       │
                                    │  - Real-time positions       │
                                    └──────────────┬───────────────┘
                                                   │
                                    ┌──────────────┴───────────────┐
                                    │        External APIs          │
                                    │  - Alpaca (positions/prices)  │
                                    │  - MarketAux (news)           │
                                    │  - OpenAI (digest generation) │
                                    └──────────────────────────────┘
```

## Project Status

🚧 Under active development

## License

MIT License