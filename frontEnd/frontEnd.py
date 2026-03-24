from UI.UImainWindow import Ui_MainWindow
from PyQt6.QtWidgets import QMainWindow, QButtonGroup, QLineEdit, QCompleter, QDialog
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QDate
import pyqtgraph as pg
from frontEnd.graph import CandlestickItem, StrategyItem, DateAxisItem, showResult
from backEnd.backend import *
from frontEnd.strategyCodeBlock import PythonEditor
from frontEnd.saveStrategy import SaveStrategyDialog
from datetime import datetime


# 主視窗控制器類別
class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setting = loadSettingFile()  # 載入設定檔
        self.setSettingParams()  # 設定參數
        self.ApiHandle = Backtest()  # 初始化回測物件
        self.startDate = "1994-10-01"  # 預設起始日期
        self.dateStrings = []  # 用於儲存當前數據的日期對應表
        self.stockInfo = self.ApiHandle.getAllTaiwanStockInfo()  # 取得台灣股票資訊
        self.ui.StockIDSerchingBar.setClearButtonEnabled(True)  # 啟用搜尋欄位清除按鈕
        searchStockAction = QAction(self.ui.StockIDSerchingBar)
        searchStockAction.setIcon(QIcon.fromTheme("edit-find"))  # 使用系統內建圖示
        self.ui.StockIDSerchingBar.addAction(
            searchStockAction, QLineEdit.ActionPosition.LeadingPosition)
        self.updateStockIDSerchingBarCompleter()  # 更新自動完成列表
        # 連接股票編號搜尋欄位的事件
        self.ui.StockIDSerchingBar.returnPressed.connect(
            self.onStockIDSerchingBarEnter)
        self.ui.StockIDSerchingBar.editingFinished.connect(
            self.onStockIDSerchingBarEnter)
        self.candlePlotInit()  # 初始化蠟燭圖
        self.codeBlockInit()  # 初始化程式碼區塊

    # 設定參數值
    def setSettingParams(self):
        self.ui.StockIDSerchingBar.setText(self.setting.get("StockId", ""))
        self.ui.StrategySerchingBar.setText(self.setting.get("Strategy", ""))
        self.ui.UserInStartDate.setDate(QDate.fromString(
            self.setting.get("startDate", "2024-01-01"), "yyyy-M-d"))
        self.ui.UserInEndDate.setDate(QDate.fromString(
            self.setting.get("endDate", "2026-03-21"), "yyyy-M-d"))

    # 關閉視窗時保存設定
    def close(self):
        saveSettingFile(self.setting)

    # 初始化蠟燭圖表
    def candlePlotInit(self):
        # 建立日期軸
        self.dateAxis = DateAxisItem(
            dates=self.dateStrings, orientation='bottom')
        # 建立繪圖畫布
        self.canvas = pg.GraphicsLayoutWidget()
        self.ui.chartLayout.addWidget(self.canvas)
        # 重要：在 addPlot 時指定 axisItems
        self.plotItem = self.canvas.addPlot(
            title=self.ui.StockIDSerchingBar.text(),
            axisItems={'bottom': self.dateAxis}
        )
        self.plotItem.showGrid(x=True, y=True)  # 顯示網格線

        # 建立時間週期選擇按鈕群組
        self.group = QButtonGroup(self)
        self.group.addButton(self.ui.UserInDayCandleMode)
        self.group.addButton(self.ui.UserInWeekCandleMode)
        self.group.addButton(self.ui.UserInMonthCandleMode)
        self.group.buttonClicked.connect(lambda: self.graphPlot(
            endDate=self.ui.UserInEndDate.text()))  # 連接按鈕事件

        # 建立十字準星
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen='y')
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen='y')
        self.plotItem.addItem(self.vLine, ignoreBounds=True)
        self.plotItem.addItem(self.hLine, ignoreBounds=True)
        # 建立滑鼠追蹤標籤
        self.label = pg.TextItem(anchor=(0, 1), color='y', fill=(0, 0, 0, 100))
        self.plotItem.addItem(self.label, ignoreBounds=True)

        # 設定滑鼠移動監聽 (使用 SignalProxy 避免過度頻繁觸發)
        self.proxy = pg.SignalProxy(self.plotItem.scene(
        ).sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        # 預先畫好標的歷史圖表
        if self.ui.StockIDSerchingBar.text() in self.stockInfo['stock_id'].values:
            today = datetime.today().strftime('%Y-%m-%d')
            self.graphPlot(endDate=today)

    # 初始化程式碼編輯區塊
    def codeBlockInit(self):
        self.codeBlock = PythonEditor()  # 建立 Python 編輯器
        self.ui.codeLayout.addWidget(self.codeBlock)
        self.ui.StrategySerchingBar.setClearButtonEnabled(True)  # 啟用搜尋欄位清除按鈕
        searchAction = QAction(self.ui.StrategySerchingBar)
        searchAction.setIcon(QIcon.fromTheme("edit-find"))  # 使用系統內建圖示
        self.ui.StrategySerchingBar.addAction(
            searchAction, QLineEdit.ActionPosition.LeadingPosition)
        self.updateCodeBlockSerchingcompleter()  # 更新自動完成列表
        # 連接策略搜尋欄位的事件
        self.ui.StrategySerchingBar.returnPressed.connect(
            self.onStrategySerchingBarEnter)
        self.ui.StrategySerchingBar.editingFinished.connect(
            self.onStrategySerchingBarEnter)
        self.onStrategySerchingBarEnter()  # 預先載入策略
        # 連接按鈕事件
        self.ui.createNewStrategy.clicked.connect(self.createNewStrategy)
        self.ui.saveStrategy.clicked.connect(self.userSaveStrategy)
        self.ui.runStrategy.clicked.connect(self.userRunStrategy)

    # 更新程式碼區塊搜尋欄位的自動完成列表
    def updateCodeBlockSerchingcompleter(self):
        completer = QCompleter(findAllStrategys())
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.ui.StrategySerchingBar.setCompleter(completer)

    # 更新股票編號搜尋欄位的自動完成列表
    def updateStockIDSerchingBarCompleter(self):
        completer = QCompleter(self.stockInfo['stock_id'].values)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        completer.setFilterMode(Qt.MatchFlag.MatchContains)
        self.ui.StockIDSerchingBar.setCompleter(completer)

    # 建立新策略
    def createNewStrategy(self):
        self.updateCodeBlockSerchingcompleter()
        content = loadStrategysFile("custom")  # 載入預設範本
        self.codeBlock.setText(content)

    # 使用者保存策略
    def userSaveStrategy(self):
        if self.ui.StrategySerchingBar.text() in findAllStrategys():
            # 若策略存在，直接覆蓋
            saveStrategysFile(
                self.ui.StrategySerchingBar.text(), self.codeBlock.text())
        else:
            # 若策略不存在，開啟對話框讓使用者輸入名稱
            dialog = SaveStrategyDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                userInput = dialog.getName() + ".py"
                saveStrategysFile(userInput, self.codeBlock.text())
                self.ui.StrategySerchingBar.setText(userInput)

    # 使用者執行策略
    def userRunStrategy(self):
        # 儲存策略
        if self.ui.StrategySerchingBar.text() in findAllStrategys():
            saveStrategysFile(
                self.ui.StrategySerchingBar.text(), self.codeBlock.text())
            runStrategy(self.ApiHandle, self.ui.StrategySerchingBar.text())
        # 取得使用者輸入參數
        stockid = self.ui.StockIDSerchingBar.text()
        startDate = self.ui.UserInStartDate.text()
        endDate = self.ui.UserInEndDate.text()
        self.setting["startDate"] = startDate  # 保存到設定
        self.setting["endDate"] = endDate  # 保存到設定
        traderFund = int(self.ui.UserInFund.text())
        fee = float(self.ui.UserInFee.text()) * 0.01
        # 取得股票數據
        stockData = self.ApiHandle.getData(
            stockId=stockid, startDate=startDate, endDate=endDate)
        # 執行模擬交易
        self.ApiHandle.runSimulation(
            stockData, traderFund=traderFund, feeRate=fee)
        # 處理結果並輸出
        result = self.ApiHandle.processResult()
        strategyItem = StrategyItem(stockData, result["tradingHistory"])
        self.plotItem.addItem(strategyItem)
        showResult(self.ui, stockData, traderFund,
                   result)  # 顯示結果（可擴展為更詳細的報告或圖表）

    # 處理策略搜尋欄位的輸入
    def onStrategySerchingBarEnter(self):
        searchTerm = self.ui.StrategySerchingBar.text()
        files = findAllStrategys()
        if searchTerm in files:
            content = loadStrategysFile(searchTerm)
            if content != None:
                self.codeBlock.setText(content)  # 載入策略內容
                self.setting["Strategy"] = searchTerm  # 保存到設定

    # 處理股票編號搜尋欄位的輸入
    def onStockIDSerchingBarEnter(self):
        searchTerm = self.ui.StockIDSerchingBar.text()
        if searchTerm in self.stockInfo['stock_id'].values:
            today = datetime.today().strftime('%Y-%m-%d')
            self.graphPlot(endDate=today)  # 繪製圖表
            self.setting["StockId"] = searchTerm  # 保存到設定

    # 繪製圖表
    def graphPlot(self, endDate):
        self.plotItem.clear()  # 清空舊圖表
        # 重新加入十字準星與標籤 (因為 clear 會清空所有 Item)
        self.plotItem.addItem(self.vLine, ignoreBounds=True)
        self.plotItem.addItem(self.hLine, ignoreBounds=True)
        self.plotItem.addItem(self.label, ignoreBounds=True)
        # 根據按鈕選擇決定週期
        period = ""
        if self.group.checkedButton() == self.ui.UserInDayCandleMode:
            period = "D"  # 日線
        elif self.group.checkedButton() == self.ui.UserInWeekCandleMode:
            period = "W"  # 週線
        elif self.group.checkedButton() == self.ui.UserInMonthCandleMode:
            period = "M"  # 月線
        # 取得使用者輸入
        stockid = self.ui.StockIDSerchingBar.text()
        print(f"正在載入 {stockid} 從 {self.startDate} 到 {endDate} 的資料...")
        # 取得股票數據
        stockData = self.ApiHandle.getData(
            stockId=stockid, startDate=self.startDate, endDate=endDate)
        # 轉換價格數據週期
        stockData = TransformPrice(stockData, period)
        stockData = stockData.reset_index(drop=True)
        # 更新 DateAxisItem 裡面的日期清單
        self.dateStrings = stockData['date'].dt.strftime('%Y-%m-%d').tolist()
        self.dateAxis.dates = self.dateStrings

        # 建立蠟燭圖表項目並加入到圖表
        candlestickItem = CandlestickItem(stockData)
        self.plotItem.addItem(candlestickItem)

    # 處理滑鼠移動事件
    def mouseMoved(self, evt):
        pos = evt[0]  # 取得滑鼠座標
        if self.plotItem.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)  # 轉換座標到數據座標
            index = int(mousePoint.x())

            # 檢查索引是否在資料範圍內
            if 0 <= index < len(self.dateStrings):
                # 取得該索引對應的日期與價格
                dateStr = self.dateStrings[index]
                price = mousePoint.y()

                # 更新十字線位置
                self.vLine.setPos(mousePoint.x())
                self.hLine.setPos(mousePoint.y())

                # 更新標籤內容與位置
                self.label.setText(f"時間: {dateStr}\n價格: {price:.2f}")
                self.label.setPos(mousePoint.x(), mousePoint.y())
