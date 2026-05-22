import httpx
import logging

logger = logging.getLogger(__name__)


async def get_stock_data(symbol: str, api_key: str):
    """使用 Alpha Vantage API 获取实时报价"""
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": api_key
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=10.0)
            data = response.json()
        except Exception as e:
            logger.error(f"Alpha Vantage 请求失败: {e}")
            return None

    quote = data.get("Global Quote")
    if not quote:
        logger.warning(f"无效响应: {data}")
        return None

    try:
        current_price = float(quote.get("05. price", 0))
        previous_close = float(quote.get("08. previous close", 0))
        change_percent = 0
        if previous_close:
            change_percent = round((current_price - previous_close) / previous_close * 100, 2)

        return {
            "symbol": symbol.upper(),
            "price": current_price,
            "volume": int(quote.get("06. volume", 0)),
            "open": float(quote.get("02. open", 0)),
            "high": float(quote.get("03. high", 0)),
            "low": float(quote.get("04. low", 0)),
            "change_percent": change_percent
        }
    except (ValueError, TypeError) as e:
        logger.error(f"解析数据失败: {e}")
        return None