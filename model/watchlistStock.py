class WatchlistStock():
    def __init__(self, stock_ticker, stock_name, current_value, percentage_from_52week_high, note):
        self.stock_ticker = stock_ticker
        self.stock_name = stock_name
        self.current_value = current_value
        self.percentage_from_52week_high = percentage_from_52week_high
        self.note = note