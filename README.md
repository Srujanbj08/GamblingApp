# GamblingApp

GamblingApp is a production-style Python application designed for interactive gambling session management, betting operations, stake tracking, and analytical reporting. The project follows a layered service-based architecture with support for validation auditing, strategy-based betting, transaction management, and rich terminal reporting.

Built using Python, MySQL, Redis, and Celery, the application demonstrates scalable backend design, clean modular structure, and real-time session handling.

---

## Features

* Interactive gambling session management
* Manual and strategy-based betting
* Stake lifecycle and transaction tracking
* Win/loss analytics and reporting
* Validation and audit logging
* Celery-powered background task processing
* MySQL database integration
* Rich terminal UI for live reporting

---

## Tech Stack

* Python 3
* MySQL
* Redis
* Celery
* Rich
* python-dotenv

---

## Project Structure

```bash id="l40fx6"
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
├── main.py
└── requirements.txt
```

---

## Setup

Install dependencies:

```bash id="eonpdi"
pip install -r requirements.txt
```

Configure environment variables in `.env`.

Run the application:

```bash id="9lt7yz"
python main.py
```

Start Celery worker:

```bash id="1z4svf"
celery -A tasks worker --loglevel=info
```

---

## Capabilities

* Create and manage gambler profiles
* Start, pause, resume, and end sessions
* Execute automated or manual betting strategies
* Monitor stake boundaries and risks
* Generate analytical session summaries and reports

---

