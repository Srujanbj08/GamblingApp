import mysql.connector
from config.settings import DB_CONFIG


def create_tables():
    # connect WITHOUT database first
    temp_config = DB_CONFIG.copy()
    temp_config.pop("database")

    conn = mysql.connector.connect(**temp_config)
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
    conn.close()

    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gamblers (
        gambler_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(100) UNIQUE,
        full_name VARCHAR(150),
        email VARCHAR(150) UNIQUE,
        is_active BOOLEAN,
        initial_stake DECIMAL(10,2),
        current_stake DECIMAL(10,2),
        win_threshold DECIMAL(10,2),
        loss_threshold DECIMAL(10,2),
        min_required_stake DECIMAL(10,2),
        created_at DATETIME,
        updated_at DATETIME
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS betting_preferences (
        preference_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT UNIQUE,
        min_bet DECIMAL(10,2),
        max_bet DECIMAL(10,2),
        preferred_game_type VARCHAR(50),
        auto_play_enabled BOOLEAN,
        auto_play_max_games INT,
        session_loss_limit DECIMAL(10,2),
        session_win_target DECIMAL(10,2),
        updated_at DATETIME,
        FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database & tables ready")