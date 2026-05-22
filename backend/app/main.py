from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import AnalyzeRequest
from .analyzer import analyze_stock
from .supabase_client import save_analysis
from .config import DEEPSEEK_API_KEY
from .stock import get_stock_data
from .config import ALPHA_VANTAGE_API_KEY

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    symbol = req.symbol.upper()
    stock_data = await get_stock_data(symbol, ALPHA_VANTAGE_API_KEY)
    if not stock_data:
        raise HTTPException(status_code=404, detail="Stock not found")
    analysis = await analyze_stock(stock_data, DEEPSEEK_API_KEY)
    save_analysis(symbol, stock_data, analysis)  # 暂时注释
    return {**stock_data, **analysis}


@app.get("/health")
async def health():
    return {"status": "ok"}
