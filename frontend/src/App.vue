<template>
  <div class="container">
    <h1>AI 股票分析面板</h1>
    <div class="search-box">
      <input v-model="symbol" placeholder="股票代码 (如 AAPL)" @keyup.enter="analyze" />
      <button @click="analyze" :disabled="loading">分析</button>
    </div>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="result" class="result">
      <div class="stock-header">
        <h2>{{ result.symbol }}</h2>
        <span class="price">${{ result.price }}</span>
        <span :class="['change', result.change_percent >= 0 ? 'positive' : 'negative']">
          {{ result.change_percent >= 0 ? '+' : '' }}{{ result.change_percent }}%
        </span>
      </div>
      <div class="stock-info">
        <div class="info-item">
          <span class="label">开盘价</span>
          <span class="value">${{ result.open }}</span>
        </div>
        <div class="info-item">
          <span class="label">最高价</span>
          <span class="value">${{ result.high }}</span>
        </div>
        <div class="info-item">
          <span class="label">最低价</span>
          <span class="value">${{ result.low }}</span>
        </div>
        <div class="info-item">
          <span class="label">成交量</span>
          <span class="value">{{ formatVolume(result.volume) }}</span>
        </div>
      </div>
      <div class="analysis">
        <h3>AI 分析结果</h3>
        <div class="analysis-item">
          <span class="label">总结</span>
          <p class="summary">{{ result.summary }}</p>
        </div>
        <div class="analysis-item">
          <span class="label">市场情绪</span>
          <span :class="['sentiment', result.sentiment.toLowerCase()]">{{ result.sentiment }}</span>
        </div>
        <div class="analysis-item">
          <span class="label">风险等级</span>
          <span :class="['risk', result.risk_level.toLowerCase()]">{{ result.risk_level }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const symbol = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref('')

const formatVolume = (vol) => {
  if (vol >= 1e9) return (vol / 1e9).toFixed(2) + 'B'
  if (vol >= 1e6) return (vol / 1e6).toFixed(2) + 'M'
  if (vol >= 1e3) return (vol / 1e3).toFixed(2) + 'K'
  return vol.toString()
}

const analyze = async () => {
  if (!symbol.value.trim()) return
  loading.value = true
  error.value = ''
  result.value = null
  try {
    const response = await axios.post('/api/analyze', { symbol: symbol.value })
    result.value = response.data
  } catch (err) {
    error.value = err.response?.data?.detail || '分析失败，请稍后重试'
  } finally {
    loading.value = false
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
  min-height: 100vh;
  color: #fff;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  font-size: 2rem;
  background: linear-gradient(90deg, #00d4ff, #7c3aed);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.search-box {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
}

input {
  flex: 1;
  padding: 14px 20px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
  outline: none;
  transition: background 0.3s;
}

input:focus {
  background: rgba(255, 255, 255, 0.15);
}

input::placeholder {
  color: rgba(255, 255, 255, 0.5);
}

button {
  padding: 14px 28px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  background: linear-gradient(135deg, #00d4ff, #7c3aed);
  color: #fff;
  transition: transform 0.2s, opacity 0.2s;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  padding: 40px;
  font-size: 1.1rem;
  color: #00d4ff;
}

.error {
  text-align: center;
  padding: 15px;
  background: rgba(255, 59, 48, 0.2);
  border: 1px solid #ff3b30;
  border-radius: 8px;
  color: #ff6b6b;
  margin-bottom: 20px;
}

.result {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 16px;
  padding: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.stock-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.stock-header h2 {
  font-size: 1.5rem;
}

.price {
  font-size: 1.8rem;
  font-weight: 700;
  color: #00d4ff;
}

.change {
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
}

.change.positive {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.change.negative {
  background: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
}

.stock-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 24px;
}

.info-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 12px 16px;
  border-radius: 8px;
}

.info-item .label {
  display: block;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 4px;
}

.info-item .value {
  font-size: 1.1rem;
  font-weight: 600;
}

.analysis h3 {
  margin-bottom: 16px;
  font-size: 1.1rem;
  color: #7c3aed;
}

.analysis-item {
  margin-bottom: 16px;
}

.analysis-item .label {
  display: block;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 6px;
}

.summary {
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.9);
}

.sentiment, .risk {
  display: inline-block;
  padding: 6px 16px;
  border-radius: 20px;
  font-weight: 600;
}

.sentiment.bullish, .risk.low {
  background: rgba(34, 197, 94, 0.2);
  color: #22c55e;
}

.sentiment.neutral, .risk.medium {
  background: rgba(255, 193, 7, 0.2);
  color: #ffc107;
}

.sentiment.bearish, .risk.high {
  background: rgba(255, 59, 48, 0.2);
  color: #ff3b30;
}
</style>
