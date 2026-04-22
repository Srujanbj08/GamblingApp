from db.connection import get_connection
from dto.gambler_stats import GamblerStatistics
from datetime import datetime


class GamblerProfileService:

    
    def create_gambler(self, gambler):
        if gambler.initial_stake < gambler.min_required_stake:
            raise ValueError("Initial stake below minimum required")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO gamblers 
        (username, full_name, email, is_active, initial_stake,
         current_stake, win_threshold, loss_threshold,
         min_required_stake, created_at, updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            gambler.username,
            gambler.full_name,
            gambler.email,
            True,
            gambler.initial_stake,
            gambler.current_stake,
            gambler.win_threshold,
            gambler.loss_threshold,
            gambler.min_required_stake,
            datetime.now(),
            datetime.now()
        ))

        conn.commit()
        conn.close()
        print("Gambler created")

    
    def update_gambler(self, gambler_id, field, value):
        conn = get_connection()
        cursor = conn.cursor()

        query = f"UPDATE gamblers SET {field}=%s, updated_at=%s WHERE gambler_id=%s"
        cursor.execute(query, (value, datetime.now(), gambler_id))

        conn.commit()
        conn.close()
        print("Updated")

    
    def get_gambler_stats(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        data = cursor.fetchone()
        conn.close()

        if not data:
            raise ValueError("Not found")

        stats = GamblerStatistics(data)

        return {
            "username": stats.username,
            "current_stake": stats.current_stake,
            "net_profit": stats.net_profit()
        }

    
    def validate_gambler(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        g = cursor.fetchone()
        conn.close()

        if not g:
            return False, "Not found"

        if not g["is_active"]:
            return False, "Inactive"

        if g["current_stake"] < g["min_required_stake"]:
            return False, "Low balance"

        if g["current_stake"] >= g["win_threshold"]:
            return False, "Win target reached"

        if g["current_stake"] <= g["loss_threshold"]:
            return False, "Loss limit reached"

        return True, "Eligible"

   
    def reset_gambler(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM gamblers WHERE gambler_id=%s", (gambler_id,))
        g = cursor.fetchone()

        if not g:
            raise ValueError("Not found")

        initial = float(g["initial_stake"])

        new_win = initial * 1.5
        new_loss = initial * 0.5

        cursor.execute("""
        UPDATE gamblers 
        SET current_stake=%s, win_threshold=%s, loss_threshold=%s, updated_at=%s
        WHERE gambler_id=%s
        """, (initial, new_win, new_loss, datetime.now(), gambler_id))

        conn.commit()
        conn.close()

        print("Reset successful")