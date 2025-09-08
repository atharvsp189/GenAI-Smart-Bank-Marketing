import os

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import events

from AgentManager.log import logger

import yaml

base_dir = os.path.dirname(os.path.dirname(__file__))
secrets_path = os.path.join(base_dir, "Telegram", "secrets.yaml")

# Load YAML config
with open(secrets_path, "r") as file:
    config = yaml.safe_load(file)

class TelegramTelethon():
    def __init__(self):
        api_id = config["telegram"]["API_ID"]
        api_hash = config["telegram"]["API_HASH"]
        self.phone = config["telegram"]["PHONE"]
        self.client = TelegramClient('session_name', api_id, api_hash)

    async def __aenter__(self):
        await self.client.start(phone=self.phone)
        logger.info("Telegram client initialized")
        return self
    
    
    async def send_telegram_message(self, receiver: str = 'me', message: str = "Empty String"):
        try:
            async with self.client:
                logger.info(f"Sending message to {receiver}")
                await self.client.send_message(receiver, message)
                logger.info(f"Message Sent to {receiver}")
        except Exception as e:
            logger.info(f"An Error Occured while sending message {e}")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.disconnect()
        logger.info("Telegram client disconnected")
