from strategies.base_strategy import BaseStrategy


class MartingaleStrategy(BaseStrategy):

    def __init__(self, base_amount):
        self.base_amount = base_amount
        self.last_bet = base_amount

    def calculate_bet(self, current_stake, last_result=None):
        if last_result == "LOSS":
            self.last_bet *= 2
        else:
            self.last_bet = self.base_amount

        return self.last_bet