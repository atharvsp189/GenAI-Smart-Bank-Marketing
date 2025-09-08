import os

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon import events

from AgentManager import get_query_handler
from AgentManager.FinanceAgent import FinanceAgentHandler

query_handler = get_query_handler()

from dotenv import load_dotenv
load_dotenv()

# Your API credentials
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = '+919765670884'

# Create the client
client = TelegramClient('finance_bot', api_id, api_hash)

# Event handler for new messages
@client.on(events.NewMessage)
async def handle_message(event):
    sender = await event.get_sender()
    message = event.message
    print(f"New message from {sender.username or sender.phone}: {message.text}")
    response = agent.invoke({"input": message.text})
    agent_response = response['output']
    query_handler.post_process_query(
        user_query=message,
        assistant_response=agent_response,
        session_id=sender.phone
    )
    print("Response: ", agent_response)
    await client.send_message(sender.phone, agent_response)


async def main():
    # Start the client
    await client.start(phone)
    obj = FinanceAgentHandler()
    global agent
    agent = obj.create_finance_agent()
    await client.send_message('me', "Hello 👋! I’m your AI assistant. Ask me anything!")
    
    if not await client.is_user_authorized():
        print("Authorising")
        await client.send_code_request(phone)
        code = input('Enter the code you received: ')
        await client.sign_in(phone, code)
    print("Authorized")

    print("Sending Messages")

    print("Listening for new messages...")
    await client.run_until_disconnected()
    print("sending messages")
    await client.send_message('+919373756219', "Hello, Harsh!\nTest for telegram feature")

# Run the client
with client:
    client.loop.run_until_complete(main())