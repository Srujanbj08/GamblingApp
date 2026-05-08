# Gambling App

Gambling App is a modular Python application designed for gambling session management, betting simulation, stake tracking, and analytical reporting. The project follows a service-oriented and feature-based architecture, where each branch represents a separate functional module of the system.

The application demonstrates concepts such as probability-based betting, session lifecycle management, validation handling, betting strategies, and real-time stake monitoring.

---

## Features

* Gambler profile management
* Betting and stake management
* Session lifecycle tracking
* Probability-based win/loss calculation
* Validation and exception handling
* Interactive terminal-based workflow
* Multiple betting strategy support
* Detailed session analytics and reporting

---

## Branch Structure

```bash id="p9c8ak"
main
├── BettingMechanism
├── GameSessionManagement
├── InputValidationandErrorHandling
├── StakeManagementOperations
├── UserInteraction
├── WinLossCalculation
├── dev
└── feature/GamblerProfileManagement
```

Each branch focuses on a specific module of the application for modular development and easier collaboration.

---

## Tech Stack

* Python
* MySQL
* Redis
* Celery
* Rich

---

## Setup

Install dependencies:

```bash id="6qozij"
pip install -r requirements.txt
```

Run the application:

```bash id="z67nsr"
python main.py
```

Start Celery worker:

```bash id="r4smy7"
celery -A tasks worker --loglevel=info
```

---

## Modules

* **BettingMechanism** – Betting logic and strategies
* **GameSessionManagement** – Session lifecycle handling
* **InputValidationandErrorHandling** – Validation and exception handling
* **StakeManagementOperations** – Stake tracking and monitoring
* **UserInteraction** – Interactive console UI
* **WinLossCalculation** – Statistics and analytics
* **GamblerProfileManagement** – Gambler profile operations

---


