# Gambling App

Gambling App is a modular backend application that simulates strategic gambling sessions with stake tracking, betting strategies, session management, and analytical reporting. The project is designed using service-oriented architecture and demonstrates concepts such as validation handling, transaction management, probability-based betting, and real-time session monitoring. 

---

## Features

* Gambler profile and session management
* Manual and strategy-based betting
* Stake tracking and transaction history
* Win/loss analytics and streak calculation
* Boundary validation for stake limits
* Probability-based outcome simulation
* Interactive terminal-based workflow
* Validation and error handling system

---

## Modules

* **Profile Management** – Create, update, validate, and reset gambler profiles
* **Stake Management** – Track balances, stake history, and thresholds
* **Betting Mechanism** – Support multiple betting strategies
* **Session Management** – Start, pause, resume, and end sessions
* **Win/Loss Calculation** – Generate statistics and performance metrics
* **Validation System** – Input validation and exception handling
* **User Interaction** – Interactive menus and status displays

---

## Tech Stack

* Python
* MySQL
* Redis
* Celery
* Rich
* Object-Oriented Programming

---

## Setup

Install dependencies:

```bash id="zkqu4f"
pip install -r requirements.txt
```

Run the application:

```bash id="mte6fa"
python main.py
```

Start Celery worker:

```bash id="n8z53n"
celery -A tasks worker --loglevel=info
```

---

## Project Structure

```bash id="o4j1pk"
GamblingApp/
│
├── config/
├── models/
├── services/
├── strategies/
├── tracking_and_reports/
├── ui/
├── utils/
├── tasks/
└── main.py
```

---

## Key Capabilities

* Automated and manual betting workflows
* Stake lifecycle tracking
* Session-based gameplay analytics
* Multiple betting strategy implementations
* Real-time validation and monitoring
* Detailed reporting and statistics generation


