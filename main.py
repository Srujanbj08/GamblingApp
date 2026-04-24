from db.init_db import create_tables
from models.gambler import Gambler
from services.gambler_service import GamblerProfileService
from services.stake_management_service import StakeManagementService
from services.betting_service import BettingService
from services.game_session_manager import GameSessionManager
from tracking_and_reports.stake_history_report import StakeHistoryReport
from strategies.fixed_strategy import FixedStrategy


def main():
    try:
        print("=== INITIALIZING SYSTEM ===")
        create_tables()

        profile_service = GamblerProfileService()
        stake_service = StakeManagementService()
        betting_service = BettingService()
        session_manager = GameSessionManager()
        report_service = StakeHistoryReport()

        print("\n=== UC-01: GAMBLER PROFILE ===")

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

        print("Stats:", profile_service.get_gambler_stats(gambler_id))
        print("Validation:", profile_service.validate_gambler(gambler_id))

        print("\n=== UC-02: STAKE MANAGEMENT ===")

        print("Initial:", stake_service.initialize_stake(gambler_id))
        print("Loss Bet:", stake_service.place_bet(gambler_id, 100, is_win=False))
        print("Win Bet:", stake_service.place_bet(gambler_id, 200, is_win=True))

        print("Deposit:", stake_service.deposit(gambler_id, 300))
        print("Withdraw:", stake_service.withdraw(gambler_id, 150))

        print("Boundary:", stake_service.validate_boundaries(gambler_id))

        print("\n=== UC-04: SESSION MANAGEMENT ===")

        session = session_manager.start_session(gambler_id)
        print("Session Started:", session)

        print("Pausing session...")
        session_manager.pause_session(gambler_id)

        print("Resuming session...")
        session_manager.resume_session(gambler_id)

        print("Session Status:", session_manager.get_session_status(gambler_id))

        print("\n=== UC-03: BETTING ===")

        bet = betting_service.place_bet(gambler_id, 100)
        print("Bet Placed:", bet)

        result = betting_service.resolve_bet(gambler_id, bet["bet_id"], True)
        print("Bet Result:", result)

        print("\n--- Strategy Bet ---")
        strategy = FixedStrategy(50)
        bet2 = betting_service.place_bet_with_strategy(gambler_id, strategy)
        print("Strategy Bet:", bet2)

        auto_end = session_manager.auto_end_if_limits_hit(gambler_id)
        if auto_end:
            print("Auto Session End:", auto_end)

        summary = session_manager.end_session(gambler_id)
        print("Session Summary:", summary)

        print("\n=== REPORT ===")

        print("Final Stats:", profile_service.get_gambler_stats(gambler_id))
        print("Stake Report:", report_service.generate_report(gambler_id))

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()