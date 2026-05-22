from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    symbol: str


class StockData(BaseModel):
    symbol: str
    price: float
    volume: int
    open: float
    high: float
    low: float
    change_percent: float


class AnalysisResult(BaseModel):
    summary: str
    sentiment: str
    risk_level: str


class AnalyzeResponse(StockData, AnalysisResult):
    pass
