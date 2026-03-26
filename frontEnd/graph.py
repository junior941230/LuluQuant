import pyqtgraph as pg
from PyQt6 import QtCore, QtGui
import backtrader as bt
import pandas as pd


class DateAxisItem(pg.AxisItem):
    """自定義日期軸，將數值索引轉換為日期字串顯示"""

    def __init__(self, dates, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dates = dates  # 傳入格式化後的日期清單，例如 ['2023-01-01', '2023-01-02', ...]

    def tickStrings(self, values, scale, spacing):
        """將 X 軸座標值轉換為對應的日期字串"""
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
    """K 線圖形物件，使用 QPicture 預先渲染以提升效能"""

    def __init__(self, data):
        pg.GraphicsObject.__init__(self)
        self.datas = data
        self.picture = QtGui.QPicture()
        self.generatePicture()

    def generatePicture(self):
        """將所有 K 線繪製到 QPicture 中，實現高效率批量渲染"""
        # 使用 QPainter 將所有 K 線繪製到 QPicture 中以提升渲染效能
        p = QtGui.QPainter(self.picture)
        candleWidth = 0.5

        for i, row in self.datas.iterrows():
            # 紅漲綠跌邏輯：開盤價 < 收盤價則紅色（上漲），否則綠色（下跌）
            openPrice = row['open']
            closePrice = row['close']
            lowPrice = row['min']
            highPrice = row['max']
            if openPrice * closePrice * lowPrice * highPrice == 0:
                continue  # 跳過價格為零的 K 線，避免繪製異常
            if openPrice < closePrice:
                p.setPen(pg.mkPen('r'))
                p.setBrush(pg.mkBrush('r'))
            else:
                p.setPen(pg.mkPen('g'))
                p.setBrush(pg.mkBrush('g'))

            # 1. 繪製上下影線 (高低點)
            p.drawLine(QtCore.QPointF(i + candleWidth / 2, lowPrice),
                       QtCore.QPointF(i + candleWidth / 2, highPrice))

            # 2. 繪製實體部分 (開收盤)
            # QRectF(x, y, width, height) -> 注意 height 若為負值會自動處理
            rect = QtCore.QRectF(i, openPrice, candleWidth,
                                 closePrice - openPrice)
            p.drawRect(rect)

        p.end()

    def paint(self, p, *args):
        """每一幀只需繪製這張預先渲染好的 Picture"""
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        """必須回傳圖形的邊界，PyQtGraph 才能正確處理縮放和互動"""
        return QtCore.QRectF(self.picture.boundingRect())


class StrategyItem(pg.GraphicsObject):
    """交易策略標示物件，顯示進場和出場訊號"""

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
        """繪製所有進場和出場訊號標示"""
        p = QtGui.QPainter(self.picture)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

        for trade in self.tradingHistory:
            # 取得日期字串
            dayIn = bt.num2date(trade.dtopen).strftime('%Y-%m-%d')
            dayOut = bt.num2date(trade.dtclose).strftime('%Y-%m-%d')
            # 參數設定
            price = trade.price
            signalWidth = 1.5  # 稍微放寬寬度，視覺較清楚
            signalHeight = price / 200  # 根據股價位階調整
            padding = price / 200      # 與 K 線的間距
            print(f"繪製交易訊號 - 進場: {dayIn}, 出場: {dayOut}, 價格: {price}")
            # 進場訊號繪製
            # 檢查日期是否存在於資料中，避免 KeyError
            if dayIn in self.dataFrame.index:
                targetIn = self.dataFrame.loc[dayIn]
                # 進場標示：倒三角形（指向最高價上方）
                p.setPen(pg.mkPen("#f59542"))
                p.setBrush(pg.mkBrush("#f59542"))
                topY = targetIn["max"] + padding + signalHeight
                baropen = trade.baropen
                p1 = QtCore.QPointF(baropen - signalWidth, topY)
                p2 = QtCore.QPointF(baropen, topY)
                p3 = QtCore.QPointF(baropen - signalWidth / 2,
                                    targetIn["max"] + padding)
                p.drawPolygon((p1, p2, p3))

            # 出場訊號繪製
            if dayOut in self.dataFrame.index:
                targetOut = self.dataFrame.loc[dayOut]
                # 出場標示：正三角形（指向最低價下方）
                p.setPen(pg.mkPen("#42f5e3"))
                p.setBrush(pg.mkBrush("#42f5e3"))
                bottomY = targetOut["min"] - padding - signalHeight
                barclose = trade.barclose
                p1 = QtCore.QPointF(barclose - signalWidth, bottomY)
                p2 = QtCore.QPointF(barclose, bottomY)
                p3 = QtCore.QPointF(barclose - signalWidth / 2,
                                    targetOut["min"] - padding)
                p.drawPolygon((p1, p2, p3))

        p.end()

    def paint(self, p, *args):
        """繪製預先渲染好的交易訊號"""
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        """回傳邊界矩形，防止圖形為空時發生錯誤"""
        # 如果 picture 為空，提供一個預設的最小矩形防止報錯
        rect = QtCore.QRectF(self.picture.boundingRect())
        if rect.isEmpty():
            return QtCore.QRectF(0, 0, 1, 1)
        return rect


class RsLineGraph(pg.GraphicsObject):
    """折線圖物件，用來繪製一條價格折線"""

    def __init__(self, data, xCol=None, yCol="rsRating", pen=None):
        pg.GraphicsObject.__init__(self)

        # 避免更動原始資料
        self.dataFrame = data.copy()

        self.xCol = xCol
        self.yCol = yCol
        self.pen = pen if pen is not None else pg.mkPen("#ffd166", width=2)

        self.picture = QtGui.QPicture()
        self.generatePicture()

    def generatePicture(self):
        """繪製折線圖"""
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        p.setPen(self.pen)

        # 檢查欄位是否存在
        if self.yCol not in self.dataFrame.columns:
            print(f"錯誤: yCol '{self.yCol}' 不存在於資料中")
            p.end()
            return

        if len(self.dataFrame) < 2:
            print("資料點不足，無法繪製折線圖")
            p.end()
            return

        # 決定 X 座標
        if self.xCol is not None and self.xCol in self.dataFrame.columns:
            xData = self.dataFrame[self.xCol].values
        else:
            # 沒指定 xCol 就直接用索引位置
            xData = range(len(self.dataFrame))

        yData = self.dataFrame[self.yCol].values

        # 畫折線
        for i in range(1, len(self.dataFrame)):
            x1 = float(xData[i - 1])
            y1 = float(yData[i - 1])
            x2 = float(xData[i])
            y2 = float(yData[i])

            p.drawLine(QtCore.QPointF(x1, y1), QtCore.QPointF(x2, y2))

        p.end()

    def paint(self, p, *args):
        """繪製預先渲染好的折線圖"""
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self):
        """回傳邊界矩形，防止圖形為空時發生錯誤"""
        rect = QtCore.QRectF(self.picture.boundingRect())
        if rect.isEmpty():
            return QtCore.QRectF(0, 0, 1, 1)
        return rect


def showResult(UI, stockData, traderFund, result):
    # 更改顏色
    if result['finalProfit'] > 0:
        UI.ind1.setStyleSheet("color: green")  # 最終盈虧 - 綠色
    elif result['finalProfit'] < 0:
        UI.ind1.setStyleSheet("color: red")  # 最終盈虧 - 紅色
    print(f"最大回撤: {result['moneyDrawdown']}")
    UI.ind1.setText(
        f"最終盈虧: {result['finalProfit']:.2f} ({(result['finalProfit'] / traderFund - 1) * 100:.2f}%)")

    UI.ind2.setStyleSheet("color: red")  # 最大回撤 - 紅色
    UI.ind2.setText(f"最大回撤: {result['maxDrawdown'] / 100.0:.2%}")
    UI.ind3.setText(f"交易次數: {result['totalTrades']}")
    UI.ind4.setText(
        f"勝率: {result['totalTrades'] and (result['finalProfit'] > 0) / result['totalTrades']:.2%}")
    UI.ind5.setText(
        f"獲利因子: {result['finalProfit'] / abs(result['finalProfit']) if result['finalProfit'] != 0 else 'N/A'}")
