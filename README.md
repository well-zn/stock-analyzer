# AI Stock Analyzer

An AI-powered stock analysis panel built with FastAPI, Vue 3, DeepSeek AI, and Supabase.

## Features

- Real-time stock data retrieval using yfinance
- AI-powered stock analysis using DeepSeek
- Historical analysis storage with Supabase
- Modern, responsive UI built with Vue 3

## Project Structure

```
stock-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI entry point
│   │   ├── config.py        # Environment configuration
│   │   ├── models.py        # Pydantic models
│   │   ├── stock.py         # Stock data fetching
│   │   ├── analyzer.py      # DeepSeek AI integration
│   │   └── supabase_client.py # Supabase storage
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.js
│   │   └── App.vue
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
```

Configure environment variables in `backend/.env`:
```
DEEPSEEK_API_KEY=your-deepseek-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

Run the backend:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Supabase Setup

Create the `stock_analyses` table in Supabase:

```sql
CREATE TABLE stock_analyses (
  id SERIAL PRIMARY KEY,
  symbol TEXT NOT NULL,
  price FLOAT,
  volume INT,
  summary TEXT,
  sentiment TEXT,
  risk_level TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## API Endpoints

- `POST /analyze` - Analyze a stock symbol
  - Request body: `{ "symbol": "AAPL" }`
  - Returns: Stock data with AI analysis

- `GET /health` - Health check endpoint

## Tech Stack

- **Backend**: FastAPI, Python
- **Frontend**: Vue 3, Vite, Axios
- **AI**: DeepSeek API
- **Database**: Supabase
- **Stock Data**: yfinance
