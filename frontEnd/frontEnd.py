from UI.UImainWindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow,QButtonGroup
import pyqtgraph as pg  
from frontEnd.graph import CandlestickItem,StrategyItem,DateAxisItem
from backEnd.backend import Backtest ,TransformPrice

class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ApiHandle = Backtest()
        self.startDate = "1994-10-01"
        self.dateStrings = [] # 用於儲存當前數據的日期對應表

        self.dateAxis = DateAxisItem(dates=self.dateStrings, orientation='bottom')
        self.canvas = pg.GraphicsLayoutWidget()
        self.ui.chartLayout.addWidget(self.canvas)
        # 重要：在 addPlot 時指定 axisItems
        self.plotItem = self.canvas.addPlot(
            title="股市數據模擬", 
            axisItems={'bottom': self.dateAxis}
        )
        self.plotItem.showGrid(x=True, y=True)
        
        self.ui.UserInStartBackTest.clicked.connect(self.runBackTest)
        self.group = QButtonGroup(self)
        self.group.addButton(self.ui.UserInDayCandleMode)
        self.group.addButton(self.ui.UserInWeekCandleMode)
        self.group.addButton(self.ui.UserInMonthCandleMode)
        self.group.buttonClicked.connect(self.graphPlot)

        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen='y')
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen='y')
        self.plotItem.addItem(self.vLine, ignoreBounds=True)
        self.plotItem.addItem(self.hLine, ignoreBounds=True)
        self.label = pg.TextItem(anchor=(0, 1), color='y', fill=(0, 0, 0, 100))
        self.plotItem.addItem(self.label, ignoreBounds=True)

        # 3. 設定滑鼠移動監聽 (使用 SignalProxy 避免過度頻繁觸發)
        self.proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)

        #預先畫好標的歷史圖表
        self.graphPlot()
        
    def runBackTest(self):
        stockid = self.ui.UserInStockID.text()
        startDate = self.ui.UserInStartDate.text()
        endDate = self.ui.UserInEndDate.text()
        traderFund = int(self.ui.UserInFund.text())
        fee = float(self.ui.UserInFee.text()) *0.01
        stockData = self.ApiHandle.getData(stockId=stockid, startDate=startDate, endDate=endDate)
        self.ApiHandle.runSimulation(stockData, traderFund=traderFund, feeRate=fee)
        maxDropDown,tradeNum,tradingHistory = self.ApiHandle.processResult()
        strategyItem = StrategyItem(stockData, tradingHistory)
        self.plotItem.addItem(strategyItem)

    def graphPlot(self):
        self.plotItem.clear()
        # 重新加入十字準星與標籤 (因為 clear 會清空所有 Item)
        self.plotItem.addItem(self.vLine, ignoreBounds=True)
        self.plotItem.addItem(self.hLine, ignoreBounds=True)
        self.plotItem.addItem(self.label, ignoreBounds=True)
        period = ""
        if self.group.checkedButton() == self.ui.UserInDayCandleMode:
            period = "D"
        elif self.group.checkedButton() == self.ui.UserInWeekCandleMode:
            period = "W"
        elif self.group.checkedButton() == self.ui.UserInMonthCandleMode:
            period = "M"
        stockid = self.ui.UserInStockID.text()
        endDate = self.ui.UserInEndDate.text()
        stockData = self.ApiHandle.getData(stockId=stockid, startDate=self.startDate, endDate=endDate)
        stockData = TransformPrice(stockData,period)
        stockData = stockData.reset_index(drop=True)
        # 更新 DateAxisItem 裡面的日期清單
        # 假設你的 stockData 裡面有 'date' 欄位
        self.dateStrings = stockData['date'].dt.strftime('%Y-%m-%d').tolist()
        self.dateAxis.dates = self.dateStrings 

        candlestickItem = CandlestickItem(stockData)
        self.plotItem.addItem(candlestickItem)

    def mouseMoved(self, evt):
        pos = evt[0]  # 取得滑鼠座標
        if self.plotItem.sceneBoundingRect().contains(pos):
            mousePoint = self.plotItem.vb.mapSceneToView(pos)
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
