from datetime import datetime


class SessionStatus:
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    ENDED = "ENDED"


class SessionEndReason:
    MANUAL = "MANUAL"
    WIN_THRESHOLD = "WIN_THRESHOLD"
    LOSS_THRESHOLD = "LOSS_THRESHOLD"


class GameSession:

    def __init__(self, gambler_id):
        self.gambler_id = gambler_id
        self.start_time = datetime.now()
        self.end_time = None
        self.status = SessionStatus.ACTIVE
        self.pause_start = None
        self.total_paused_duration = 0

    def pause(self):
        if self.status != SessionStatus.ACTIVE:
            raise ValueError("Session not active")

        self.pause_start = datetime.now()
        self.status = SessionStatus.PAUSED

    def resume(self):
        if self.status != SessionStatus.PAUSED:
            raise ValueError("Session not paused")

        paused_time = (datetime.now() - self.pause_start).total_seconds()
        self.total_paused_duration += paused_time

        self.pause_start = None
        self.status = SessionStatus.ACTIVE

    def end(self):
        self.end_time = datetime.now()
        self.status = SessionStatus.ENDED

    def get_active_duration(self):
        if not self.end_time:
            return 0

        total = (self.end_time - self.start_time).total_seconds()
        return total - self.total_paused_duration