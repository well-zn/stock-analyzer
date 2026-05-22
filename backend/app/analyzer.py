import httpx
import json
import re


SYSTEM_PROMPT = """
你是一个股票分析 AI。请分析给定的股票数据，并仅返回一个合法的 JSON 对象，该对象必须包含以下字段：
- summary: 字符串（简要分析，1-2 句话）
- sentiment: 字符串，取值 "Bullish"（看涨）、"Neutral"（中性）或 "Bearish"（看跌）
- risk_level: 字符串，取值 "Low"（低）、"Medium"（中）或 "High"（高）
不要在 JSON 前后附加任何解释性文字。仅输出原始 JSON。
"""



async def analyze_stock(data: dict, api_key: str):
    user_content = f"""
Stock Data:
- Symbol: {data['symbol']}
- Current Price: ${data['price']}
- Change: {data['change_percent']}%
- Volume: {data['volume']}
- Day Range: ${data['low']} - ${data['high']}

Provide JSON analysis.
"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_content}
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            },
            timeout=30.0
        )
        result = response.json()
        if "error" in result:
            raise Exception(f"DeepSeek API error: {result['error']}")
        content = result["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except:
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError("LLM did not return valid JSON")
