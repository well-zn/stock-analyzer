from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


def save_analysis(symbol: str, stock_data: dict, analysis: dict):
    record = {
        "symbol": symbol,
        "price": stock_data["price"],
        "volume": stock_data["volume"],
        "summary": analysis["summary"],
        "sentiment": analysis["sentiment"],
        "risk_level": analysis["risk_level"],
        "created_at": "now()"
    }
    supabase.table("stock_analyses").insert(record).execute()
