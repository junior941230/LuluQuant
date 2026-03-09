from FinMind.data import DataLoader
import json
from backEnd.strategy import MaCross, RSI_WR_AND, TradeRecorder
import backtrader as bt
import pandas as pd
import os


def findAllStrategys():
    files = os.listdir("strategy")
    return files


def loadStrategysFile(filePath):
    filePath = "strategy/" + filePath
    with open(filePath, "r", encoding="utf-8") as f:
        fileContent = f.read()
    return fileContent


def saveStrategysFile(filePath, content):
    filePath = "strategy/" + filePath + ".py"
    with open(filePath, "w+", encoding="utf-8") as f:
        f.write(content)


def FinMindDataToBacktrader(rawDf):
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


def TransformPrice(df, period):
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    # 3. 轉換為每週資料 (Weekly)
    # 我們對不同欄位採用不同的計算方式
    if period == "W":
        df = df.resample('W').agg({
            'stock_id': 'first',             # 股票代碼維持不變
            'Trading_Volume': 'sum',         # 成交量加總
            'Trading_money': 'sum',          # 成交金額加總
            'open': 'first',                  # 開盤價取該週的第一個交易日
            'max': 'max',         # 週最高價：該週最大值
            'min': 'min',         # 週最低價：該週最小值
            'close': 'last',      # 週收盤價：該週最後一筆
            'spread': 'sum',      # 漲跌：通常週漲跌是週收盤減掉前週收盤，這裡暫用加總
            'Trading_turnover': 'sum'  # 成交筆數：總和
        })
    elif period == "M":
        # 4. 轉換為每月資料 (Monthly)
        df = df.resample('ME').agg({
            'stock_id': 'first',
            'Trading_Volume': 'sum',
            'Trading_money': 'sum',
            'open': 'first',
            'max': 'max',         # 週最高價：該週最大值
            'min': 'min',         # 週最低價：該週最小值
            'close': 'last',      # 週收盤價：該週最後一筆
            'spread': 'sum',      # 漲跌：通常週漲跌是週收盤減掉前週收盤，這裡暫用加總
            'Trading_turnover': 'sum'  # 成交筆數：總和
        })

    return df.reset_index()


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
        if (self.api.api_usage >= self.api.api_usage_limit * 0.9):
            print("API 次數已達90%，請注意使用量！")

    def getData(self, stockId, startDate, endDate):
        if not os.path.exists("cache"):
            os.makedirs("cache")
        cachedData = self.findCacheData(stockId, startDate, endDate)
        if cachedData is not None:
            return cachedData
        rawDf = self.api.taiwan_stock_daily(
            stock_id=stockId,
            start_date=startDate,
            end_date=endDate
        )
        rawDf.to_pickle(f"cache/{stockId}_{startDate}_{endDate}.pkl")
        return rawDf

    def findCacheData(self, stockId, startDate, endDate):
        files = os.listdir("cache")
        for file in files:
            endDateInFile = file.split("_")[-1].split(".")[0]
            startDateInFile = file.split("_")[1]
            if f"{stockId}" in file:
                # 檔案的日期範圍包含了使用者要求的日期範圍，才算找到快取資料
                if endDateInFile >= endDate and startDateInFile <= startDate:
                    cachedData = pd.read_pickle(f"cache/{file}")
                    print("找到快取資料，直接使用")
                    # 轉換 date 欄位為 datetime 格式，才能使用 between 方法過濾日期範圍
                    cachedData['date'] = pd.to_datetime(cachedData['date'])
                    filteredDf = cachedData[cachedData['date'].between(
                        startDate, endDate)]
                    return filteredDf
        print("沒有找到快取資料，將從 API 取得")
        return None


class Backtest(FinMindApi):
    def __init__(self):
        super().__init__()
        self.result = None

    # 修正：傳入動態參數
    def runSimulation(self, data, traderFund, feeRate):
        self.traderFund = traderFund
        cerebro = bt.Cerebro()
        data = FinMindDataToBacktrader(data)
        cerebro.adddata(data)
        cerebro.addstrategy(RSI_WR_AND)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeStats')
        cerebro.addanalyzer(TradeRecorder, _name='myRecorder')
        cerebro.broker.setcash(traderFund)
        cerebro.broker.setcommission(commission=feeRate)
        self.result = cerebro.run()
        self.finalProfit = cerebro.broker.getvalue()
        self.cerebro = cerebro

    def processResult(self):
        firstStrategyResult = self.result[0]
        drawdownData = firstStrategyResult.analyzers.drawdown.get_analysis()
        tradeAnalysis = firstStrategyResult.analyzers.tradeStats.get_analysis()
        finalTrades = firstStrategyResult.analyzers.myRecorder.get_analysis()
        return drawdownData.max.drawdown, tradeAnalysis.total.closed, finalTrades
