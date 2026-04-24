from db.connection import get_connection


class WinLossStatistics:

    def generate_statistics(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT result FROM game_records 
        WHERE gambler_id=%s
        """, (gambler_id,))

        records = cursor.fetchall()

        if not records:
            return {"message": "No game records"}

        total = len(records)
        wins = sum(1 for r in records if r["result"] == "WIN")
        losses = total - wins

        win_ratio = wins / total if total > 0 else 0

        cursor.execute("""
        SELECT SUM(bet_amount) as total_bet, 
               SUM(win_amount) as total_win
        FROM bets WHERE gambler_id=%s
        """, (gambler_id,))

        bet_data = cursor.fetchone()

        total_bet = float(bet_data["total_bet"] or 0)
        total_win = float(bet_data["total_win"] or 0)

        roi = (total_win - total_bet) / total_bet if total_bet > 0 else 0
        profit_factor = (total_win / total_bet) if total_bet > 0 else 0

        return {
            "total_games": total,
            "wins": wins,
            "losses": losses,
            "win_ratio": round(win_ratio, 2),
            "roi": round(roi, 2),
            "profit_factor": round(profit_factor, 2)
        }