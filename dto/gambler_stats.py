class GamblerStatistics:

    def __init__(self, data):
        self.username = data["username"]
        self.current_stake = float(data["current_stake"])
        self.initial_stake = float(data["initial_stake"])

    def net_profit(self):
        return self.current_stake - self.initial_stake

    def win_rate_status(self, win_threshold):
        return self.current_stake >= win_threshold

    def loss_status(self, loss_threshold):
        return self.current_stake <= loss_threshold