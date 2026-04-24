from services.gambler_service import GamblerProfileService
from services.stake_management_service import StakeManagementService
from services.betting_service import BettingService
from services.game_session_manager import GameSessionManager
from services.win_loss_calculator import WinLossCalculator

from tracking_and_reports.stake_history_report import StakeHistoryReport
from tracking_and_reports.win_loss_statistics import WinLossStatistics

from utils.input_validator import InputValidator
from ui.game_status_display import GameStatusDisplay
from ui.session_summary import SessionSummary


class InteractiveMenu:

    def __init__(self):
        self.profile = GamblerProfileService()
        self.stake = StakeManagementService()
        self.betting = BettingService()
        self.session = GameSessionManager()
        self.validator = InputValidator()
        self.calc = WinLossCalculator()

        self.report = StakeHistoryReport()
        self.stats = WinLossStatistics()

        self.display = GameStatusDisplay()
        self.summary = SessionSummary()

    def start(self, gambler_id):
        self.session.start_session(gambler_id)

        while True:
            print("\n==== MENU ====")
            print("1. Show Balance")
            print("2. Place Bet")
            print("3. Deposit")
            print("4. Withdraw")
            print("5. Session Status")
            print("6. End Session")
            print("7. Exit")

            choice = input("Enter choice: ")

            try:
                if choice == "1":
                    balance = self.stake.get_balance(gambler_id)
                    self.display.show_balance(balance)

                elif choice == "2":
                    amt = float(input("Enter bet amount: "))

                    validation = self.validator.validate_bet_amount(gambler_id, amt)
                    self.display.show_validation(validation)

                    bet = self.betting.place_bet(gambler_id, amt)

                    result_input = input("Win or Loss? (w/l): ").lower()
                    is_win = result_input == "w"

                    result = self.betting.resolve_bet(gambler_id, bet["bet_id"], is_win)
                    self.display.show_bet_result(result)

                    self.calc.update_running_totals(gambler_id)

                    auto = self.session.auto_end_if_limits_hit(gambler_id)
                    if auto:
                        self.display.show_message("Session auto-ended")
                        break

                elif choice == "3":
                    amt = float(input("Enter deposit amount: "))
                    self.validator.validate_numeric(amt, "Deposit")
                    balance = self.stake.deposit(gambler_id, amt)
                    self.display.show_balance(balance)

                elif choice == "4":
                    amt = float(input("Enter withdraw amount: "))
                    self.validator.validate_numeric(amt, "Withdraw")
                    balance = self.stake.withdraw(gambler_id, amt)
                    self.display.show_balance(balance)

                elif choice == "5":
                    status = self.session.get_session_status(gambler_id)
                    self.display.show_message(status)

                elif choice == "6":
                    break

                elif choice == "7":
                    print("Exiting...")
                    return

                else:
                    print("Invalid choice")

            except Exception as e:
                self.display.show_error(e)

        session_summary = self.session.end_session(gambler_id)
        stats = self.stats.generate_statistics(gambler_id)
        stake_report = self.report.generate_report(gambler_id)

        self.summary.display(session_summary, stats, stake_report)