import pyqtgraph as pg
from PySide6 import QtCore, QtGui
import backtrader as bt 
import pandas as pd

class DateAxisItem(pg.AxisItem):
    def __init__(self, dates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates = dates  # 傳入格式化後的日期清單，例如 ['2023-01-01', '2023-01-02', ...]

    def tickStrings(self, values, scale, spacing):
        # values 是 pyqtgraph 傳入目前畫面可見的 X 軸座標值
        result = []
        for v in values:
            idx = int(v)
            if 0 <= idx < len(self.dates):
                result.append(self.dates[idx])
            else:
                result.append("")
        return result
class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.datas = data  
        self.picture = QtGui.QPicture()
        self.generatePicture()

    def generatePicture(self):
        # 使用 QPainter 將所有 K 線繪製到 QPicture 中以提升渲染效能
        p = QtGui.QPainter(self.picture)
        candleWidth = 0.5
        
        for i, row in self.datas.iterrows():
            # 紅漲綠跌邏輯
            openPrice = row['open']
            closePrice = row['close']
            lowPrice = row['min']
            highPrice = row['max']
            if openPrice < closePrice:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))
            
            # 1. 繪製上下影線 (高低點)
            p.drawLine(QtCore.QPointF(i, lowPrice), QtCore.QPointF(i, highPrice))
            
            # 2. 繪製實體部分 (開收盤)
            # QRectF(x, y, width, height) -> 注意 height 若為負值會自動處理
            rect = QtCore.QRectF(i - candleWidth / 2, openPrice, candleWidth, closePrice - openPrice)
            p.drawRect(rect)
            
        p.end()

    def paint(self, p, *args):
        # 每一幀只需繪製這張預先渲染好的 Picture
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        # 必須回傳圖形的邊界，PyQtGraph 才能正確處理縮放
        return QtCore.QRectF(self.picture.boundingRect())
    
class StrategyItem(pg.GraphicsObject):
    def __init__(self, data, tradingHistory):
        pg.GraphicsObject.__init__(self)
        # 避免更動原始 data，使用 copy
        self.dataFrame = data.copy()
        self.dataFrame['date'] = pd.to_datetime(self.dataFrame['date'])
        self.dataFrame.set_index('date', inplace=True)
        
        self.tradingHistory = tradingHistory
        self.picture = QtGui.QPicture()
        self.generatePicture()

    def generatePicture(self):
        p = QtGui.QPainter(self.picture)
    
        p.setRenderHint(QtGui.QPainter.Antialiasing)

        for trade in self.tradingHistory:
            # 取得日期字串
            dayIn = bt.num2date(trade.dtopen).strftime('%Y-%m-%d')
            dayOut = bt.num2date(trade.dtclose).strftime('%Y-%m-%d')
            # 參數設定
            price = trade.price
            signalWidth = 0.5  # 稍微放寬寬度，視覺較清楚
            signalHeight = price/200 # 根據股價位階調整
            padding = price/200      # 與 K 線的間距
            # 檢查日期是否存在於資料中，避免 KeyError
            if dayIn in self.dataFrame.index:
                targetIn = self.dataFrame.loc[dayIn]
                # 進場標示：倒三角形（指向最高價上方）
                p.setPen(pg.mkPen("#f59542"))
                p.setBrush(pg.mkBrush("#f59542"))
                topY = targetIn["max"] + padding + signalHeight
                p1 = QtCore.QPointF(trade.baropen - signalWidth, topY)
                p2 = QtCore.QPointF(trade.baropen + signalWidth, topY)
                p3 = QtCore.QPointF(trade.baropen, targetIn["max"] + padding)
                p.drawPolygon((p1, p2, p3))

            if dayOut in self.dataFrame.index:
                targetOut = self.dataFrame.loc[dayOut]
                # 出場標示：正三角形（指向最低價下方）
                p.setPen(pg.mkPen("#42f5e3"))
                p.setBrush(pg.mkBrush("#42f5e3"))
                bottomY = targetOut["min"] - padding - signalHeight
                p1 = QtCore.QPointF(trade.barclose - signalWidth, bottomY)
                p2 = QtCore.QPointF(trade.barclose + signalWidth, bottomY)
                p3 = QtCore.QPointF(trade.barclose, targetOut["min"] - padding)
                p.drawPolygon((p1, p2, p3))
            
        p.end()

    def paint(self, p, *args):
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        # 如果 picture 為空，提供一個預設的最小矩形防止報錯
        rect = QtCore.QRectF(self.picture.boundingRect())
        if rect.isEmpty():
            return QtCore.QRectF(0, 0, 1, 1)
        return rect