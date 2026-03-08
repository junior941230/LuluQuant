import pyqtgraph as pg
from PySide6 import QtCore, QtGui

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
    
class stragegyItem(pg.GraphicsObject):
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