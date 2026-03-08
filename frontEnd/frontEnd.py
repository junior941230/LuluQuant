from UI.UImainWindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow
import pyqtgraph as pg  
from frontEnd.graph import CandlestickItem
from backEnd.backtest import FinMindApi

class MainWindowController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ApiHandle = FinMindApi()
        self.startDate = "1994-10-01"

        self.canvas = pg.GraphicsLayoutWidget()
        self.ui.chartLayout.addWidget(self.canvas)

        self.plotItem = self.canvas.addPlot(title="股市數據模擬")
        self.plotItem.showGrid(x=True, y=True)
        
        self.ui.UserInStartBackTest.clicked.connect(self.runBackTest)

        #預先畫好標的歷史圖表
        stockid = self.ui.UserInStockID.text()
        endDate = self.ui.UserInEndDate.text()
        stockData = self.ApiHandle.getData(stockId=stockid, startDate=self.startDate, endDate=endDate)
        self.graphPlot(stockData)
        
    def runBackTest(self):
        stockid = self.ui.UserInStockID.text()
        startDate = self.ui.UserInStartDate.text()
        endDate = self.ui.UserInEndDate.text()
        stockData = self.ApiHandle.getData(stockId=stockid, startDate=startDate, endDate=endDate)
        self.graphPlot(stockData)
        

    def graphPlot(self, stockData):
        # 將資料轉換為 (xIndex, open, close, low, high) 的格式
        
        # 創建並添加 CandlestickItem 到圖表
        candlestickItem = CandlestickItem(stockData)
        self.plotItem.addItem(candlestickItem)
        print("圖表繪製完成")