import backtrader as bt

class TradeRecorder(bt.Analyzer):
    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades.append(trade)

    def get_analysis(self):
        return self.trades

class MaCross(bt.Strategy):
    # 設定策略參數
    params = (
        ('fastPeriod', 5),
        ('slowPeriod', 20),
        ('investPercent', 1.0), # 設定每次投入總資金的比例，此處為 90%
        ('tradeValue',500000)
    )

    def __init__(self):
        # __init__ 階段負責定義指標，這裡只宣告，不進行買賣判斷
        self.fastMa = bt.indicators.SMA(
            self.data.close, period=self.params.fastPeriod
        )
        self.slowMa = bt.indicators.SMA(
            self.data.close, period=self.params.slowPeriod
        )
        
        # 內建的交叉指標：1 代表上穿(黃金交叉)，-1 代表下穿(死亡交叉)
        self.crossoverSignal = bt.indicators.CrossOver(self.fastMa, self.slowMa)

    def next(self):
        # next 階段是核心，系統會逐根 K 線執行這裡的邏輯
        
        # 實話實說：這裡你隨時可以印出 currentEquity 來觀察資金的動態變化
        currentEquity = self.broker.getvalue()

        # 如果目前沒有持倉
        if not self.position:
            # 發生黃金交叉
            if self.crossoverSignal > 0:
                # 動態下單：告訴系統目標是佔用帳戶總資金的 90%
                # 系統會自動根據當下收盤價與帳戶總資金，精準算出能買幾股並下單
                actualInvestValue = min(self.params.tradeValue, currentEquity * 0.95)
            
                # 直接讓系統根據安全金額換算股數下單
                self.order_target_value(target=actualInvestValue)
                
        # 如果目前有持倉
        else:
            # 發生死亡交叉
            if self.crossoverSignal < 0:
                # 平倉所有部位
                self.close()

    def notify_order(self, order):
        # 如果訂單狀態是已提交或已被券商接受，不需處理
        if order.status in [order.Submitted, order.Accepted]:
            return

        # # 如果訂單狀態是完成
        # if order.status in [order.Completed]:
        #     if order.isbuy():
        #         print(f"買單執行: 價格 {order.executed.price}, 成本 {order.executed.value}, 手續費 {order.executed.comm}")
        #     elif order.issell():
        #         print(f"賣單執行: 價格 {order.executed.price}, 成本 {order.executed.value}, 手續費 {order.executed.comm}")

        # 如果訂單被拒絕、取消或保證金不足 (這就是你遇到的狀況)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print("警告：訂單被拒絕或資金不足！")


class RSI_WR_AND(bt.Strategy):
    params = (
        ('fast_period', 6),
        ('slow_period', 12),
        ('diff_threshold', -12),
        ('sell_rsi_level', 80),
        ('wr_period', 14),
        ('wr_buy_level', 80),
        ('tradeValue',500000)
    )

    def __init__(self):
        self.rsi6 = bt.indicators.RSI(self.data.close, period=self.params.fast_period)
        self.rsi12 = bt.indicators.RSI(self.data.close, period=self.params.slow_period)
        self.rsi_diff = self.rsi6 - self.rsi12
        self.weakCondition = self.rsi_diff <= self.params.diff_threshold
        self.wr = bt.indicators.WilliamsR(self.data, period=self.params.wr_period)
        self.wrCondition = self.wr < -self.params.wr_buy_level

    def next(self):
        # 如果目前沒有持倉
        currentEquity = self.broker.getvalue()
        if not self.position:
            # 發生黃金交叉
            if self.weakCondition[0] and self.wrCondition[0]:
                # 動態下單：告訴系統目標是佔用帳戶總資金的 90%
                # 系統會自動根據當下收盤價與帳戶總資金，精準算出能買幾股並下單
                actualInvestValue = min(self.params.tradeValue, currentEquity * 0.95)
            
                # 直接讓系統根據安全金額換算股數下單
                self.order_target_value(target=actualInvestValue)
                
        # 如果目前有持倉
        else:
            if self.rsi6 >= self.params.sell_rsi_level or self.rsi6 < self.rsi12:
                self.close()

    def notify_order(self, order):
        # 如果訂單狀態是已提交或已被券商接受，不需處理
        if order.status in [order.Submitted, order.Accepted]:
            return

        # # 如果訂單狀態是完成
        # if order.status in [order.Completed]:
        #     if order.isbuy():
        #         print(f"買單執行: 價格 {order.executed.price}, 成本 {order.executed.value}, 手續費 {order.executed.comm} ,日期 {self.data.datetime.date(0)}")
        #     elif order.issell():
        #         print(f"賣單執行: 價格 {order.executed.price}, 成本 {order.executed.value}, 手續費 {order.executed.comm} ,日期 {self.data.datetime.date(0)}")

        # 如果訂單被拒絕、取消或保證金不足 (這就是你遇到的狀況)
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print("警告：訂單被拒絕或資金不足！")
class GapStrategy(bt.Strategy):
    params = (
        ('tradeValue', 500000),
    )

    def __init__(self):
        # 今天開盤 > 昨天收盤 → 買進條件
        self.buyCondition = self.data.open > self.data.close(-1)

        # 今天開盤 < 昨天收盤 → 賣出條件
        self.sellCondition = self.data.open < self.data.close(-1)

    def next(self):
        # 目前帳戶總資產
        currentEquity = self.broker.getvalue()

        # 如果目前沒有持倉
        if not self.position:
            if self.buyCondition[0]:
                # 實際投入金額 = tradeValue 與 資產95% 取較小者
                actualInvestValue = min(self.params.tradeValue, currentEquity * 0.95)

                # 根據目標金額自動換算股數下單
                self.order_target_value(target=actualInvestValue)

        # 如果目前有持倉
        else:
            if self.sellCondition[0]:
                self.close()

    def notify_order(self, order):
        # 如果訂單只是送出或被接受，先不處理
        if order.status in [order.Submitted, order.Accepted]:
            return

        # 如果訂單成交
        if order.status in [order.Completed]:
            if order.isbuy():
                print(
                    f"買單執行: 價格 {order.executed.price}, "
                    f"成本 {order.executed.value}, "
                    f"手續費 {order.executed.comm}, "
                    f"日期 {self.data.datetime.date(0)}"
                )
            elif order.issell():
                print(
                    f"賣單執行: 價格 {order.executed.price}, "
                    f"成本 {order.executed.value}, "
                    f"手續費 {order.executed.comm}, "
                    f"日期 {self.data.datetime.date(0)}"
                )

        # 如果訂單被取消、拒絕、或資金不足
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"警告：訂單被拒絕、取消或資金不足！日期 {self.data.datetime.date(0)}")
import backtrader as bt

class BB_TrailingStop(bt.Strategy):
    params = (
        ('period', 20),      # 布林通道週期
        ('devfactor', 2.0),  # 標準差倍數
        ('tradeValue', 500000),
    )

    def __init__(self):
        # 初始化布林通道指標
        self.bb = bt.indicators.BollingerBands(self.data.close, 
                                                period=self.params.period, 
                                                devfactor=self.params.devfactor)
        # 用來記錄當前的動態止損價
        self.stop_price = None

    def next(self):
        currentEquity = self.broker.getvalue()
        
        # 1. 如果目前沒有持倉：找尋進場點
        if not self.position:
            # 進場邏輯範例：收盤價突破布林上軌（強勢突破）
            if self.data.close[0] > self.bb.lines.top[0]:
                actualInvestValue = min(self.params.tradeValue, currentEquity * 0.95)
                self.order_target_value(target=actualInvestValue)
                # 進場時，初步止損可以設在下軌或前低，這裡我們先設為 None 等待站上中軌
                self.stop_price = None
        
        # 2. 如果目前有持倉：執行移動止損邏輯
        else:
            # 依照你的需求：如果站上 BB 中軌，就將該處設為止損點
            # 我們取「當前中軌值」與「過去已紀錄止損價」的最大值，確保止損點只會上移不會下移
            current_mid = self.bb.lines.mid[0]
            
            if self.data.close[0] > current_mid:
                if self.stop_price is None:
                    self.stop_price = current_mid
                else:
                    self.stop_price = max(self.stop_price, current_mid)

            # 出場判斷：如果止損點已建立，且收盤價跌破止損點
            if self.stop_price is not None and self.data.close[0] < self.stop_price:
                self.close()
                self.stop_price = None # 出場後重置止損價

    def notify_order(self, order):
        # 沿用你原本的通知邏輯
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            verb = "買進" if order.isbuy() else "賣出"
            print(f"{verb}執行: 價格 {order.executed.price}, 日期 {self.data.datetime.date(0)}")
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            print(f"警告：訂單失敗！日期 {self.data.datetime.date(0)}")