from db.init_db import create_tables
from models.gambler import Gambler
from services.gambler_service import GamblerProfileService
from services.stake_management_service import StakeManagementService
from dto.stake_history_report import StakeHistoryReport
from services.betting_service import BettingService
from strategies.fixed_strategy import FixedStrategy

def main():
    try:
        print("Initializing Database...")
        create_tables()

        profile_service = GamblerProfileService()
        stake_service = StakeManagementService()
        report_service = StakeHistoryReport()

        print("\n--- Creating Gambler (UC-01) ---")
        gambler = Gambler(
            username="player2",
            full_name="Srujan",
            email="test@mail.com",
            initial_stake=1000,
            win_threshold=1500,
            loss_threshold=500,
            min_required_stake=200
        )

        profile_service.create_gambler(gambler)

        gambler_id = 1

        print("\n--- Gambler Stats ---")
        print(profile_service.get_gambler_stats(gambler_id))

        print("\n--- Validate Gambler ---")
        print(profile_service.validate_gambler(gambler_id))

        print("\n--- Initialize Stake (UC-02) ---")
        print("Initial Balance:", stake_service.initialize_stake(gambler_id))

        print("\n--- Place Bet (Loss) ---")
        print("Balance:", stake_service.place_bet(gambler_id, 100, is_win=False))

        print("\n--- Place Bet (Win) ---")
        print("Balance:", stake_service.place_bet(gambler_id, 200, is_win=True))

        print("\n--- Deposit ---")
        print("Balance:", stake_service.deposit(gambler_id, 300))

        print("\n--- Withdraw ---")
        print("Balance:", stake_service.withdraw(gambler_id, 150))

        print("\n--- Boundary Validation ---")
        print(stake_service.validate_boundaries(gambler_id))

        print("\n--- Final Stats ---")
        print(profile_service.get_gambler_stats(gambler_id))

        print("\n--- Stake Report ---")
        report = report_service.generate_report(gambler_id)
        print(report)

    except Exception as e:
        print("Error:", e)
        

betting_service = BettingService()

print("\n--- Place Bet ---")
bet = betting_service.place_bet(gambler_id, 100)
print(bet)

print("\n--- Resolve Bet (Win) ---")
result = betting_service.resolve_bet(gambler_id, bet["bet_id"], True)
print(result)

print("\n--- Strategy Bet ---")
strategy = FixedStrategy(50)
bet2 = betting_service.place_bet_with_strategy(gambler_id, strategy)
print(bet2)


if __name__ == "__main__":
    main()