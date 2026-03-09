import backtrader as bt


class TradeRecorder(bt.Analyzer):
    def __init__(self):
        self.trades = []

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades.append(trade)

    def get_analysis(self):
        return self.trades


class template(bt.Strategy):
    # insertCode
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
