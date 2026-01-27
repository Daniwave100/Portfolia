# Portfolia

A comprehensive portfolio management and stock analysis platform built with Streamlit.

## Overview

Portfolia is an intelligent investment management application that combines portfolio tracking, stock analysis, and automated reporting to help investors make informed decisions.

## Features

### 📰 Daily Market Digest (Live)
- Automated daily market and news digest generated using LLMs
- Scheduled execution via **cron on AWS EC2**
- Ingests external news and market data through APIs
- Stores structured daily digests as JSON in **Amazon S3**
- Designed for reuse by downstream applications (e.g. Streamlit)

### 📊 Portfolio Dashboard (In Progress)
- Streamlit-based interactive dashboard
- Planned portfolio position tracking and summaries
- Will consume precomputed digests from S3
- Visualizations and portfolio insights under development

### 📈 Stock Analysis Service (In Progress)
- Planned multi-timeframe stock analysis
- Trend and volatility metrics
- AI-assisted investment insights
- Future integration with additional market data APIs

## Tech Stack

### Cloud & Infrastructure
- **AWS EC2** – compute for scheduled batch jobs
- **Ubuntu Linux** – operating system
- **Cron** – native Linux scheduler for automation
- **Amazon S3** – durable object storage for daily digests

### Backend & AI
- **Python** – core application logic
- **Virtual Environments (venv)** – dependency isolation
- **OpenAI API** – LLM-powered summarization and analysis
- **External APIs** – news and market data ingestion

### Frontend
- **Streamlit** – interactive web application (in development)

## Project Status

🚧 Under active development

## License

MIT License
