import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from backtest import runSimulation, getBacktestData

st.set_page_config(layout="wide")

def plotTradingView(rawDf, backtestObj):
    tradeDetail = backtestObj.trade_detail
    
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05, 
        subplot_titles=("K線與交易訊號", "策略累積報酬率"),
        row_heights=[0.7, 0.3]
    )

    fig.add_trace(go.Candlestick(
        x=rawDf["date"], open=rawDf["open"], high=rawDf["max"],
        low=rawDf["min"], close=rawDf["close"], name="股價"
    ), row=1, col=1)

    if not tradeDetail.empty:
        # 修正：使用 signal 判斷買賣方向
        buySignals = tradeDetail[tradeDetail["signal"] > 0]
        sellSignals = tradeDetail[tradeDetail["signal"] < 0]

        # 修正：FinMind 的成交價格欄位名稱為 trade_price
        fig.add_trace(go.Scatter(
            x=buySignals["date"], y=buySignals["trade_price"],
            mode="markers", marker=dict(symbol="triangle-up", size=12, color="#00ff00"),
            name="買入"
        ), row=1, col=1)

        fig.add_trace(go.Scatter(
            x=sellSignals["date"], y=sellSignals["trade_price"],
            mode="markers", marker=dict(symbol="triangle-down", size=12, color="#ff0000"),
            name="賣出"
        ), row=1, col=1)

    compareDetail = backtestObj.compare_market_detail
    if not compareDetail.empty and "strategy_return" in compareDetail.columns:
        fig.add_trace(go.Scatter(
            x=compareDetail["date"], y=compareDetail["strategy_return"],
            line=dict(color="#2962FF", width=2), name="策略報酬率"
        ), row=2, col=1)

    fig.update_layout(height=800, template="plotly_dark", xaxis_rangeslider_visible=False)
    return fig

st.title("FinMind 策略回測視覺化工具")

with st.sidebar:
    st.header("設定參數")
    stockId = st.text_input("股票代碼", value="00940")
    inputFund = st.number_input("初始資金", value=500000)
    dateRange = st.date_input("時間範圍", [pd.to_datetime("2024-04-01"), pd.to_datetime("2026-03-06")])

if len(dateRange) == 2:
    startStr = dateRange[0].strftime("%Y-%m-%d")
    endStr = dateRange[1].strftime("%Y-%m-%d")

    if st.button("開始模擬"):
        with st.spinner("資料抓取與運算中..."):
            resultObj = runSimulation(stockId, startStr, endStr, inputFund)
            rawDf = getBacktestData(stockId, startStr, endStr)
            
            col1, col2, col3, col4, col5 = st.columns(5)
            # col1.metric("總損益", f"{result["FinalProfit"]:,.0f}", f"{result["FinalProfitPer"]:.2f}%")
            # col2.metric("最大資產回撤", f"{result["MaxLoss"]:.2f}",f"{result["MaxLossPer"]:.2f}%")
            # col3.metric("總交易量", f"{tradesCount}")
            # col4.metric("獲利因子", f"{profitFactor:.3f}")
            # col5.metric("獲利交易", f"{winRate:.2f}% ({winningTrades}/{tradesCount})")

            # if not tradeDetail.empty:
            #     # 1. 計算總損益
            #     finalFund = tradeDetail["trader_fund"].iloc[-1]
            #     finalProfit = finalFund - inputFund
            #     profitRate = (finalProfit / inputFund) * 100
                
            #     # 2. 配對買賣紀錄以計算勝率與獲利因子
            #     buyRecords = tradeDetail[tradeDetail["signal"] > 0].reset_index(drop=True)
            #     sellRecords = tradeDetail[tradeDetail["signal"] < 0].reset_index(drop=True)
                
            #     # 確保買賣次數配對，避免最後一筆買入但尚未賣出的情況導致報錯
            #     tradesCount = min(len(buyRecords), len(sellRecords))
            #     winningTrades = 0
            #     grossProfit = 0.0
            #     grossLoss = 0.0
                
            #     for i in range(tradesCount):
            #         # 修正：欄位名稱更正為 trade_price
            #         buyPrice = buyRecords.loc[i, "trade_price"]
            #         sellPrice = sellRecords.loc[i, "trade_price"]
            #         tradeProfit = sellPrice - buyPrice
                    
            #         if tradeProfit > 0:
            #             winningTrades += 1
            #             grossProfit += tradeProfit
            #         else:
            #             grossLoss += abs(tradeProfit)
                
            #     winRate = (winningTrades / tradesCount * 100) if tradesCount > 0 else 0.0
            #     profitFactor = (grossProfit / grossLoss) if grossLoss > 0 else (float('inf') if grossProfit > 0 else 0.0)
                
            #     # 3. 計算最大資產回撤 (MDD)
            #     performanceDf = resultObj.compare_market_detail
            #     if not tradeDetail.empty and "trader_fund" in tradeDetail.columns:
            #         equityCurve = tradeDetail["trader_fund"]
            #         rollMax = equityCurve.cummax()
            #         drawdowns = (equityCurve - rollMax) / rollMax
            #         maxDrawdown = drawdowns.min() * 100
            #     else:
            #         maxDrawdown = 0.0

            #     # 4. 渲染 5 個指標
            #     col1, col2, col3, col4, col5 = st.columns(5)
            #     col1.metric("總損益", f"{finalProfit:,.0f}", f"{profitRate:.2f}%")
            #     col2.metric("最大資產回撤", f"{maxDrawdown:.2f}%")
            #     col3.metric("總交易量", f"{tradesCount}")
            #     col4.metric("獲利因子", f"{profitFactor:.3f}")
            #     col5.metric("獲利交易", f"{winRate:.2f}% ({winningTrades}/{tradesCount})")
            # else:
            #     st.warning("此區間內無交易紀錄，無法計算損益與指標。")

            # fig = plotTradingView(rawDf, resultObj)
            
            # # 修正：解決即將棄用的警告，改用 width="stretch"
            # st.plotly_chart(fig, width="stretch")
            
            # st.subheader("交易明細")
            # st.dataframe(tradeDetail, width="stretch")