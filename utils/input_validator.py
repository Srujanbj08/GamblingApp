from db.connection import get_connection
from utils.exceptions import (
    ValidationError,
    InsufficientBalanceError,
    InvalidAmountError,
    BoundaryViolationError,
    SessionError
)
from datetime import datetime


class InputValidator:

    def _log_event(self, gambler_id, event_type, message, level):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO validation_events
        (gambler_id, event_type, message, level, created_at)
        VALUES (%s,%s,%s,%s,%s)
        """, (gambler_id, event_type, message, level, datetime.now()))

        conn.commit()
        conn.close()

    def validate_numeric(self, value, field_name):
        if value is None:
            raise ValidationError(f"{field_name} cannot be null")

        if not isinstance(value, (int, float)):
            raise InvalidAmountError(f"{field_name} must be numeric")

        if value < 0:
            raise InvalidAmountError(f"{field_name} cannot be negative")

        return True

    def validate_bet_amount(self, gambler_id, amount):
        self.validate_numeric(amount, "Bet amount")

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT current_stake FROM gamblers WHERE gambler_id=%s
        """, (gambler_id,))

        data = cursor.fetchone()
        conn.close()

        if not data:
            raise ValidationError("Gambler not found")

        current = float(data["current_stake"])

        if amount == 0:
            raise InvalidAmountError("Bet cannot be zero")

        if amount > current:
            raise InsufficientBalanceError("Insufficient balance")

        if amount > current * 0.5:
            self._log_event(gambler_id, "BET_WARNING", "High bet amount", "WARNING")
            return {"status": "warning", "message": "High bet amount"}

        return {"status": "valid", "message": "Bet valid"}

    def validate_stake_limits(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT current_stake, win_threshold, loss_threshold 
        FROM gamblers WHERE gambler_id=%s
        """, (gambler_id,))

        data = cursor.fetchone()
        conn.close()

        if not data:
            raise ValidationError("Gambler not found")

        current = float(data["current_stake"])
        win = float(data["win_threshold"])
        loss = float(data["loss_threshold"])

        if current >= win:
            raise BoundaryViolationError("Win threshold reached")

        if current <= loss:
            raise BoundaryViolationError("Loss threshold reached")

        if current >= win * 0.8:
            self._log_event(gambler_id, "LIMIT_WARNING", "Near win threshold", "WARNING")
            return {"status": "warning", "message": "Near win limit"}

        if current <= loss * 1.2:
            self._log_event(gambler_id, "LIMIT_WARNING", "Near loss threshold", "WARNING")
            return {"status": "warning", "message": "Near loss limit"}

        return {"status": "valid", "message": "Within limits"}

    def validate_session_active(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT * FROM sessions 
        WHERE gambler_id=%s AND end_time IS NULL
        """, (gambler_id,))

        session = cursor.fetchone()
        conn.close()

        if not session:
            raise SessionError("No active session")

        return True