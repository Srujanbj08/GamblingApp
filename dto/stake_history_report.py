from db.connection import get_connection


class StakeHistoryReport:

    def generate_report(self, gambler_id):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
        SELECT transaction_type, amount, balance_after, created_at
        FROM stake_transactions
        WHERE gambler_id=%s
        ORDER BY created_at
        """, (gambler_id,))

        transactions = cursor.fetchall()
        conn.close()

        if not transactions:
            return {"message": "No transactions found"}

        total_transactions = len(transactions)

        net = 0
        peak = float(transactions[0]["balance_after"])
        lowest = peak

        for t in transactions:
            amt = float(t["amount"])
            bal = float(t["balance_after"])

            net += amt
            peak = max(peak, bal)
            lowest = min(lowest, bal)

        return {
            "total_transactions": total_transactions,
            "net_movement": net,
            "peak_balance": peak,
            "lowest_balance": lowest,
            "transactions": transactions
        }