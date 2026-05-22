# AI 股票分析面板

基于 FastAPI、Vue 3、DeepSeek AI 和 Supabase 构建的 AI 股票分析面板。


- 前端页面：http://8.136.49.196:3000/
- 后端 API 文档：http://8.136.49.196:8000/docs

## 功能特点

- 使用 ALPHA_VANTAGE 获取实时股票数据
- 调用 DeepSeek 大模型进行智能分析
- 将分析记录持久化存储到 Supabase
- 基于 Vue 3 的现代化、响应式用户界面

## 项目结构


```
stock-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py         
│   │   ├── config.py       
│   │   ├── models.py        
│   │   ├── stock.py        
│   │   ├── analyzer.py      
│   │   └── supabase_client.py 
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


## 本地运行

### 后端

```bash
cd backend
pip install -r requirements.txt

Configure environment variables in `backend/.env`:
```
```
DEEPSEEK_API_KEY=your-deepseek-api-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
ALPHA_VANTAGE_API_KEY=your--key
```
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

API 接口
POST /analyze – 分析指定股票

请求体：{ "symbol": "AAPL" }

返回：包含 AI 分析结果的股票数据

GET /health – 健康检查接口

技术栈
后端：FastAPI, Python

前端：Vue 3, Vite, Axios

AI 模型：DeepSeek API

数据库：Supabase

股票数据源：ALPHA_VANTAGE


promt
```
SYSTEM_PROMPT = """
你是一个股票分析 AI。请分析给定的股票数据，并仅返回一个合法的 JSON 对象，该对象必须包含以下字段：
- summary: 字符串（简要分析，1-2 句话）
- sentiment: 字符串，取值 "Bullish"（看涨）、"Neutral"（中性）或 "Bearish"（看跌）
- risk_level: 字符串，取值 "Low"（低）、"Medium"（中）或 "High"（高）
不要在 JSON 前后附加任何解释性文字。仅输出原始 JSON。
"""
```



debug记录：
本地运行无误后部署到云服务器上，之后报错：
```
index-C5VYvyNt.js:13 TypeError: Cannot read properties of undefined (reading 'toString')
    at i (index-C5VYvyNt.js:25:6212)
    at Proxy.<anonymous> (index-C5VYvyNt.js:25:7509)
    at ar (index-C5VYvyNt.js:13:13737)
    at si.A [as fn] (index-C5VYvyNt.js:13:22998)
    at si.run (index-C5VYvyNt.js:9:2041)
    at si.runIfDirty (index-C5VYvyNt.js:9:2350)
    at rn (index-C5VYvyNt.js:13:46)
    at Ei (index-C5VYvyNt.js:13:1795)
```

将报错丢给AI，得到答案：
```
看起来是前端代码在尝试显示数据时，result 对象中某些字段是 undefined，导致调用 toString() 失败。

快速修复方案
在你的前端项目 frontend/src/App.vue 中，需要确保在 result 有数据时才显示，并对可能缺失的字段做保护。

请修改模板部分，将原本可能直接使用 {{ result.price }} 的地方改为：

vue
<div v-if="result" class="result">
  <h3>{{ result.symbol }} - ${{ result.price || 'N/A' }}</h3>
  <p>涨跌幅: {{ result.change_percent !== undefined ? result.change_percent + '%' : 'N/A' }}</p>
  <p><strong>总结：</strong>{{ result.summary || '暂无' }}</p>
  <p><strong>情绪：</strong>{{ result.sentiment || '未知' }}</p>
  <p><strong>风险等级：</strong>{{ result.risk_level || '未知' }}</p>
</div>
同时，在 analyze 方法中，确保对返回数据的处理：

javascript
const resp = await axios.post('http://8.136.49.196:8000/analyze', {
  symbol: this.symbol
});
this.result = resp.data;
console.log('API返回数据:', this.result);  // 添加日志查看实际字段
修改后重新构建前端：

cmd
cd C:\prj\stock-analyzer\frontend
npm run build
然后重启 serve（先按 Ctrl+C 停止之前的，再重新运行 serve -s dist -l 3000）。

检查后端返回的数据结构
你也可以在服务器本地用 curl 测试后端返回的 JSON 格式：

cmd
curl -X POST http://localhost:8000/analyze -H "Content-Type: application/json" -d "{\"symbol\":\"AAPL\"}"
看看返回的字段是否包含 price, change_percent, summary, sentiment, risk_level 等。如果缺少某些字段（例如 change_percent 可能是 undefined），需要修改后端 stock.py 确保这些字段总是存在。

如果还是不行
请把你 App.vue 中显示数据的部分代码（模板部分）和 analyze 方法发给我，我会给出更精准的修复。同时，后端返回的实际 JSON 也请提供（可以从浏览器开发者工具 Network 标签中看到）。

```

根据AI回答修改前端代码中的
```
相对路径 /api/analyze
```
修改为后端实际在服务器中运行的地址：
```
http://8.136.49.196:8000/analyze
```



