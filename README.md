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





