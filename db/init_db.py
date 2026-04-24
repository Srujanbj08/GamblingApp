import mysql.connector
from config.settings import DB_CONFIG


def create_tables():
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stake_transactions (
        transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        amount DECIMAL(10,2),
        transaction_type VARCHAR(50),
        balance_after DECIMAL(10,2),
        created_at DATETIME,
        FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        session_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        start_time DATETIME,
        end_time DATETIME,
        FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS running_totals_snapshots (
        snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        current_stake DECIMAL(10,2),
        peak_stake DECIMAL(10,2),
        lowest_stake DECIMAL(10,2),
        created_at DATETIME
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bets (
        bet_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        bet_amount DECIMAL(10,2),
        outcome VARCHAR(10),
        win_amount DECIMAL(10,2),
        created_at DATETIME,
        FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS betting_strategies (
        strategy_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        strategy_name VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS game_records (
        record_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        bet_id BIGINT,
        result VARCHAR(20),
        created_at DATETIME,
        FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id),
        FOREIGN KEY (bet_id) REFERENCES bets(bet_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pause_records (
        pause_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        pause_start DATETIME,
        pause_end DATETIME
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS session_parameters (
        param_id BIGINT AUTO_INCREMENT PRIMARY KEY,
        gambler_id BIGINT,
        max_duration INT,
        auto_stop BOOLEAN
    )
    """)
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS validation_events (
    event_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gambler_id BIGINT,
    event_type VARCHAR(50),
    message TEXT,
    level VARCHAR(10),
    created_at DATETIME
)

    conn.commit()
  """)   conn.close()

    print("Database & all tables (UC1–UC4) ready")