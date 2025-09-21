import telebot
import requests
import json
import random
from colorama import Fore, Style

# === BOT TOKEN ===
BOT_TOKEN = "BOT_TOKEN"  # 🔁 Replace with your bot token
bot = telebot.TeleBot(BOT_TOKEN)

# === API CONFIGURATION ===
API_TOKEN = "API"
LANG = "ru"
LIMIT = 300
URL = "https://leakosintapi.com/"

# === START MESSAGE ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "👋 Welcome to *Professor Anish Bot*\n\n"
        "🔍 Send your target number/email (e.g. +91********** or email@example.com)\n"
        "_I will search for leaked data if available._\n\n"
        "🔴 *Credit by ANISH EXPLOITS*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown')

# === FORMAT RESULT LIKE JS STYLE ===
def format_as_js(data):
    lines = []
    for key, value in data.items():
        value_str = json.dumps(value)
        lines.append(f"  {key}: {value_str}")
    return "{\n" + "\n".join(lines) + "\n}"

# === HANDLE TEXT MESSAGE (Target Input) ===
@bot.message_handler(func=lambda message: True)
def handle_query(message):
    query = message.text.strip()

    # API payload
    payload = {
        "token": API_TOKEN,
        "request": query,
        "limit": LIMIT,
        "lang": LANG
    }

    try:
        response = requests.post(URL, json=payload).json()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ API ERROR: {str(e)}")
        return

    if "Error code" in response:
        bot.send_message(message.chat.id, f"🚫 API Error: {response['Error code']}")
        return

    if response.get("List") == {}:
        bot.send_message(message.chat.id, "❌ No data found.")
        return

    for db in response["List"].keys():
        db_title = "Professor Anish" if db.lower() == "1win" else db
        bot.send_message(message.chat.id, f"📁 *Database:* `{db_title}`", parse_mode='Markdown')

        for entry in response["List"][db]["Data"]:
            formatted = format_as_js(entry)
            bot.send_message(message.chat.id, f"```js\n{formatted}\n```", parse_mode='Markdown')

    bot.send_message(message.chat.id, "🔴 *Credit by ANISH EXPLOITS*", parse_mode='Markdown')

# === RUN BOT ===
print("🤖 Bot is running...")
bot.infinity_polling()