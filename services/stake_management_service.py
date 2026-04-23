from db.connection import get_connection
from datetime import datetime


class StakeManagementService:

    def _get_gambler(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT current_stake, win_threshold, loss_threshold 
        FROM gamblers WHERE gambler_id=%s
        """, (gambler_id,))

        data = cursor.fetchone()
        conn.close()

        if not data:
            raise ValueError("Gambler not found")

        return data

    def _log_transaction(self, gambler_id, amount, t_type, balance):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO stake_transactions
        (gambler_id, amount, transaction_type, balance_after, created_at)
        VALUES (%s,%s,%s,%s,%s)
        """, (gambler_id, amount, t_type, balance, datetime.now()))

        conn.commit()
        conn.close()

    def initialize_stake(self, gambler_id):
        data = self._get_gambler(gambler_id)
        current = float(data["current_stake"])

        self._log_transaction(gambler_id, current, "INITIAL_STAKE", current)

        return current

    def place_bet(self, gambler_id, amount, is_win=False):
        data = self._get_gambler(gambler_id)
        current = float(data["current_stake"])

        if amount > current:
            raise ValueError("Insufficient balance")

        if is_win:
            new_balance = current + amount
            t_type = "BET_WIN"
        else:
            new_balance = current - amount
            t_type = "BET_LOSS"

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s
        """, (new_balance, gambler_id))

        conn.commit()
        conn.close()

        self._log_transaction(gambler_id, amount, t_type, new_balance)

        return new_balance

    def deposit(self, gambler_id, amount):
        data = self._get_gambler(gambler_id)
        current = float(data["current_stake"])

        new_balance = current + amount

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s
        """, (new_balance, gambler_id))

        conn.commit()
        conn.close()

        self._log_transaction(gambler_id, amount, "DEPOSIT", new_balance)

        return new_balance

    def withdraw(self, gambler_id, amount):
        data = self._get_gambler(gambler_id)
        current = float(data["current_stake"])

        if amount > current:
            raise ValueError("Insufficient balance")

        new_balance = current - amount

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE gamblers SET current_stake=%s WHERE gambler_id=%s
        """, (new_balance, gambler_id))

        conn.commit()
        conn.close()

        self._log_transaction(gambler_id, amount, "WITHDRAWAL", new_balance)

        return new_balance

    def validate_boundaries(self, gambler_id):
        data = self._get_gambler(gambler_id)

        current = float(data["current_stake"])
        win = float(data["win_threshold"])
        loss = float(data["loss_threshold"])

        if current >= win:
            return False, "Win threshold reached"

        if current <= loss:
            return False, "Loss threshold reached"

        if current <= loss * 1.2:
            return True, "Warning: Near minimum limit"

        if current >= win * 0.8:
            return True, "Warning: Near maximum limit"

        return True, "Within safe limits"

    def get_balance(self, gambler_id):
        data = self._get_gambler(gambler_id)
        return float(data["current_stake"])