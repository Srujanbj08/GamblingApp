from db.init_db import create_tables
from models.gambler import Gambler
from services.gambler_service import GamblerProfileService


def start_app():
    create_tables()

    service = GamblerProfileService()

    g = Gambler(
        username="player1",
        full_name="Srujan",
        email="test@mail.com",
        initial_stake=1000,
        win_threshold=1500,
        loss_threshold=500,
        min_required_stake=200
    )

    service.create_gambler(g)

    print(service.get_gambler_stats(1))
    print(service.validate_gambler(1))

    service.update_gambler(1, "full_name", "Updated User")
    service.reset_gambler(1)


if __name__ == "__main__":
    start_app()