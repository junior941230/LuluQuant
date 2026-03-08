from UI.UImainWindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow,QButtonGroup
import pyqtgraph as pg  
from frontEnd.graph import CandlestickItem
from backEnd.backend import Backtest ,TransformPrice

class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ApiHandle = Backtest()
        self.startDate = "1994-10-01"

        self.canvas = pg.GraphicsLayoutWidget()
        self.ui.chartLayout.addWidget(self.canvas)

        self.plotItem = self.canvas.addPlot(title="股市數據模擬")
        self.plotItem.showGrid(x=True, y=True)
        
        self.ui.UserInStartBackTest.clicked.connect(self.runBackTest)
        self.group = QButtonGroup(self)
        self.group.addButton(self.ui.UserInDayCandleMode)
        self.group.addButton(self.ui.UserInWeekCandleMode)
        self.group.addButton(self.ui.UserInMonthCandleMode)
        self.group.buttonClicked.connect(self.graphPlot)

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
        

    def graphPlot(self):
        self.plotItem.clear()
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
        candlestickItem = CandlestickItem(stockData)
        self.plotItem.addItem(candlestickItem)
