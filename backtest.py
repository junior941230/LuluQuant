from FinMind.data import DataLoader
import json
from stragegy import MaCross,RSI_WR_AND
import backtrader as bt
import pandas as pd

class FinMindApi:
    def __init__(self):
        try:
            with open('token.json', 'r') as f:
                tokenInfo = json.load(f)
                apiToken = tokenInfo.get('token', '')
        except FileNotFoundError:
            apiToken = ""

        self.api = DataLoader()
        if apiToken:
            self.api.login_by_token(api_token=apiToken)
        self.apiUsageCheck()
        print("FinMind API 初始化完成")
        print(f"目前 API 使用量: {self.api.api_usage}/{self.api.api_usage_limit}")
    
    def apiUsageCheck(self):
        if(self.api.api_usage >= self.api.api_usage_limit *0.9):
            print("API 次數已達90%，請注意使用量！")

    def getBacktestData(self, stockId, startDate, endDate):
        rawDf = self.api.taiwan_stock_daily(
            stock_id=stockId,
            start_date=startDate,
            end_date=endDate
        )
        return rawDf 
    
    def FinMindDataToBacktrader(self,rawDf):
        stockData = rawDf.rename(columns={
            "max": "high",
            "min": "low",
            "Trading_Volume": "volume"
        })
        # 將 date 欄位轉換為時間物件，並設定為 Index
        stockData["date"] = pd.to_datetime(stockData["date"])
        stockData = stockData.set_index("date")
        # 剔除不必要的欄位 (如 stock_id, Trading_money 等)，只保留開高低收與成交量
        # 並確保資料型態為浮點數，避免 Backtrader 運算報錯
        columnsToKeep = ["open", "high", "low", "close", "volume"]
        cleanData = stockData[columnsToKeep].astype(float)
        return bt.feeds.PandasData(dataname=cleanData)

class Backtest(FinMindApi):
    def __init__(self):
        super().__init__()
        self.fee = 0.001425  # 假設的交易費用率，可以根據實際情況調整
        self.result = None

    # 修正：傳入動態參數
    def runSimulation(self, stockId, startDate, endDate, traderFund):
        self.traderFund = traderFund
        cerebro = bt.Cerebro()
        data = self.getBacktestData(stockId, startDate, endDate)       
        data = self.FinMindDataToBacktrader(data) 
        cerebro.adddata(data)
        cerebro.addstrategy(RSI_WR_AND)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeStats')
        cerebro.broker.setcash(traderFund)
        cerebro.broker.setcommission(commission=0.001425)
        self.result = cerebro.run()
        self.finalProfit = cerebro.broker.getvalue()
        self.cerebro = cerebro

    def processResult(self):
        firstStrategyResult = self.result[0]
        drawdownData = firstStrategyResult.analyzers.drawdown.get_analysis()
        print(f"最大回撤: {drawdownData.max.drawdown}%")
        tradeAnalysis = firstStrategyResult.analyzers.tradeStats.get_analysis()
        # 印出總共完成(已平倉)的交易次數，這等同於你的總賣單數
        totalClosedTrades = tradeAnalysis.total.closed
        print(f"總共完成的交易次數 (平倉/賣出): {totalClosedTrades}")
        print(f"最終資產淨值: {self.finalProfit}")
        print(f"總損益: {(self.finalProfit - self.traderFund)/self.traderFund * 100:.2f}%")
        # self.cerebro.plot()