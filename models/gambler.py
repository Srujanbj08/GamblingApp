class Gambler:
    def __init__(self, username, full_name, email,
                 initial_stake, win_threshold,
                 loss_threshold, min_required_stake):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.initial_stake = initial_stake
        self.current_stake = initial_stake
        self.win_threshold = win_threshold
        self.loss_threshold = loss_threshold
        self.min_required_stake = min_required_stake