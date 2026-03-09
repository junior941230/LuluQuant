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
        ('investPercent', 1.0),  # 設定每次投入總資金的比例，此處為 90%
        ('tradeValue', 500000)
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
        self.crossoverSignal = bt.indicators.CrossOver(
            self.fastMa, self.slowMa)

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
                actualInvestValue = min(
                    self.params.tradeValue, currentEquity * 0.95)

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
        ('tradeValue', 500000)
    )

    def __init__(self):
        self.rsi6 = bt.indicators.RSI(
            self.data.close, period=self.params.fast_period)
        self.rsi12 = bt.indicators.RSI(
            self.data.close, period=self.params.slow_period)
        self.rsi_diff = self.rsi6 - self.rsi12
        self.weakCondition = self.rsi_diff <= self.params.diff_threshold
        self.wr = bt.indicators.WilliamsR(
            self.data, period=self.params.wr_period)
        self.wrCondition = self.wr < -self.params.wr_buy_level

    def next(self):
        # 如果目前沒有持倉
        currentEquity = self.broker.getvalue()
        if not self.position:
            # 發生黃金交叉
            if self.weakCondition[0] and self.wrCondition[0]:
                # 動態下單：告訴系統目標是佔用帳戶總資金的 90%
                # 系統會自動根據當下收盤價與帳戶總資金，精準算出能買幾股並下單
                actualInvestValue = min(
                    self.params.tradeValue, currentEquity * 0.95)

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
