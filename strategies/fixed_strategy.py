from strategies.base_strategy import BaseStrategy


class FixedStrategy(BaseStrategy):

    def __init__(self, amount):
        self.amount = amount

    def calculate_bet(self, current_stake):
        return self.amount