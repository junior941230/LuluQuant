from FinMind.data import DataLoader

api = DataLoader()
api.taiwan_stock_daily_adj(
    stock_id="2330",
    start_date="2022-01-01",
    end_date="2022-12-31"
)
