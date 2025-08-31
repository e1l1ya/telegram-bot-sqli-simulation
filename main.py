import sqlite3
from telegram import KeyboardButton, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

DB_NAME = "votes.db"
TOKEN = "TOKEN"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Votes table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS votes (
            name TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)

    # Insert candidates if not already present
    for candidate in ["DuckMen", "Wolfy", "Just a random old man"]:
        cur.execute("INSERT OR IGNORE INTO votes (name, count) VALUES (?, ?)", (candidate, 0))

    # Admins table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT
        )
    """)

    # Ensure default admins exist
    default_admins = [
        (950818049, "e1l1ya", "Eiliya"),
        (123456789, "Paul", "ADMIN")
    ]

    for user_id, username, name in default_admins:
        cur.execute("SELECT 1 FROM admins WHERE user_id = ?", (user_id,))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO admins (user_id, username, name) VALUES (?, ?, ?)",
                (user_id, username, name)
            )

    conn.commit()
    conn.close()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    
    user_id = user.id
    first_name = user.first_name or ""
    last_name = user.last_name or ""

    
    keyboard = [
        [KeyboardButton("🦆 Vote for - DuckMen")],
        [KeyboardButton("🐺 Vote for - Wolfy")],
        [KeyboardButton("👨‍🦳 Vote for - Just a random old man")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "This is the biggest election in the world. Select your candidate:",
        reply_markup=reply_markup
    )
    init_db()

async def handle_vote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "Vote for - " not in text:
        return  # Ignore non-voting messages

    # Extract candidate name (remove everything before " - ")
    candidate = text.split(" - ", 1)[-1]

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Update vote count
    cur.execute("UPDATE votes SET count = count + 1 WHERE name = " + '"' + candidate + '"')
    conn.commit()

    # Fetch new count
    cur.execute("SELECT count FROM votes WHERE name = " + '"' + candidate + '"')
    row = cur.fetchone()
    conn.close()

    if row:
        count = row[0]
        await update.message.reply_text(f"You voted for {candidate}! 🎉\nYou can see the full result: /result\nCurrent votes: {count}")
    else:
        await update.message.reply_text("❌ Candidate not found.")


async def show_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT name, count FROM votes ORDER BY count DESC")
    results = cur.fetchall()
    conn.close()

    if not results:
        await update.message.reply_text("No votes yet.")
        return

    message = "📊 Current Results:\n\n"
    for name, count in results:
        message += f"{name}: {count} votes\n"

    await update.message.reply_text(message)

def main():
    init_db()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("result", show_results))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vote))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
