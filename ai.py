import os
import requests
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from google import genai
from lightweight_charts_v5 import lightweight_charts_v5_component
from datetime import datetime

# =========================
# Page Config
# =========================
st.set_page_config(page_title="AI Stock Research Platform Pro v2", layout="wide")

# =========================
# Language / i18n
# =========================
I18N = {
    "zh": {
        "page_title": "AI股票研究平台 Pro v2",
        "sidebar_title": "⚙️ 控制台",
        "api_key": "Gemini API Key",
        "symbol": "股票代號",
        "interval": "K線週期",
        "show_volume": "顯示成交量",
        "show_macd": "顯示 MACD",
        "show_rsi": "顯示 RSI",
        "peer_input": "手動同業代號（可留空，逗號分隔）",
        "scan_mode": "掃描範圍",
        "scan_mode_core": "預設核心股票池",
        "scan_mode_300": "全市場前300檔",
        "scan_mode_800": "全市場前800檔",
        "scan_limit": "排行榜 / 選股掃描數量",
        "sidebar_caption": "台股可輸入 2330；美股可輸入 AAPL；若興櫃抓不到會自動嘗試不同格式",
        "add_watchlist": "加入自選",
        "remove_watchlist": "移除自選",
        "watchlist": "⭐ 自選股",

        "app_title": "📈 AI 股票研究平台 Pro v2",
        "app_caption": "先看結論，再看理由，最後再看細節；再加上排行、選股、型態與自動同業比較。",

        "tab_overview": "總覽",
        "tab_technical": "技術面",
        "tab_fundamental": "基本面 / 同業",
        "tab_ranking": "排行榜",
        "tab_screener": "選股器",
        "tab_ai": "AI研究",
        "tab_debug": "除錯 / 資料狀態",

        "main_chart": "### 主要技術圖",
        "key_summary": "### 關鍵摘要",
        "pattern_detect": "### 型態偵測",
        "bull_reasons": "### 看多理由",
        "bear_reasons": "### 風險 / 看空理由",
        "multi_timeframe": "### 多時間框架總覽",
        "signal_table": "### 技術訊號總表",
        "watchlist_overview": "### 自選股總覽",

        "today_opportunities": "### 🔥 今日交易機會",
        "tw_opportunities": "台股機會",
        "us_opportunities": "美股機會",
        "no_tw_opportunities": "今天沒有掃描到明顯台股機會。",
        "no_us_opportunities": "今天沒有掃描到明顯美股機會。",
        "col_symbol": "代號",
        "col_price": "價格",
        "col_signals": "機會",
        "signal_breakout": "突破",
        "signal_pullback": "回踩",
        "signal_rsi_oversold": "RSI超賣",
        "signal_volume_spike": "爆量",

        "trend": "整體趨勢",
        "valuation": "估值評級",
        "risk": "風險等級",
        "bull_signal": "多方訊號",
        "bear_signal": "空方訊號",
        "support": "支撐",
        "resistance": "壓力",
        "target_up": "上行目標",
        "target_down": "下行風險",
        "volume": "成交量",

        "data_source": "資料來源",
        "data_quality": "資料品質",
        "display_period": "顯示週期",
        "fetch_interval": "實際抓取 interval",
        "fetch_period": "抓取 period",

        "ai_quick": "### AI快速摘要",
        "ai_full": "### 完整 AI 研究報告",
        "ai_system_conclusion": "### 系統快速結論",
        "gen_ai_quick": "生成 AI 快速摘要",
        "gen_ai_full": "生成完整 AI 報告",
        "enter_api_key": "請先輸入 Gemini API Key",
        "ai_quick_loading": "AI 摘要生成中...",
        "ai_full_loading": "AI 完整報告生成中...",
        "ai_quick_failed": "AI 快速摘要生成失敗：",
        "ai_full_failed": "AI 完整報告生成失敗：",
        "ai_full_caption": "可先生成快速摘要，再視需要生成完整報告。",

        "ranking_title": "### 熱門排行榜",
        "tw_ranking": "台股排行榜",
        "us_ranking": "美股排行榜",
        "tw_top": "#### 台股｜技術最強",
        "us_top": "#### 美股｜技術最強",
        "tw_breakout": "#### 台股｜接近突破",
        "us_breakout": "#### 美股｜接近突破",
        "no_tw_rank": "台股排行榜暫時無資料。",
        "no_us_rank": "美股排行榜暫時無資料。",
        "no_tw_breakout": "目前沒有明顯接近突破的台股標的。",
        "no_us_breakout": "目前沒有明顯接近突破的美股標的。",

        "screener_title": "### 簡易選股器",
        "tw_screener": "台股選股器",
        "us_screener": "美股選股器",
        "tw_filter": "#### 台股條件篩選",
        "us_filter": "#### 美股條件篩選",
        "min_score": "最低訊號分數",
        "only_breakout": "只看接近突破",
        "only_bull": "只看多頭排列",
        "no_tw_filtered": "目前沒有符合條件的台股標的。",
        "no_us_filtered": "目前沒有符合條件的美股標的。",

        "fundamental_observe": "### 基本面觀察",
        "peer_compare": "### 自動同業比較",
        "manual_peer_used": "目前使用：手動輸入同業代號",
        "auto_peer_used": "目前使用：系統自動帶出同業",
        "peer_invalid": "目前無法取得有效同業資料。",

        "debug_status": "### 資料狀態",
        "debug_errors": "### 嘗試過的候選代號 / 錯誤",
        "no_error": "- 無",
        "no_data": "查無資料，可能是代號格式不符、資料源無支援，或 Yahoo 暫時抓不到。",
        "try_symbol_errors": "🔍 嘗試過的代號與錯誤",

        "tech_interpret": "### 技術解讀",
        "trend_rating": "趨勢評級",
        "support_resistance": "支撐 / 壓力",
        "bull_strength": "多方訊號強度",
        "bear_strength": "空方訊號強度",
        "pattern": "型態",
        "tech_note": "這裡比較適合解讀成『技術訊號偏向』，不是保證性預測。",
        "gross_margin": "毛利率",
        "revenue_growth": "營收成長",
        "debt_ratio": "負債比",
        "valuation_grade": "估值評級",
        "valuation_now": "目前估值判斷",
        "quality_status": "資料品質狀態",
        "industry_label": "產業",
        "yahoo_backup_note": "若 Yahoo Finance 某些欄位缺失，正式產品建議加第二資料源備援。",
        "current_price": "現價",
        "market": "市場",
        "industry": "產業",
        "market_cap": "市值",
        "status_item": "項目",
        "status_value": "值",
        "actual_symbol": "實際使用代號",
        "raw_symbol": "原始輸入代號",
        "source_yahoo": "Yahoo Finance",
        "display_interval": "顯示週期",
        "use_symbol_errors": "嘗試過的候選代號 / 錯誤",
        "ma20_avg_vol": "均量20",
        "close": "收盤",
    },
    "en": {
        "page_title": "AI Stock Research Platform Pro v2",
        "sidebar_title": "⚙️ Control Panel",
        "api_key": "Gemini API Key",
        "symbol": "Ticker",
        "interval": "Chart Interval",
        "show_volume": "Show Volume",
        "show_macd": "Show MACD",
        "show_rsi": "Show RSI",
        "peer_input": "Manual Peer Tickers (optional, comma separated)",
        "scan_mode": "Scan Range",
        "scan_mode_core": "Core Watchlist",
        "scan_mode_300": "Top 300 Market Symbols",
        "scan_mode_800": "Top 800 Market Symbols",
        "scan_limit": "Ranking / Screener Scan Size",
        "sidebar_caption": "Use 2330 for Taiwan stocks, AAPL for US stocks. If OTC data is unavailable, the app will try alternative formats.",
        "add_watchlist": "Add to Watchlist",
        "remove_watchlist": "Remove from Watchlist",
        "watchlist": "⭐ Watchlist",

        "app_title": "📈 AI Stock Research Platform Pro v2",
        "app_caption": "See the conclusion first, then the reasons, then the details.",

        "tab_overview": "Overview",
        "tab_technical": "Technical",
        "tab_fundamental": "Fundamentals / Peers",
        "tab_ranking": "Ranking",
        "tab_screener": "Screener",
        "tab_ai": "AI Research",
        "tab_debug": "Debug / Data Status",

        "main_chart": "### Main Chart",
        "key_summary": "### Key Summary",
        "pattern_detect": "### Pattern Detection",
        "bull_reasons": "### Bullish Reasons",
        "bear_reasons": "### Risk / Bearish Reasons",
        "multi_timeframe": "### Multi-Timeframe Overview",
        "signal_table": "### Signal Table",
        "watchlist_overview": "### Watchlist Overview",

        "today_opportunities": "### 🔥 Today's Opportunities",
        "tw_opportunities": "Taiwan Opportunities",
        "us_opportunities": "US Opportunities",
        "no_tw_opportunities": "No clear Taiwan opportunities were found today.",
        "no_us_opportunities": "No clear US opportunities were found today.",
        "col_symbol": "Symbol",
        "col_price": "Price",
        "col_signals": "Signals",
        "signal_breakout": "Breakout",
        "signal_pullback": "Pullback",
        "signal_rsi_oversold": "RSI Oversold",
        "signal_volume_spike": "Volume Spike",

        "trend": "Trend",
        "valuation": "Valuation",
        "risk": "Risk",
        "bull_signal": "Bullish Signals",
        "bear_signal": "Bearish Signals",
        "support": "Support",
        "resistance": "Resistance",
        "target_up": "Upside Target",
        "target_down": "Downside Risk",
        "volume": "Volume",

        "data_source": "Data Source",
        "data_quality": "Data Quality",
        "display_period": "Display Interval",
        "fetch_interval": "Fetch Interval",
        "fetch_period": "Fetch Period",

        "ai_quick": "### AI Quick Summary",
        "ai_full": "### Full AI Research Report",
        "ai_system_conclusion": "### System Conclusion",
        "gen_ai_quick": "Generate AI Quick Summary",
        "gen_ai_full": "Generate Full AI Report",
        "enter_api_key": "Please enter your Gemini API Key first.",
        "ai_quick_loading": "Generating AI quick summary...",
        "ai_full_loading": "Generating full AI report...",
        "ai_quick_failed": "AI quick summary generation failed: ",
        "ai_full_failed": "AI full report generation failed: ",
        "ai_full_caption": "Generate a quick summary first, then generate the full report if needed.",

        "ranking_title": "### Ranking",
        "tw_ranking": "Taiwan Ranking",
        "us_ranking": "US Ranking",
        "tw_top": "#### Taiwan | Strongest Technical Setups",
        "us_top": "#### US | Strongest Technical Setups",
        "tw_breakout": "#### Taiwan | Near Breakout",
        "us_breakout": "#### US | Near Breakout",
        "no_tw_rank": "No Taiwan ranking data available.",
        "no_us_rank": "No US ranking data available.",
        "no_tw_breakout": "No Taiwan near-breakout setups found.",
        "no_us_breakout": "No US near-breakout setups found.",

        "screener_title": "### Stock Screener",
        "tw_screener": "Taiwan Screener",
        "us_screener": "US Screener",
        "tw_filter": "#### Taiwan Filters",
        "us_filter": "#### US Filters",
        "min_score": "Minimum Signal Score",
        "only_breakout": "Only Near Breakout",
        "only_bull": "Only Bullish Alignment",
        "no_tw_filtered": "No Taiwan stocks matched the filters.",
        "no_us_filtered": "No US stocks matched the filters.",

        "fundamental_observe": "### Fundamental Notes",
        "peer_compare": "### Peer Comparison",
        "manual_peer_used": "Current mode: Manual peer tickers",
        "auto_peer_used": "Current mode: Auto-selected peers",
        "peer_invalid": "No valid peer data available.",

        "debug_status": "### Data Status",
        "debug_errors": "### Tried Symbols / Errors",
        "no_error": "- None",
        "no_data": "No data found. The ticker format may be unsupported, the source may not support it, or Yahoo may be temporarily unavailable.",
        "try_symbol_errors": "🔍 Tried Symbols and Errors",

        "tech_interpret": "### Technical Interpretation",
        "trend_rating": "Trend Rating",
        "support_resistance": "Support / Resistance",
        "bull_strength": "Bullish Signal Strength",
        "bear_strength": "Bearish Signal Strength",
        "pattern": "Pattern",
        "tech_note": "This section should be read as a technical bias summary, not a guaranteed forecast.",
        "gross_margin": "Gross Margin",
        "revenue_growth": "Revenue Growth",
        "debt_ratio": "Debt Ratio",
        "valuation_grade": "Valuation Grade",
        "valuation_now": "Current Valuation View",
        "quality_status": "Data Quality Status",
        "industry_label": "Industry",
        "yahoo_backup_note": "If Yahoo Finance fields are missing, a production version should include a secondary backup data source.",
        "current_price": "Current Price",
        "market": "Market",
        "industry": "Industry",
        "market_cap": "Market Cap",
        "status_item": "Item",
        "status_value": "Value",
        "actual_symbol": "Actual Symbol Used",
        "raw_symbol": "Original Input Symbol",
        "source_yahoo": "Yahoo Finance",
        "display_interval": "Display Interval",
        "use_symbol_errors": "Tried Symbols / Errors",
        "ma20_avg_vol": "Volume MA20",
        "close": "Close",
    }
}


def tr(key, lang="zh"):
    return I18N.get(lang, I18N["zh"]).get(key, key)


def trend_label(score, lang="zh"):
    if lang == "en":
        if score >= 4:
            return "Bullish"
        if score == 3:
            return "Slightly Bullish"
        if score == 2:
            return "Neutral"
        if score == 1:
            return "Slightly Bearish"
        return "Bearish"
    else:
        if score >= 4:
            return "偏多"
        if score == 3:
            return "中性偏多"
        if score == 2:
            return "中性"
        if score == 1:
            return "中性偏空"
        return "偏空"


def valuation_label(pe, pb, lang="zh"):
    try:
        pe = float(pe) if pe is not None else None
    except Exception:
        pe = None

    try:
        pb = float(pb) if pb is not None else None
    except Exception:
        pb = None

    if pe is None and pb is None:
        return "Insufficient Data" if lang == "en" else "資料不足"

    if pe is not None:
        if pe < 15:
            return "Undervalued" if lang == "en" else "偏低"
        elif pe <= 25:
            return "Fair" if lang == "en" else "合理"
        else:
            return "Overvalued" if lang == "en" else "偏高"

    if pb is not None:
        if pb < 1.5:
            return "Undervalued" if lang == "en" else "偏低"
        elif pb <= 3:
            return "Fair" if lang == "en" else "合理"
        else:
            return "Overvalued" if lang == "en" else "偏高"

    return "Insufficient Data" if lang == "en" else "資料不足"


def risk_label(latest, support, resistance, lang="zh"):
    if latest is None:
        return "Unknown" if lang == "en" else "未知"

    price = latest["Close"]
    rsi_value = latest.get("RSI", np.nan)
    flags = 0

    if support is not None and price <= support * 1.02:
        flags += 1

    if resistance is not None and price >= resistance * 0.98:
        flags += 1

    if pd.notna(rsi_value) and (rsi_value >= 70 or rsi_value <= 30):
        flags += 1

    if flags >= 2:
        return "High" if lang == "en" else "高"
    if flags == 1:
        return "Medium" if lang == "en" else "中"
    return "Low" if lang == "en" else "低"


def pattern_text(key, lang="zh"):
    mapping = {
        "多頭排列": "Bullish Alignment",
        "接近突破": "Near Breakout",
        "接近壓力": "Near Resistance",
        "接近支撐": "Near Support",
        "強勢整理": "Strong Consolidation",
        "暫無明確型態": "No Clear Pattern",
    }
    if lang == "en":
        return mapping.get(key, key)
    return key


def quality_text(value, lang="zh"):
    mapping = {
        "完整": "Complete",
        "部分缺漏": "Partial",
        "不足": "Insufficient",
    }
    return mapping.get(value, value) if lang == "en" else value


def market_text(value, lang="zh"):
    mapping = {
        "台股/櫃買": "Taiwan",
        "海外/其他": "Global / Other",
    }
    return mapping.get(value, value) if lang == "en" else value


def signal_status_text(value, lang="zh"):
    mapping = {
        "多頭": "Bullish",
        "空頭": "Bearish",
        "過熱": "Overbought",
        "超賣": "Oversold",
        "偏強": "Strong",
        "偏弱": "Weak",
        "中性": "Neutral",
        "黃金交叉上方": "Above Signal (Bullish)",
        "死亡交叉下方": "Below Signal (Bearish)",
        "接近壓力/突破": "Near Resistance / Breakout",
        "接近支撐": "Near Support",
        "區間中段": "Mid-range",
        "放量": "High Volume",
        "量縮": "Low Volume",
    }
    return mapping.get(value, value) if lang == "en" else value


def reason_text(text, lang="zh"):
    if lang == "zh":
        return text

    mapping = {
        "股價站上 MA20，短線結構偏強": "Price is above MA20, suggesting stronger short-term structure.",
        "股價未站穩 MA20，短線動能偏弱": "Price is below MA20, indicating weaker short-term momentum.",
        "MA20 位於 MA60 之上，均線排列偏多": "MA20 is above MA60, showing a bullish moving average structure.",
        "MA20 尚未有效站上 MA60，趨勢確認不足": "MA20 has not clearly moved above MA60, so trend confirmation is still weak.",
        "MACD 位於訊號線上方，動能結構較佳": "MACD is above the signal line, indicating better momentum structure.",
        "MACD 位於訊號線下方，短期動能保守": "MACD is below the signal line, suggesting weaker short-term momentum.",
        "RSI 偏高，需留意過熱拉回風險": "RSI is elevated, so a pullback risk should be monitored.",
        "RSI 進入低檔區，可能接近技術性反彈區": "RSI is in a lower range, which may indicate a technical rebound zone.",
        "股價接近壓力區，追價風險提高": "Price is near resistance, so chasing may carry higher risk.",
        "股價靠近支撐區，可觀察承接力道": "Price is near support, so buying interest can be observed.",
        "目前偏多訊號有限，需等待更明確確認": "Bullish signals are still limited; clearer confirmation is needed.",
        "明顯偏空訊號有限，但仍需留意市場波動": "Clear bearish signals are limited, but volatility should still be monitored.",
    }
    return mapping.get(text, text)


# =========================
# Styles
# =========================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1550px;
    }
    .hero-card {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 18px;
        padding: 18px 20px;
        background: rgba(255,255,255,0.02);
        margin-bottom: 10px;
    }
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.15rem;
    }
    .hero-sub {
        color: #9aa4b2;
        font-size: 0.95rem;
    }
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.82rem;
        margin-right: 8px;
        border: 1px solid rgba(255,255,255,0.12);
    }
    .ai-box {
        border-left: 4px solid #42a5f5;
        padding: 12px 14px;
        background: rgba(66,165,245,0.08);
        border-radius: 10px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# Built-in Universe / Peer Map
# =========================
DEFAULT_TW_UNIVERSE = [
    "2330", "2303", "2454", "3711", "3034", "6669", "2379", "3231",
    "2317", "2382", "2357", "4938",
    "2881", "2882", "2884", "2885", "2891", "2892", "5880",
    "1101", "1102", "1216", "1301", "1303", "2002",
    "2603", "2609", "2615",
    "3008", "6415", "2376", "3443"
]

DEFAULT_US_UNIVERSE = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AMD", "TSLA",
    "AVGO", "NFLX", "INTC", "QCOM", "MU", "SMCI", "TSM", "ASML",
    "JPM", "BAC", "GS", "MS",
    "XOM", "CVX",
    "KO", "PEP", "WMT", "COST",
    "PLTR", "SNOW", "CRM", "ADBE"
]

TW_UNIVERSE_CACHE = "tw_universe.csv"
US_UNIVERSE_CACHE = "us_universe.csv"

MANUAL_PEER_MAP = {
    "2330": ["2303", "3711", "2454", "3034", "2379"],
    "2303": ["2330", "3711", "2454", "3034", "2379"],
    "2454": ["2330", "2303", "3711", "3034", "2379"],
    "2317": ["2382", "2357", "4938"],
    "2881": ["2882", "2884", "2885", "2891", "2892"],
    "2603": ["2609", "2615"],
    "NVDA": ["AMD", "AVGO", "INTC", "QCOM", "MU", "TSM"],
    "AMD": ["NVDA", "INTC", "QCOM", "MU", "AVGO"],
    "AAPL": ["MSFT", "GOOGL", "AMZN", "META"],
    "MSFT": ["AAPL", "GOOGL", "AMZN", "META", "CRM", "ADBE"],
    "GOOGL": ["MSFT", "META", "AMZN", "AAPL"],
    "AMZN": ["MSFT", "GOOGL", "META", "AAPL"],
    "META": ["GOOGL", "MSFT", "AMZN", "AAPL"],
    "TSLA": ["NVDA", "AAPL", "AMZN"],
    "JPM": ["BAC", "GS", "MS"],
}

# =========================
# Full Market Universe Loaders
# =========================
@st.cache_data(show_spinner=False, ttl=86400)
def load_tw_universe():
    if os.path.exists(TW_UNIVERSE_CACHE):
        try:
            df = pd.read_csv(TW_UNIVERSE_CACHE, dtype=str)
            if not df.empty:
                return df
        except Exception:
            pass

    try:
        twse_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
        res = requests.get(twse_url, timeout=20)
        res.raise_for_status()
        data = res.json()
        df = pd.DataFrame(data)

        rename_map = {}
        for c in df.columns:
            c2 = str(c).strip()
            if c2 in ["公司代號", "證券代號", "股票代號"]:
                rename_map[c] = "symbol"
            elif c2 in ["公司名稱", "證券名稱", "股票名稱"]:
                rename_map[c] = "name"

        df = df.rename(columns=rename_map)

        if "symbol" not in df.columns:
            return pd.DataFrame({
                "symbol": DEFAULT_TW_UNIVERSE,
                "name": DEFAULT_TW_UNIVERSE,
                "market": ["TW"] * len(DEFAULT_TW_UNIVERSE),
            })

        if "name" not in df.columns:
            df["name"] = df["symbol"]

        df["symbol"] = df["symbol"].astype(str).str.strip()
        df = df[df["symbol"].str.match(r"^\d{4,6}$", na=False)]
        df["market"] = "TW"
        df = df[["symbol", "name", "market"]].drop_duplicates()

        df.to_csv(TW_UNIVERSE_CACHE, index=False, encoding="utf-8-sig")
        return df

    except Exception:
        return pd.DataFrame({
            "symbol": DEFAULT_TW_UNIVERSE,
            "name": DEFAULT_TW_UNIVERSE,
            "market": ["TW"] * len(DEFAULT_TW_UNIVERSE),
        })


@st.cache_data(show_spinner=False, ttl=86400)
def load_us_universe():
    if os.path.exists(US_UNIVERSE_CACHE):
        try:
            df = pd.read_csv(US_UNIVERSE_CACHE, dtype=str)
            if not df.empty:
                return df
        except Exception:
            pass

    try:
        nasdaq_url = "https://www.nasdaqtrader.com/dynamic/symdir/nasdaqlisted.txt"
        df = pd.read_csv(nasdaq_url, sep="|", dtype=str)

        df = df.rename(columns={
            "Symbol": "symbol",
            "Security Name": "name"
        })

        df = df[df["symbol"].notna()]
        df = df[~df["symbol"].astype(str).str.contains("File Creation Time", na=False)]

        if "ETF" in df.columns:
            df = df[df["ETF"] == "N"]
        if "Test Issue" in df.columns:
            df = df[df["Test Issue"] == "N"]

        df["name"] = df["name"].fillna("")
        df = df[
            ~df["name"].str.contains(
                "Warrant|Right|Unit|Preferred|ETF|ETN|Trust|Depositary",
                case=False,
                na=False
            )
        ]

        df["symbol"] = df["symbol"].astype(str).str.strip().str.upper()
        df = df[df["symbol"].str.match(r"^[A-Z.\-]+$", na=False)]

        df["market"] = "US"
        df = df[["symbol", "name", "market"]].drop_duplicates()

        df.to_csv(US_UNIVERSE_CACHE, index=False, encoding="utf-8-sig")
        return df

    except Exception:
        return pd.DataFrame({
            "symbol": DEFAULT_US_UNIVERSE,
            "name": DEFAULT_US_UNIVERSE,
            "market": ["US"] * len(DEFAULT_US_UNIVERSE),
        })


def get_tw_scan_symbols(scan_mode):
    tw_df = load_tw_universe()
    symbols = tw_df["symbol"].dropna().astype(str).tolist()

    if scan_mode in ["預設核心股票池", "Core Watchlist"]:
        return DEFAULT_TW_UNIVERSE
    elif scan_mode in ["全市場前300檔", "Top 300 Market Symbols"]:
        return symbols[:300]
    elif scan_mode in ["全市場前800檔", "Top 800 Market Symbols"]:
        return symbols[:800]
    else:
        return DEFAULT_TW_UNIVERSE


def get_us_scan_symbols(scan_mode):
    us_df = load_us_universe()
    symbols = us_df["symbol"].dropna().astype(str).tolist()

    if scan_mode in ["預設核心股票池", "Core Watchlist"]:
        return DEFAULT_US_UNIVERSE
    elif scan_mode in ["全市場前300檔", "Top 300 Market Symbols"]:
        return symbols[:300]
    elif scan_mode in ["全市場前800檔", "Top 800 Market Symbols"]:
        return symbols[:800]
    else:
        return DEFAULT_US_UNIVERSE


# =========================
# Technical Indicators
# =========================
def sma(series, n):
    return series.rolling(n).mean()


def ema(series, n):
    return series.ewm(span=n, adjust=False).mean()


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd(series):
    ema12 = ema(series, 12)
    ema26 = ema(series, 26)

    macd_line = ema12 - ema26
    signal = ema(macd_line, 9)
    hist = macd_line - signal

    return macd_line, signal, hist


# =========================
# Format Helpers
# =========================
def safe_float(v, digits=2):
    try:
        if v is None or pd.isna(v):
            return None
        return round(float(v), digits)
    except Exception:
        return None


def fmt_value(v, digits=2, default="N/A"):
    try:
        if v is None or pd.isna(v):
            return default
        if isinstance(v, (float, np.floating, int, np.integer)):
            return f"{float(v):,.{digits}f}"
        return str(v)
    except Exception:
        return default


def fmt_ratio(v, default="N/A"):
    try:
        if v is None or pd.isna(v):
            return default
        v = float(v)
        if abs(v) <= 1:
            return f"{v * 100:.2f}%"
        return f"{v:.2f}"
    except Exception:
        return default


def fmt_large_num(v):
    try:
        if v is None or pd.isna(v):
            return "N/A"
        v = float(v)
        if abs(v) >= 1_000_000_000:
            return f"{v / 1_000_000_000:.2f}B"
        if abs(v) >= 1_000_000:
            return f"{v / 1_000_000:.2f}M"
        return f"{v:,.0f}"
    except Exception:
        return "N/A"


# =========================
# Interval Helpers
# =========================
def interval_to_period(interval: str):
    if interval == "1h":
        return "60d"
    elif interval == "4h":
        return "60d"
    elif interval == "1d":
        return "1y"
    elif interval == "1wk":
        return "5y"
    elif interval == "1mo":
        return "10y"
    return "1y"


def interval_to_fetch_interval(interval: str):
    if interval == "1h":
        return "60m"
    elif interval == "4h":
        return "60m"
    return interval


# =========================
# Symbol Candidates
# =========================
def build_symbol_candidates(symbol: str):
    symbol = symbol.upper().strip()

    if not symbol.isdigit():
        return [symbol]

    raw = symbol
    z5 = symbol.zfill(5)
    z6 = symbol.zfill(6)

    candidates = []
    for s in [raw, z5, z6]:
        candidates.append(f"{s}.TW")
        candidates.append(f"{s}.TWO")
    candidates.append(raw)

    seen = set()
    result = []
    for s in candidates:
        if s not in seen:
            seen.add(s)
            result.append(s)

    return result


# =========================
# Resample 4H
# =========================
def resample_to_4h(df):
    if df is None or df.empty:
        return df

    df = df.copy()

    if not isinstance(df.index, pd.DatetimeIndex):
        return df

    try:
        if df.index.tz is not None:
            df = df.tz_convert(None)
    except Exception:
        pass

    out = df.resample("4h").agg({
        "Open": "first",
        "High": "max",
        "Low": "min",
        "Close": "last",
        "Volume": "sum",
    })

    out = out.dropna(subset=["Open", "High", "Low", "Close"])
    return out


# =========================
# Support / Resistance
# =========================
def support_resistance(df, window=20):
    support = df["Low"].rolling(window).min().iloc[-1]
    resistance = df["High"].rolling(window).max().iloc[-1]
    return safe_float(support), safe_float(resistance)


def calculate_target(price, resistance, support):
    if resistance is None or support is None:
        return None, None

    up = resistance * 1.05
    down = support * 0.95
    return safe_float(up), safe_float(down)


# =========================
# Trend / Risk / Valuation
# =========================
def trend_score(df):
    latest = df.iloc[-1]
    score = 0

    if pd.notna(latest["MA20"]) and latest["Close"] > latest["MA20"]:
        score += 1

    if pd.notna(latest["MA20"]) and pd.notna(latest["MA60"]) and latest["MA20"] > latest["MA60"]:
        score += 1

    if pd.notna(latest["RSI"]) and latest["RSI"] > 55:
        score += 1

    if pd.notna(latest["MACD"]) and pd.notna(latest["MACD_SIGNAL"]) and latest["MACD"] > latest["MACD_SIGNAL"]:
        score += 1

    vol_ma20 = df["Volume"].rolling(20).mean().iloc[-1]
    if pd.notna(vol_ma20) and latest["Volume"] > vol_ma20:
        score += 1

    return score


def get_trend_label(score, lang="zh"):
    return trend_label(score, lang)


def get_risk_label(latest, support, resistance, lang="zh"):
    return risk_label(latest, support, resistance, lang)


def get_valuation_label(pe, pb, lang="zh"):
    return valuation_label(pe, pb, lang)


def data_quality_badge(data):
    pe_ok = data.get("pe") is not None
    pb_ok = data.get("pb") is not None
    eps_ok = data.get("eps") is not None
    hist_ok = data.get("hist") is not None and not data["hist"].empty

    score = sum([pe_ok, pb_ok, eps_ok, hist_ok])

    if score >= 4:
        return "完整"
    elif score >= 2:
        return "部分缺漏"
    else:
        return "不足"


# =========================
# Pattern / Signal Logic
# =========================
def detect_patterns(df):
    latest = df.iloc[-1]
    patterns = []

    if pd.notna(latest["MA20"]) and pd.notna(latest["MA60"]):
        if latest["Close"] > latest["MA20"] and latest["MA20"] > latest["MA60"]:
            patterns.append("多頭排列")

    resistance = df["High"].rolling(20).max().iloc[-1]
    support = df["Low"].rolling(20).min().iloc[-1]
    vol_ma20 = df["Volume"].rolling(20).mean().iloc[-1]

    if pd.notna(resistance) and latest["Close"] >= resistance * 0.98:
        if pd.notna(vol_ma20) and latest["Volume"] >= vol_ma20:
            patterns.append("接近突破")
        else:
            patterns.append("接近壓力")

    if pd.notna(support) and latest["Close"] <= support * 1.02:
        patterns.append("接近支撐")

    if pd.notna(latest["RSI"]) and 50 <= latest["RSI"] <= 65 and latest["Close"] > latest["MA20"]:
        patterns.append("強勢整理")

    if not patterns:
        patterns.append("暫無明確型態")

    return patterns


# =========================
# Quick Summary
# =========================
def build_local_ai_brief(data, quick_summary, lang="zh"):
    patterns = " / ".join([pattern_text(p, lang) for p in quick_summary["patterns"][:2]])
    reasons = " ; ".join(quick_summary["bullish"][:2])
    risks = " ; ".join(quick_summary["bearish"][:2])

    if lang == "en":
        return (
            f"AI Brief: {data['name']} is currently {quick_summary['trend']}. "
            f"Key pattern(s): {patterns}. "
            f"Main strengths: {reasons}. "
            f"Main risks: {risks}."
        )

    return (
        f"AI快評：{data['name']}目前偏向{quick_summary['trend']}，"
        f"型態重點為{patterns}。主要優勢：{reasons}。主要風險：{risks}。"
    )


def build_quick_summary(data, lang="zh"):
    hist = data.get("hist")
    if hist is None or hist.empty:
        return {
            "trend": "No Data" if lang == "en" else "無資料",
            "valuation": "No Data" if lang == "en" else "無資料",
            "risk": "No Data" if lang == "en" else "無資料",
            "patterns": ["No Clear Pattern"] if lang == "en" else ["暫無明確型態"],
            "bullish": ["Insufficient data"] if lang == "en" else ["資料不足"],
            "bearish": ["Insufficient data"] if lang == "en" else ["資料不足"],
            "one_line": "No sufficient data available." if lang == "en" else "目前資料不足，無法產生完整摘要。"
        }

    latest = hist.iloc[-1]
    patterns = detect_patterns(hist)

    trend = get_trend_label(data.get("score", 0), lang=lang)
    valuation = get_valuation_label(data.get("pe"), data.get("pb"), lang=lang)
    risk = get_risk_label(latest, data.get("support"), data.get("resistance"), lang=lang)

    bullish = []
    bearish = []

    if pd.notna(latest.get("MA20")) and latest["Close"] > latest["MA20"]:
        bullish.append(reason_text("股價站上 MA20，短線結構偏強", lang))
    else:
        bearish.append(reason_text("股價未站穩 MA20，短線動能偏弱", lang))

    if pd.notna(latest.get("MA20")) and pd.notna(latest.get("MA60")) and latest["MA20"] > latest["MA60"]:
        bullish.append(reason_text("MA20 位於 MA60 之上，均線排列偏多", lang))
    else:
        bearish.append(reason_text("MA20 尚未有效站上 MA60，趨勢確認不足", lang))

    if pd.notna(latest.get("MACD")) and pd.notna(latest.get("MACD_SIGNAL")):
        if latest["MACD"] > latest["MACD_SIGNAL"]:
            bullish.append(reason_text("MACD 位於訊號線上方，動能結構較佳", lang))
        else:
            bearish.append(reason_text("MACD 位於訊號線下方，短期動能保守", lang))

    if pd.notna(latest.get("RSI")):
        if latest["RSI"] >= 70:
            bearish.append(reason_text("RSI 偏高，需留意過熱拉回風險", lang))
        elif latest["RSI"] <= 30:
            bullish.append(reason_text("RSI 進入低檔區，可能接近技術性反彈區", lang))

    if data.get("resistance") is not None and latest["Close"] >= data["resistance"] * 0.98:
        bearish.append(reason_text("股價接近壓力區，追價風險提高", lang))

    if data.get("support") is not None and latest["Close"] <= data["support"] * 1.02:
        bullish.append(reason_text("股價靠近支撐區，可觀察承接力道", lang))

    if not bullish:
        bullish.append(reason_text("目前偏多訊號有限，需等待更明確確認", lang))

    if not bearish:
        bearish.append(reason_text("明顯偏空訊號有限，但仍需留意市場波動", lang))

    if lang == "en":
        one_line = f"{data['name']} is currently {trend}, with valuation viewed as {valuation} and overall risk assessed as {risk}."
    else:
        one_line = f"{data['name']} 目前趨勢為{trend}，估值評級為{valuation}，整體風險屬於{risk}。"

    return {
        "trend": trend,
        "valuation": valuation,
        "risk": risk,
        "patterns": patterns,
        "bullish": bullish[:3],
        "bearish": bearish[:3],
        "one_line": one_line,
    }


# =========================
# Signals Table
# =========================
def generate_signal_table(df, support, resistance, lang="zh"):
    latest = df.iloc[-1]
    rows = []

    col_signal = "訊號" if lang == "zh" else "Signal"
    col_status = "狀態" if lang == "zh" else "Status"
    col_desc = "說明" if lang == "zh" else "Description"

    def add_signal(name, status, detail):
        rows.append({
            col_signal: name,
            col_status: status,
            col_desc: detail
        })

    if pd.notna(latest["MA20"]) and pd.notna(latest["MA60"]):
        add_signal(
            "均線排列" if lang == "zh" else "Moving Average Structure",
            signal_status_text("多頭" if latest["MA20"] > latest["MA60"] else "空頭", lang),
            f"MA20={fmt_value(latest['MA20'])} / MA60={fmt_value(latest['MA60'])}",
        )

    if pd.notna(latest["RSI"]):
        r = float(latest["RSI"])
        if r >= 70:
            status = "過熱"
        elif r <= 30:
            status = "超賣"
        elif r >= 55:
            status = "偏強"
        elif r <= 45:
            status = "偏弱"
        else:
            status = "中性"

        add_signal("RSI", signal_status_text(status, lang), f"RSI={fmt_value(r)}")

    if pd.notna(latest["MACD"]) and pd.notna(latest["MACD_SIGNAL"]):
        status = "黃金交叉上方" if latest["MACD"] > latest["MACD_SIGNAL"] else "死亡交叉下方"
        add_signal(
            "MACD",
            signal_status_text(status, lang),
            f"MACD={fmt_value(latest['MACD'])} / Signal={fmt_value(latest['MACD_SIGNAL'])}",
        )

    if support is not None and resistance is not None:
        close = float(latest["Close"])
        if close >= resistance * 0.98:
            status = "接近壓力/突破"
        elif close <= support * 1.02:
            status = "接近支撐"
        else:
            status = "區間中段"

        add_signal(
            "關鍵價位" if lang == "zh" else "Key Levels",
            signal_status_text(status, lang),
            f"{tr('support', lang)}={support} / {tr('resistance', lang)}={resistance}"
        )

    vol_ma20 = df["Volume"].rolling(20).mean().iloc[-1]
    if pd.notna(vol_ma20):
        status = "放量" if latest["Volume"] > vol_ma20 else "量縮"
        add_signal(
            tr("volume", lang),
            signal_status_text(status, lang),
            f"{tr('volume', lang)}={fmt_large_num(latest['Volume'])} / MA20={fmt_large_num(vol_ma20)}"
        )

    patterns = detect_patterns(df)
    add_signal(
        "型態" if lang == "zh" else "Pattern",
        " / ".join([pattern_text(p, lang) for p in patterns]),
        "系統根據均線、區間高低與量能做簡易偵測" if lang == "zh" else "Detected from moving averages, range levels, and volume."
    )

    return pd.DataFrame(rows)


# =========================
# Cached Data Fetch
# =========================
@st.cache_data(show_spinner=False, ttl=900)
def safe_get_info_cached(symbol_used):
    try:
        info = yf.Ticker(symbol_used).info
        if isinstance(info, dict):
            return info
        return {}
    except Exception:
        return {}


@st.cache_data(show_spinner=False, ttl=900)
def fetch_history_cached(symbol_used, interval, period):
    fetch_interval = interval_to_fetch_interval(interval)

    try:
        hist = yf.Ticker(symbol_used).history(
            period=period,
            interval=fetch_interval,
            auto_adjust=False
        )

        if hist is None or hist.empty:
            return pd.DataFrame()

        if interval == "4h":
            hist = resample_to_4h(hist)

        return hist

    except Exception:
        return pd.DataFrame()


def enrich_hist(hist):
    hist = hist.copy()
    hist = hist.dropna(subset=["Open", "High", "Low", "Close"])

    hist["MA20"] = sma(hist["Close"], 20)
    hist["MA60"] = sma(hist["Close"], 60)
    hist["RSI"] = rsi(hist["Close"])
    hist["MACD"], hist["MACD_SIGNAL"], hist["MACD_HIST"] = macd(hist["Close"])

    return hist


# =========================
# Main Stock Fetch
# =========================
def get_stock(symbol, interval="1d"):
    candidates = build_symbol_candidates(symbol)
    errors = []
    period = interval_to_period(interval)
    fetch_interval = interval_to_fetch_interval(interval)

    for sym in candidates:
        try:
            hist = fetch_history_cached(sym, interval, period)

            if hist is None or hist.empty:
                errors.append(f"{sym}: 無歷史資料")
                continue

            required_cols = ["Open", "High", "Low", "Close", "Volume"]
            if not all(col in hist.columns for col in required_cols):
                errors.append(f"{sym}: 欄位不完整")
                continue

            hist = enrich_hist(hist)

            if hist.empty:
                errors.append(f"{sym}: 清理後無資料")
                continue

            info = safe_get_info_cached(sym)
            latest = hist.iloc[-1]

            prev_close = hist["Close"].iloc[-2] if len(hist) >= 2 else latest["Close"]
            change = float(latest["Close"] - prev_close)
            change_pct = (change / prev_close * 100) if prev_close not in [0, None] else 0

            support, resistance = support_resistance(hist)
            up_target, down_target = calculate_target(latest["Close"], resistance, support)

            score = trend_score(hist)
            bull = round((score / 5) * 100, 1)
            bear = round(100 - bull, 1)

            market = "台股/櫃買" if str(sym).endswith((".TW", ".TWO")) or str(symbol).isdigit() else "海外/其他"

            sector = info.get("sector") or "N/A"
            industry = info.get("industry") or "N/A"

            return {
                "symbol_used": sym,
                "raw_symbol": symbol.upper().strip(),
                "name": info.get("longName") or info.get("shortName") or sym,
                "sector": sector,
                "industry": industry,
                "display_industry": industry if industry != "N/A" else sector,
                "market": market,
                "price": safe_float(latest["Close"]),
                "change": safe_float(change),
                "change_pct": safe_float(change_pct),
                "pe": info.get("trailingPE"),
                "eps": info.get("trailingEps"),
                "pb": info.get("priceToBook"),
                "roe": info.get("returnOnEquity"),
                "gross": info.get("grossMargins"),
                "revenue": info.get("revenueGrowth"),
                "debt": info.get("debtToEquity"),
                "market_cap": info.get("marketCap"),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
                "currency": info.get("currency", ""),
                "support": support,
                "resistance": resistance,
                "target_up": up_target,
                "target_down": down_target,
                "bull": bull,
                "bear": bear,
                "score": score,
                "hist": hist,
                "errors": errors,
                "interval": interval,
                "period": period,
                "fetch_interval": fetch_interval,
                "data_quality": data_quality_badge({
                    "pe": info.get("trailingPE"),
                    "pb": info.get("priceToBook"),
                    "eps": info.get("trailingEps"),
                    "hist": hist,
                }),
            }

        except Exception as e:
            errors.append(f"{sym}: {str(e)}")
            continue

    return {
        "errors": errors,
        "symbol_used": None
    }


# =========================
# Multi Timeframe Summary
# =========================
def get_multi_timeframe_summary(symbol, lang="zh", intervals=("1h", "4h", "1d", "1wk")):
    rows = []

    col_period = "週期" if lang == "zh" else "Interval"
    col_trend = "趨勢" if lang == "zh" else "Trend"
    col_price = "價格" if lang == "zh" else "Price"
    col_rsi = "RSI"
    col_score = "訊號分數" if lang == "zh" else "Signal Score"

    for iv in intervals:
        data = get_stock(symbol, interval=iv)

        if data.get("hist") is None:
            rows.append({
                col_period: iv,
                col_trend: "無資料" if lang == "zh" else "No Data",
                col_price: "N/A",
                col_rsi: "N/A",
                col_score: "N/A"
            })
            continue

        latest = data["hist"].iloc[-1]

        rows.append({
            col_period: iv,
            col_trend: get_trend_label(data["score"], lang=lang),
            col_price: fmt_value(data["price"]),
            col_rsi: fmt_value(latest.get("RSI")),
            col_score: f"{data['score']}/5",
        })

    return pd.DataFrame(rows)


# =========================
# Auto Peer Compare
# =========================
def auto_find_peers(data, max_peers=5):
    raw_symbol = str(data.get("raw_symbol", "")).upper()

    if raw_symbol in MANUAL_PEER_MAP:
        return MANUAL_PEER_MAP[raw_symbol][:max_peers]

    if data["market"] == "台股/櫃買":
        universe = [s for s in DEFAULT_TW_UNIVERSE if s != raw_symbol]
        return universe[:max_peers]

    universe = [s for s in DEFAULT_US_UNIVERSE if s != raw_symbol]
    return universe[:max_peers]


def build_peer_compare_table(symbols, lang="zh", max_items=6):
    rows = []

    for sym in symbols[:max_items]:
        p_data = get_stock(sym, interval="1d")
        if p_data.get("hist") is not None:
            rows.append({
                tr("col_symbol", lang): p_data["raw_symbol"],
                "名稱" if lang == "zh" else "Name": p_data["name"],
                tr("col_price", lang): fmt_value(p_data["price"]),
                "PE": fmt_value(p_data["pe"]),
                "PB": fmt_value(p_data["pb"]),
                "ROE": fmt_ratio(p_data["roe"]),
                tr("trend", lang): get_trend_label(p_data["score"], lang=lang),
                "型態" if lang == "zh" else "Pattern": " / ".join(
                    [pattern_text(p, lang) for p in detect_patterns(p_data["hist"])[:2]]
                ),
            })

    return pd.DataFrame(rows)


# =========================
# Universe Scan / Ranking / Screener
# =========================
def get_default_universe_for_market(symbol):
    return DEFAULT_TW_UNIVERSE if str(symbol).isdigit() else DEFAULT_US_UNIVERSE


@st.cache_data(show_spinner=False, ttl=1800)
def scan_universe(universe_symbols, lang="zh", limit=None):
    rows = []
    symbols = list(universe_symbols)

    if limit is not None:
        symbols = symbols[:limit]

    for sym in symbols:
        d = get_stock(sym, interval="1d")
        if d.get("hist") is None:
            continue

        latest = d["hist"].iloc[-1]
        patterns = detect_patterns(d["hist"])

        try:
            roe_value = d["roe"]
            if roe_value is not None:
                roe_value = float(roe_value)
                if abs(roe_value) <= 1:
                    roe_value = roe_value * 100
                roe_value = safe_float(roe_value)
            else:
                roe_value = None
        except Exception:
            roe_value = None

        rows.append({
            tr("col_symbol", lang): d["raw_symbol"],
            "名稱" if lang == "zh" else "Name": d["name"],
            tr("col_price", lang): safe_float(d["price"]),
            "漲跌幅" if lang == "zh" else "Change %": safe_float(d["change_pct"]),
            "訊號分數" if lang == "zh" else "Signal Score": d["score"],
            tr("trend", lang): get_trend_label(d["score"], lang=lang),
            "RSI": safe_float(latest["RSI"]),
            "PE": safe_float(d["pe"]),
            "ROE": roe_value,
            "型態" if lang == "zh" else "Pattern": " / ".join([pattern_text(p, lang) for p in patterns[:2]]),
            "接近突破" if lang == "zh" else "Near Breakout": ("是" if lang == "zh" else "Yes") if "接近突破" in patterns else "",
            "多頭排列" if lang == "zh" else "Bullish Alignment": ("是" if lang == "zh" else "Yes") if "多頭排列" in patterns else "",
            "強勢整理" if lang == "zh" else "Strong Consolidation": ("是" if lang == "zh" else "Yes") if "強勢整理" in patterns else "",
        })

    return pd.DataFrame(rows)


def run_simple_screener(df, lang="zh", min_score=3, require_breakout=False, require_bull=False):
    if df.empty:
        return df

    score_col = "訊號分數" if lang == "zh" else "Signal Score"
    breakout_col = "接近突破" if lang == "zh" else "Near Breakout"
    bull_col = "多頭排列" if lang == "zh" else "Bullish Alignment"
    change_col = "漲跌幅" if lang == "zh" else "Change %"
    yes_value = "是" if lang == "zh" else "Yes"

    out = df.copy()
    out = out[out[score_col] >= min_score]

    if require_breakout:
        out = out[out[breakout_col] == yes_value]

    if require_bull:
        out = out[out[bull_col] == yes_value]

    return out.sort_values([score_col, change_col], ascending=[False, False])


# =========================
# AI Report
# =========================
def ai_report(api_key, data, quick_only=False, lang="zh"):
    today = datetime.now().strftime("%Y-%m-%d" if lang == "en" else "%Y年%m月%d日")
    client = genai.Client(api_key=api_key)

    if lang == "en":
        prompt = f"""
You are a stock research analyst. Write a formal, neutral, and conservative investment research report in English.

Date: {today}
Company: {data['name']}
Ticker: {data['symbol_used']}
Current Price: {data['price']}
Industry: {data['display_industry']}
Market: {data['market']}

PE: {data['pe']}
EPS: {data['eps']}
PB: {data['pb']}
ROE: {data['roe']}
Gross Margin: {data['gross']}
Revenue Growth: {data['revenue']}
Debt to Equity: {data['debt']}
Market Cap: {data.get('market_cap')}
52 Week High: {data.get('fifty_two_week_high')}
52 Week Low: {data.get('fifty_two_week_low')}

Support: {data['support']}
Resistance: {data['resistance']}
Bullish Signal Score: {data['bull']}%
Bearish Signal Score: {data['bear']}%
Target Price: {data['target_up']}
Risk Price: {data['target_down']}
Data Quality: {data['data_quality']}

Notes:
1. Do not guarantee profits.
2. Do not fabricate facts.
3. If data is insufficient, clearly state the limitations.
4. Treat “probability” as signal strength, not certainty.
"""
        if quick_only:
            prompt += """
Please output:
1. One-line summary (within 50 words)
2. 3 bullish reasons
3. 3 bearish/risk reasons
4. 2 key price levels to watch
"""
        else:
            prompt += """
Please output in this format:
# Investment Research Report

## 1. Company Overview
## 2. Fundamental Analysis
## 3. Technical Analysis
## 4. Bullish and Bearish Signal Interpretation
## 5. Risks
## 6. Investment Conclusion
## 7. Data Limitations
"""
    else:
        prompt = f"""
你是一位股票研究員，請用繁體中文撰寫正式、保守、中立的投資研究內容。

報告日期：{today}
股票名稱：{data['name']}
股票代號：{data['symbol_used']}
當前股價：{data['price']}
產業：{data['display_industry']}
市場：{data['market']}

PE：{data['pe']}
EPS：{data['eps']}
PB：{data['pb']}
ROE：{data['roe']}
毛利率：{data['gross']}
營收成長：{data['revenue']}
負債比：{data['debt']}
市值：{data.get('market_cap')}
52週高點：{data.get('fifty_two_week_high')}
52週低點：{data.get('fifty_two_week_low')}

支撐：{data['support']}
壓力：{data['resistance']}
多方訊號分數：{data['bull']}%
空方訊號分數：{data['bear']}%
目標價：{data['target_up']}
風險價：{data['target_down']}
資料品質：{data['data_quality']}

注意事項：
1. 嚴禁保證獲利。
2. 嚴禁編造不存在的事實。
3. 若資料不足，要明確指出資料限制。
4. 將「機率」理解為技術訊號強弱，不要寫成必然預測。
"""
        if quick_only:
            prompt += """
請輸出以下格式：
1. 一句話總結（50字內）
2. 看多理由 3 點
3. 看空/風險理由 3 點
4. 最適合觀察的關鍵價位 2 個
"""
        else:
            prompt += f"""
請依照以下格式輸出：
# {data['name']} ({data['symbol_used']}) 投資研究報告
撰寫日期：{today}｜股票代號：{data['symbol_used']}｜當前股價：{data['price']}元

## 1. 公司簡介
## 2. 基本面分析
## 3. 技術分析
## 4. 多方與空方訊號解讀
## 5. 投資風險
## 6. 投資結論
## 7. 資料限制與提醒
"""

    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return resp.text


# =========================
# Chart Helpers
# =========================
def format_chart_time(ts, interval="1d"):
    if not isinstance(ts, pd.Timestamp):
        ts = pd.Timestamp(ts)

    try:
        if ts.tzinfo is not None:
            ts = ts.tz_convert(None)
    except Exception:
        pass

    if interval in ["1h", "4h"]:
        return int(ts.timestamp())

    return ts.strftime("%Y-%m-%d")


def to_candle_data(df, interval="1d"):
    out = []
    for idx, row in df.iterrows():
        out.append({
            "time": format_chart_time(idx, interval),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
        })
    return out


def to_line_data(df, col, interval="1d"):
    out = []
    temp = df.dropna(subset=[col])
    for idx, row in temp.iterrows():
        out.append({
            "time": format_chart_time(idx, interval),
            "value": float(row[col]),
        })
    return out


def to_volume_data(df, interval="1d"):
    out = []
    for idx, row in df.iterrows():
        color = "rgba(239, 83, 80, 0.7)" if row["Close"] < row["Open"] else "rgba(38, 166, 154, 0.7)"
        out.append({
            "time": format_chart_time(idx, interval),
            "value": float(row["Volume"]),
            "color": color,
        })
    return out


def make_horizontal_line(df, value, interval="1d"):
    if value is None:
        return []
    return [
        {
            "time": format_chart_time(idx, interval),
            "value": float(value)
        }
        for idx in df.index
    ]


def build_tv_charts(df, interval="1d", show_volume=True, show_macd=True, show_rsi=False, support=None, resistance=None):
    candles = to_candle_data(df, interval)
    ma20 = to_line_data(df, "MA20", interval)
    ma60 = to_line_data(df, "MA60", interval)
    macd_line = to_line_data(df, "MACD", interval)
    signal_line = to_line_data(df, "MACD_SIGNAL", interval)
    hist_line = to_line_data(df, "MACD_HIST", interval)
    rsi_line = to_line_data(df, "RSI", interval)
    volume = to_volume_data(df, interval)

    support_line = make_horizontal_line(df, support, interval)
    resistance_line = make_horizontal_line(df, resistance, interval)

    price_series = [
        {
            "type": "Candlestick",
            "data": candles,
            "options": {
                "upColor": "#26a69a",
                "downColor": "#ef5350",
                "borderVisible": False,
                "wickUpColor": "#26a69a",
                "wickDownColor": "#ef5350",
            },
        },
        {
            "type": "Line",
            "data": ma20,
            "options": {
                "color": "#f5c542",
                "lineWidth": 2,
                "priceLineVisible": False,
                "crosshairMarkerVisible": False
            },
        },
        {
            "type": "Line",
            "data": ma60,
            "options": {
                "color": "#42a5f5",
                "lineWidth": 2,
                "priceLineVisible": False,
                "crosshairMarkerVisible": False
            },
        },
    ]

    if support_line:
        price_series.append({
            "type": "Line",
            "data": support_line,
            "options": {
                "color": "#66bb6a",
                "lineWidth": 1,
                "lineStyle": 2,
                "priceLineVisible": False,
                "crosshairMarkerVisible": False
            }
        })

    if resistance_line:
        price_series.append({
            "type": "Line",
            "data": resistance_line,
            "options": {
                "color": "#ef5350",
                "lineWidth": 1,
                "lineStyle": 2,
                "priceLineVisible": False,
                "crosshairMarkerVisible": False
            }
        })

    if show_volume:
        price_series.append({
            "type": "Histogram",
            "data": volume,
            "options": {
                "priceFormat": {"type": "volume"},
                "priceScaleId": "",
            },
            "priceScale": {
                "scaleMargins": {
                    "top": 0.8,
                    "bottom": 0,
                }
            }
        })

    base_chart = {
        "layout": {
            "background": {"type": "solid", "color": "#131722"},
            "textColor": "#d1d4dc",
        },
        "grid": {
            "vertLines": {"color": "rgba(42, 46, 57, 0.5)"},
            "horzLines": {"color": "rgba(42, 46, 57, 0.5)"},
        },
        "crosshair": {
            "vertLine": {"visible": False, "labelVisible": False},
            "horzLine": {"visible": False, "labelVisible": False}
        },
        "rightPriceScale": {"borderVisible": False},
        "timeScale": {
            "borderVisible": False,
            "timeVisible": True,
            "secondsVisible": False,
        },
    }

    chart_price = {
        "chart": base_chart,
        "series": price_series,
        "height": 520
    }

    chart_macd = {
        "chart": base_chart,
        "series": [
            {
                "type": "Histogram",
                "data": [
                    {
                        "time": x["time"],
                        "value": x["value"],
                        "color": "rgba(38, 166, 154, 0.7)" if x["value"] >= 0 else "rgba(239, 83, 80, 0.7)"
                    }
                    for x in hist_line
                ],
            },
            {
                "type": "Line",
                "data": macd_line,
                "options": {
                    "color": "#26a69a",
                    "lineWidth": 2,
                    "crosshairMarkerVisible": False
                },
            },
            {
                "type": "Line",
                "data": signal_line,
                "options": {
                    "color": "#ffb74d",
                    "lineWidth": 2,
                    "crosshairMarkerVisible": False
                },
            },
        ],
        "height": 220
    }

    chart_rsi = {
        "chart": base_chart,
        "series": [
            {
                "type": "Line",
                "data": rsi_line,
                "options": {
                    "color": "#ab47bc",
                    "lineWidth": 2,
                    "crosshairMarkerVisible": False
                },
            }
        ],
        "height": 180
    }

    charts = [chart_price]

    if show_macd:
        charts.append(chart_macd)

    if show_rsi:
        charts.append(chart_rsi)

    return charts


# =========================
# Watchlist Session
# =========================
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []


def add_to_watchlist(symbol):
    symbol = symbol.upper().strip()
    if symbol and symbol not in st.session_state.watchlist:
        st.session_state.watchlist.append(symbol)


def remove_from_watchlist(symbol):
    st.session_state.watchlist = [s for s in st.session_state.watchlist if s != symbol]


def build_watchlist_table(symbols, lang="zh"):
    rows = []
    for sym in symbols:
        d = get_stock(sym, interval="1d")
        if d.get("hist") is not None:
            quick = build_quick_summary(d, lang=lang)
            rows.append({
                tr("col_symbol", lang): d["raw_symbol"],
                "名稱" if lang == "zh" else "Name": d["name"],
                tr("col_price", lang): fmt_value(d["price"]),
                "漲跌幅" if lang == "zh" else "Change %": fmt_value(d["change_pct"]),
                tr("trend", lang): quick["trend"],
                tr("risk", lang): quick["risk"],
                "型態" if lang == "zh" else "Pattern": " / ".join([pattern_text(p, lang) for p in quick["patterns"][:2]]),
            })
    return pd.DataFrame(rows)


# =========================
# Sidebar
# =========================
with st.sidebar:
    language = st.selectbox("Language / 語言", ["繁體中文", "English"], index=0)
    lang = "zh" if language == "繁體中文" else "en"

    st.title(tr("sidebar_title", lang))

    api_key = st.text_input(tr("api_key", lang), type="password")
    symbol = st.text_input(tr("symbol", lang), value="AAPL")

    interval = st.selectbox(
        tr("interval", lang),
        ["1h", "4h", "1d", "1wk", "1mo"],
        index=2
    )

    show_volume = st.checkbox(tr("show_volume", lang), value=True)
    show_macd = st.checkbox(tr("show_macd", lang), value=True)
    show_rsi = st.checkbox(tr("show_rsi", lang), value=False)

    peer_input = st.text_input(tr("peer_input", lang), value="")

    scan_mode_options = [
        tr("scan_mode_core", lang),
        tr("scan_mode_300", lang),
        tr("scan_mode_800", lang),
    ]

    scan_mode = st.selectbox(
        tr("scan_mode", lang),
        scan_mode_options,
        index=0
    )

    scan_limit = st.slider(tr("scan_limit", lang), min_value=5, max_value=50, value=15, step=1)

    st.caption(tr("sidebar_caption", lang))

    colw1, colw2 = st.columns(2)
    with colw1:
        if st.button(tr("add_watchlist", lang)):
            add_to_watchlist(symbol)
    with colw2:
        if st.button(tr("remove_watchlist", lang)):
            remove_from_watchlist(symbol.upper().strip())

    if st.session_state.watchlist:
        st.markdown(f"### {tr('watchlist', lang)}")
        for s in st.session_state.watchlist:
            st.write(f"- {s}")


# =========================
# Title
# =========================
st.title(tr("app_title", lang))
st.caption(tr("app_caption", lang))


# =========================
# Market Opportunity Scanner
# =========================
def detect_opportunity(df):
    latest = df.iloc[-1]
    signals = []

    high20 = df["High"].rolling(20).max().iloc[-2]
    if latest["Close"] > high20:
        signals.append("Breakout")

    if latest["MA20"] > latest["MA60"]:
        if abs(latest["Close"] - latest["MA20"]) / latest["MA20"] < 0.02:
            signals.append("Pullback")

    if latest["RSI"] < 30:
        signals.append("RSI Oversold")

    vol_avg = df["Volume"].rolling(20).mean().iloc[-1]
    if latest["Volume"] > vol_avg * 2:
        signals.append("Volume Spike")

    return signals


def scan_market(symbols, lang="zh"):
    results = []

    signal_map = {
        "Breakout": tr("signal_breakout", lang),
        "Pullback": tr("signal_pullback", lang),
        "RSI Oversold": tr("signal_rsi_oversold", lang),
        "Volume Spike": tr("signal_volume_spike", lang),
    }

    for sym in symbols:
        data = get_stock(sym)

        if data.get("hist") is None:
            continue

        df = data["hist"]
        signals = detect_opportunity(df)

        if signals:
            translated_signals = [signal_map.get(s, s) for s in signals]
            results.append({
                tr("col_symbol", lang): sym,
                tr("col_price", lang): data["price"],
                tr("col_signals", lang): ", ".join(translated_signals)
            })

    return pd.DataFrame(results)


# =========================
# Main UI
# =========================
if symbol:
    symbol = symbol.upper().strip()
    data = get_stock(symbol, interval=interval)

    if data.get("hist") is not None:
        quick_summary = build_quick_summary(data, lang=lang)
        latest = data["hist"].iloc[-1]
        local_ai_brief = build_local_ai_brief(data, quick_summary, lang=lang)

        col_symbol = tr("col_symbol", lang)
        col_price = tr("col_price", lang)
        col_trend = tr("trend", lang)

        name_col = "名稱" if lang == "zh" else "Name"
        change_col = "漲跌幅" if lang == "zh" else "Change %"
        score_col = "訊號分數" if lang == "zh" else "Signal Score"
        pattern_col = "型態" if lang == "zh" else "Pattern"
        breakout_col = "接近突破" if lang == "zh" else "Near Breakout"
        yes_value = "是" if lang == "zh" else "Yes"

        # Hero
        c1, c2 = st.columns([2.2, 1.2])

        with c1:
            st.markdown(
                f"""
                <div class='hero-card'>
                    <div class='hero-title'>{data['name']}</div>
                    <div class='hero-sub'>
                        {tr("col_symbol", lang)}: {data['symbol_used']} ｜ 
                        {tr("market", lang)}: {market_text(data['market'], lang)} ｜ 
                        {tr("industry", lang)}: {data['display_industry']}
                    </div>
                    <div style='margin-top:12px;'>
                        <span class='badge'>{tr("data_quality", lang)}: {quality_text(data['data_quality'], lang)}</span>
                        <span class='badge'>{tr("display_period", lang)}: {data['interval']}</span>
                        <span class='badge'>{tr("fetch_period", lang)}: {data['period']}</span>
                        <span class='badge'>{tr("pattern", lang)}: {' / '.join([pattern_text(p, lang) for p in quick_summary['patterns'][:2]])}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            delta_text = f"{fmt_value(data['change'])} ({fmt_value(data['change_pct'])}%)"
            st.metric(
                label=f"{tr('current_price', lang)} {data['currency']}",
                value=fmt_value(data["price"]),
                delta=delta_text,
            )
            st.metric(
                "52W High / Low" if lang == "en" else "52週高 / 低",
                f"{fmt_value(data['fifty_two_week_high'])} / {fmt_value(data['fifty_two_week_low'])}"
            )
            st.metric(tr("market_cap", lang), fmt_large_num(data.get("market_cap")))

        s1, s2, s3, s4, s5 = st.columns(5)
        s1.metric(tr("trend", lang), quick_summary["trend"])
        s2.metric(tr("valuation", lang), quick_summary["valuation"])
        s3.metric(tr("risk", lang), quick_summary["risk"])
        s4.metric(tr("bull_signal", lang), f"{data['bull']}%")
        s5.metric(tr("bear_signal", lang), f"{data['bear']}%")

        st.info(quick_summary["one_line"])
        st.markdown(f"<div class='ai-box'>{local_ai_brief}</div>", unsafe_allow_html=True)

        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            tr("tab_overview", lang),
            tr("tab_technical", lang),
            tr("tab_fundamental", lang),
            tr("tab_ranking", lang),
            tr("tab_screener", lang),
            tr("tab_ai", lang),
            tr("tab_debug", lang),
        ])

        # =========================
        # Tab 1: Overview
        # =========================
        with tab1:
            left, right = st.columns([2.2, 1])

            with left:
                st.markdown(tr("main_chart", lang))

                charts = build_tv_charts(
                    data["hist"],
                    interval=data["interval"],
                    show_volume=show_volume,
                    show_macd=show_macd,
                    show_rsi=show_rsi,
                    support=data["support"],
                    resistance=data["resistance"]
                )

                lightweight_charts_v5_component(
                    name=f"tv_chart_{data['symbol_used']}_{data['interval']}",
                    charts=charts,
                    height=980 if (show_macd or show_rsi) else 640
                )

            with right:
                st.markdown(tr("key_summary", lang))
                st.metric(tr("support", lang), fmt_value(data["support"]))
                st.metric(tr("resistance", lang), fmt_value(data["resistance"]))
                st.metric(tr("target_up", lang), fmt_value(data["target_up"]))
                st.metric(tr("target_down", lang), fmt_value(data["target_down"]))
                st.metric("RSI", fmt_value(latest["RSI"]))
                st.metric("MACD", fmt_value(latest["MACD"]))
                st.metric(tr("volume", lang), fmt_large_num(latest["Volume"]))

                st.markdown(tr("pattern_detect", lang))
                for p in quick_summary["patterns"]:
                    st.write(f"• {pattern_text(p, lang)}")

                st.markdown(tr("bull_reasons", lang))
                for item in quick_summary["bullish"]:
                    st.write(f"• {item}")

                st.markdown(tr("bear_reasons", lang))
                for item in quick_summary["bearish"]:
                    st.write(f"• {item}")

            st.markdown(tr("multi_timeframe", lang))
            mtf_df = get_multi_timeframe_summary(symbol, lang=lang)
            st.dataframe(mtf_df, width="stretch", hide_index=True)

            st.markdown(tr("signal_table", lang))
            signal_df = generate_signal_table(data["hist"], data["support"], data["resistance"], lang=lang)
            st.dataframe(signal_df, width="stretch", hide_index=True)

            if st.session_state.watchlist:
                st.markdown(tr("watchlist_overview", lang))
                watch_df = build_watchlist_table(st.session_state.watchlist, lang=lang)
                if not watch_df.empty:
                    st.dataframe(watch_df, width="stretch", hide_index=True)

            st.markdown(tr("today_opportunities", lang))

            tw_op_df = scan_market(get_tw_scan_symbols(scan_mode)[:scan_limit], lang=lang)
            us_op_df = scan_market(get_us_scan_symbols(scan_mode)[:scan_limit], lang=lang)

            op_tab1, op_tab2 = st.tabs([tr("tw_opportunities", lang), tr("us_opportunities", lang)])

            with op_tab1:
                if not tw_op_df.empty:
                    st.dataframe(tw_op_df, width="stretch", hide_index=True)
                else:
                    st.caption(tr("no_tw_opportunities", lang))

            with op_tab2:
                if not us_op_df.empty:
                    st.dataframe(us_op_df, width="stretch", hide_index=True)
                else:
                    st.caption(tr("no_us_opportunities", lang))

        # =========================
        # Tab 2: Technical
        # =========================
        with tab2:
            c1, c2, c3 = st.columns(3)

            c1.metric("MA20", fmt_value(latest["MA20"]))
            c1.metric("MA60", fmt_value(latest["MA60"]))
            c1.metric(tr("close", lang), fmt_value(latest["Close"]))

            c2.metric("RSI", fmt_value(latest["RSI"]))
            c2.metric("MACD", fmt_value(latest["MACD"]))
            c2.metric("Signal", fmt_value(latest["MACD_SIGNAL"]))

            c3.metric("MACD Hist", fmt_value(latest["MACD_HIST"]))
            c3.metric(tr("volume", lang), fmt_large_num(latest["Volume"]))
            c3.metric(tr("ma20_avg_vol", lang), fmt_large_num(data["hist"]["Volume"].rolling(20).mean().iloc[-1]))

            st.markdown(tr("tech_interpret", lang))
            st.write(f"- {tr('trend_rating', lang)}：{quick_summary['trend']}")
            st.write(f"- {tr('support_resistance', lang)}：{fmt_value(data['support'])} / {fmt_value(data['resistance'])}")
            st.write(f"- {tr('bull_strength', lang)}：{data['bull']}%")
            st.write(f"- {tr('bear_strength', lang)}：{data['bear']}%")
            st.write(f"- {tr('pattern', lang)}：{' / '.join([pattern_text(p, lang) for p in quick_summary['patterns']])}")
            st.write(f"- {tr('tech_note', lang)}")

        # =========================
        # Tab 3: Fundamentals / Peers
        # =========================
        with tab3:
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("PE", fmt_value(data["pe"]))
            b2.metric("PB", fmt_value(data["pb"]))
            b3.metric("EPS", fmt_value(data["eps"]))
            b4.metric("ROE", fmt_ratio(data["roe"]))

            b5, b6, b7, b8 = st.columns(4)
            b5.metric(tr("gross_margin", lang), fmt_ratio(data["gross"]))
            b6.metric(tr("revenue_growth", lang), fmt_ratio(data["revenue"]))
            b7.metric(tr("debt_ratio", lang), fmt_value(data["debt"]))
            b8.metric(tr("valuation_grade", lang), quick_summary["valuation"])

            st.markdown(tr("fundamental_observe", lang))
            st.write(f"- {tr('valuation_now', lang)}：{quick_summary['valuation']}")
            st.write(f"- {tr('quality_status', lang)}：{quality_text(data['data_quality'], lang)}")
            st.write(f"- {tr('industry_label', lang)}：{data['display_industry']}")
            st.write(f"- {tr('yahoo_backup_note', lang)}")

            st.markdown(tr("peer_compare", lang))
            manual_peer_symbols = [x.strip().upper() for x in peer_input.split(",") if x.strip()]
            peer_symbols = manual_peer_symbols if manual_peer_symbols else auto_find_peers(data, max_peers=5)

            peer_df = build_peer_compare_table(peer_symbols, lang=lang, max_items=6)
            if not peer_df.empty:
                st.dataframe(peer_df, width="stretch", hide_index=True)
                if manual_peer_symbols:
                    st.caption(tr("manual_peer_used", lang))
                else:
                    st.caption(tr("auto_peer_used", lang))
            else:
                st.warning(tr("peer_invalid", lang))

        # =========================
        # Tab 4: Ranking
        # =========================
        with tab4:
            st.markdown(tr("ranking_title", lang))

            tw_symbols = get_tw_scan_symbols(scan_mode)
            us_symbols = get_us_scan_symbols(scan_mode)

            tw_rank_df = scan_universe(tuple(tw_symbols), lang=lang, limit=scan_limit)
            us_rank_df = scan_universe(tuple(us_symbols), lang=lang, limit=scan_limit)

            subtab1, subtab2 = st.tabs([tr("tw_ranking", lang), tr("us_ranking", lang)])

            with subtab1:
                st.markdown(tr("tw_top", lang))
                if tw_rank_df.empty:
                    st.warning(tr("no_tw_rank", lang))
                else:
                    tw_top_signal = tw_rank_df.sort_values(
                        [score_col, change_col],
                        ascending=[False, False]
                    ).head(10)

                    tw_top_breakout = tw_rank_df[
                        tw_rank_df[breakout_col] == yes_value
                    ].sort_values(
                        [score_col, change_col],
                        ascending=[False, False]
                    ).head(10)

                    st.dataframe(
                        tw_top_signal[[col_symbol, name_col, col_price, change_col, score_col, col_trend, pattern_col]],
                        width="stretch",
                        hide_index=True
                    )

                    st.markdown(tr("tw_breakout", lang))
                    if not tw_top_breakout.empty:
                        st.dataframe(
                            tw_top_breakout[[col_symbol, name_col, col_price, change_col, score_col, pattern_col]],
                            width="stretch",
                            hide_index=True
                        )
                    else:
                        st.caption(tr("no_tw_breakout", lang))

            with subtab2:
                st.markdown(tr("us_top", lang))
                if us_rank_df.empty:
                    st.warning(tr("no_us_rank", lang))
                else:
                    us_top_signal = us_rank_df.sort_values(
                        [score_col, change_col],
                        ascending=[False, False]
                    ).head(10)

                    us_top_breakout = us_rank_df[
                        us_rank_df[breakout_col] == yes_value
                    ].sort_values(
                        [score_col, change_col],
                        ascending=[False, False]
                    ).head(10)

                    st.dataframe(
                        us_top_signal[[col_symbol, name_col, col_price, change_col, score_col, col_trend, pattern_col]],
                        width="stretch",
                        hide_index=True
                    )

                    st.markdown(tr("us_breakout", lang))
                    if not us_top_breakout.empty:
                        st.dataframe(
                            us_top_breakout[[col_symbol, name_col, col_price, change_col, score_col, pattern_col]],
                            width="stretch",
                            hide_index=True
                        )
                    else:
                        st.caption(tr("no_us_breakout", lang))

        # =========================
        # Tab 5: Screener
        # =========================
        with tab5:
            st.markdown(tr("screener_title", lang))

            subtab_sc1, subtab_sc2 = st.tabs([tr("tw_screener", lang), tr("us_screener", lang)])

            with subtab_sc1:
                st.markdown(tr("tw_filter", lang))
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    tw_min_score = st.slider(
                        tr("min_score", lang),
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        key="tw_screen_min_score"
                    )
                with sc2:
                    tw_require_breakout = st.checkbox(
                        tr("only_breakout", lang),
                        value=False,
                        key="tw_require_breakout"
                    )
                with sc3:
                    tw_require_bull = st.checkbox(
                        tr("only_bull", lang),
                        value=False,
                        key="tw_require_bull"
                    )

                tw_symbols = get_tw_scan_symbols(scan_mode)
                tw_screen_df = scan_universe(tuple(tw_symbols), lang=lang, limit=scan_limit)
                tw_filtered = run_simple_screener(
                    tw_screen_df,
                    lang=lang,
                    min_score=tw_min_score,
                    require_breakout=tw_require_breakout,
                    require_bull=tw_require_bull
                )

                if tw_filtered.empty:
                    st.warning(tr("no_tw_filtered", lang))
                else:
                    st.dataframe(
                        tw_filtered[[col_symbol, name_col, col_price, change_col, score_col, col_trend, "RSI", pattern_col]],
                        width="stretch",
                        hide_index=True
                    )

            with subtab_sc2:
                st.markdown(tr("us_filter", lang))
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    us_min_score = st.slider(
                        tr("min_score", lang),
                        min_value=1,
                        max_value=5,
                        value=3,
                        step=1,
                        key="us_screen_min_score"
                    )
                with sc2:
                    us_require_breakout = st.checkbox(
                        tr("only_breakout", lang),
                        value=False,
                        key="us_require_breakout"
                    )
                with sc3:
                    us_require_bull = st.checkbox(
                        tr("only_bull", lang),
                        value=False,
                        key="us_require_bull"
                    )

                us_symbols = get_us_scan_symbols(scan_mode)
                us_screen_df = scan_universe(tuple(us_symbols), lang=lang, limit=scan_limit)
                us_filtered = run_simple_screener(
                    us_screen_df,
                    lang=lang,
                    min_score=us_min_score,
                    require_breakout=us_require_breakout,
                    require_bull=us_require_bull
                )

                if us_filtered.empty:
                    st.warning(tr("no_us_filtered", lang))
                else:
                    st.dataframe(
                        us_filtered[[col_symbol, name_col, col_price, change_col, score_col, col_trend, "RSI", pattern_col]],
                        width="stretch",
                        hide_index=True
                    )

        # =========================
        # Tab 6: AI
        # =========================
        with tab6:
            st.markdown(tr("ai_quick", lang))

            qa, qb = st.columns([1, 1])

            with qa:
                if st.button(tr("gen_ai_quick", lang)):
                    if not api_key:
                        st.error(tr("enter_api_key", lang))
                    else:
                        try:
                            with st.spinner(tr("ai_quick_loading", lang)):
                                quick_ai = ai_report(api_key, data, quick_only=True, lang=lang)
                            st.session_state["quick_ai_report"] = quick_ai
                        except Exception as e:
                            st.error(f"{tr('ai_quick_failed', lang)}{e}")

            with qb:
                if st.button(tr("gen_ai_full", lang)):
                    if not api_key:
                        st.error(tr("enter_api_key", lang))
                    else:
                        try:
                            with st.spinner(tr("ai_full_loading", lang)):
                                full_ai = ai_report(api_key, data, quick_only=False, lang=lang)
                            st.session_state["full_ai_report"] = full_ai
                        except Exception as e:
                            st.error(f"{tr('ai_full_failed', lang)}{e}")

            st.markdown(tr("ai_system_conclusion", lang))
            st.markdown(f"<div class='ai-box'>{local_ai_brief}</div>", unsafe_allow_html=True)

            if "quick_ai_report" in st.session_state:
                st.markdown(st.session_state["quick_ai_report"])

            st.markdown(tr("ai_full", lang))
            if "full_ai_report" in st.session_state:
                st.markdown(st.session_state["full_ai_report"])
            else:
                st.caption(tr("ai_full_caption", lang))

        # =========================
        # Tab 7: Debug
        # =========================
        with tab7:
            st.markdown(tr("debug_status", lang))

            item_col = tr("status_item", lang)
            value_col = tr("status_value", lang)

            status_rows = [
                {item_col: tr("actual_symbol", lang), value_col: data["symbol_used"]},
                {item_col: tr("raw_symbol", lang), value_col: data["raw_symbol"]},
                {item_col: tr("data_source", lang), value_col: tr("source_yahoo", lang)},
                {item_col: tr("display_interval", lang), value_col: data["interval"]},
                {item_col: tr("fetch_interval", lang), value_col: data["fetch_interval"]},
                {item_col: tr("fetch_period", lang), value_col: data["period"]},
                {item_col: tr("data_quality", lang), value_col: quality_text(data["data_quality"], lang)},
                {item_col: "Sector", value_col: data["sector"]},
                {item_col: "Industry", value_col: data["industry"]},
            ]

            st.dataframe(pd.DataFrame(status_rows), width="stretch", hide_index=True)

            st.markdown(tr("debug_errors", lang))
            if data.get("errors"):
                for err in data["errors"]:
                    st.write(f"- {err}")
            else:
                st.write(tr("no_error", lang))

    else:
        st.error(tr("no_data", lang))

        if data.get("errors"):
            with st.expander(tr("try_symbol_errors", lang)):
                for err in data["errors"]:
                    st.write(f"- {err}")