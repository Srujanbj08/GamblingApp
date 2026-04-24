from db.connection import get_connection
from datetime import datetime
from services.stake_management_service import StakeManagementService


class BettingService:

    def __init__(self):
        self.stake_service = StakeManagementService()

    def _get_balance(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT current_stake FROM gamblers WHERE gambler_id=%s
        """, (gambler_id,))

        data = cursor.fetchone()
        conn.close()

        if not data:
            raise ValueError("Gambler not found")

        return float(data["current_stake"])

    def place_bet(self, gambler_id, bet_amount):
        current = self._get_balance(gambler_id)

        if bet_amount <= 0:
            raise ValueError("Invalid bet amount")

        if bet_amount > current:
            raise ValueError("Insufficient balance")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bets (gambler_id, bet_amount, outcome, win_amount, created_at)
        VALUES (%s,%s,%s,%s,%s)
        """, (gambler_id, bet_amount, "PENDING", 0, datetime.now()))

        conn.commit()
        bet_id = cursor.lastrowid
        conn.close()

        return {
            "bet_id": bet_id,
            "bet_amount": bet_amount,
            "status": "PLACED"
        }

    def resolve_bet(self, gambler_id, bet_id, is_win):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT bet_amount FROM bets WHERE bet_id=%s", (bet_id,))
        bet = cursor.fetchone()

        if not bet:
            conn.close()
            raise ValueError("Bet not found")

        amount = float(bet["bet_amount"])

        if is_win:
            win_amount = amount * 2
            outcome = "WIN"
            new_balance = self.stake_service.place_bet(gambler_id, amount, is_win=True)
        else:
            win_amount = 0
            outcome = "LOSS"
            new_balance = self.stake_service.place_bet(gambler_id, amount, is_win=False)

        cursor = conn.cursor()

        cursor.execute("""
        UPDATE bets 
        SET outcome=%s, win_amount=%s 
        WHERE bet_id=%s
        """, (outcome, win_amount, bet_id))

        cursor.execute("""
        INSERT INTO game_records (gambler_id, bet_id, result, created_at)
        VALUES (%s,%s,%s,%s)
        """, (gambler_id, bet_id, outcome, datetime.now()))

        conn.commit()
        conn.close()

        return {
            "bet_id": bet_id,
            "result": outcome,
            "win_amount": win_amount,
            "new_balance": new_balance
        }

    def place_bet_with_strategy(self, gambler_id, strategy, last_result=None):
        current = self._get_balance(gambler_id)

        try:
            bet_amount = strategy.calculate_bet(current, last_result)
        except TypeError:
            bet_amount = strategy.calculate_bet(current)

        return self.place_bet(gambler_id, bet_amount)