# Telegram bot SQLi simulation

This repository contains a **Telegram bot** that simulates a SQL injection vulnerability in a voting system. This project is intended **for educational purposes only** to demonstrate SQL injection risks in Python applications. Do **not** use this bot in production or against real users.

---

## Features

- Vote for candidates via Telegram messages
- Stores votes in a SQLite database
- Admin management
- Demonstrates how **unsanitized SQL queries** can be exploited
- View current voting results

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/e1l1ya/telegram-bot-sqli-simulation.git
cd telegram-bot-sqli-simulation
````

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your Telegram bot token in the code (`TOKEN` variable in `main.py` line 6).

5. Run the bot:

```bash
python main.py
```

---

## Usage

1. Start the bot by sending `/start` in Telegram.
2. Vote for a candidate by selecting a button.
3. View results by sending `/result`.

---

## Important Notes

* This bot **intentionally contains unsafe SQL queries** to simulate SQL injection.
* This project is **for learning purposes only**. Do **not** use it for real attacks.
* All user votes are stored in `votes.db`.

---

## Support

Follow [HackMeLocal](https://t.me/hackmelocal) on Telegram for more educational security content.

---

## License

This project is licensed under the [MIT License](LICENSE).
