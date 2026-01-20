# Portfolia

A comprehensive portfolio management and stock analysis platform built with Streamlit.

## Overview

Portfolia is an intelligent investment management application that combines portfolio tracking, stock analysis, and automated reporting to help investors make informed decisions.

## Features

### 📊 Portfolio Dashboard
- Manual stock position management
- Real-time stock charts and position tracking
- Portfolio risk analysis engine
- Persistent data storage in SQL database
- Future integration with paper trading platforms

### 📈 Stock Analysis Service
- Multi-timeframe analysis (short, medium, long-term)
- Trend analysis and volatility metrics
- Risk assessment for investment opportunities
- AI-powered insights

### 📧 Email Digest Service
- Daily portfolio summaries
- Risk alerts and notifications
- "What changed" updates
- Personalized investment insights

## Tech Stack

- **Frontend**: Streamlit
- **Database**: SQL (user data, holdings, preferences)
- **Vector Database**: Memory storage for historical decisions and news summaries
- **AI**: OpenAI API for analysis and insights
- **Python**: Core application logic

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Mac/Linux
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=your_database_url
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Project Status

🚧 Under active development

## License

MIT License