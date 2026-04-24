class GameStatusDisplay:

    def show_balance(self, balance):
        print(f"\nCurrent Balance: {balance}")

    def show_message(self, message):
        print(f"\n{message}")

    def show_bet_result(self, result):
        print("\n--- Bet Result ---")
        print(f"Bet ID: {result['bet_id']}")
        print(f"Outcome: {result['result']}")
        print(f"Win Amount: {result['win_amount']}")
        print(f"New Balance: {result['new_balance']}")

    def show_validation(self, validation):
        print("\nValidation:", validation)

    def show_error(self, error):
        print(f"\nError: {error}")