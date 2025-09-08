# from telegram_bot import user_chat_map

import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = Final = os.getenv("BOT_USERNAME")

# def send_telegram_message(mobile_number: str, message: str):
#     """
#     Send a message to a Telegram user identified by their mobile number.
#     The mobile_number must already be mapped to a chat_id.
#     """
#     chat_id = user_chat_map.get(mobile_number)

#     if not chat_id:
#         raise ValueError(f"No chat_id found for mobile number {mobile_number}")

#     app.send_message(chat_id=chat_id, text=message)
#     print(f"Message sent to {mobile_number} (chat_id: {chat_id})")

import requests
message = "Send Telegram Message"
user_id = ""
chat_id = ""

print("sending message through url")
url = f"https://api.telegram.org/{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"

r = requests.get(url)
print(r.json())

# send_telegram_message(user_id, message)