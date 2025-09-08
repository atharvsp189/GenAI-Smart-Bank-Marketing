import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from AgentManager import get_query_handler
from AgentManager.FinanceAgent import FinanceAgentHandler

# 🔑 Set your tokens here (or export as ENV variables)
TELEGRAM_TOKEN = ""
OPENAI_API_KEY = ""

query_handler = get_query_handler()

session_id = ""

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Starting Bot")
    obj = FinanceAgentHandler()
    global agent
    agent = obj.create_finance_agent()
    await update.message.reply_text("Hello 👋! I’m your AI assistant. Ask me anything!")

# Handle messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    print(f"Received Input: {user_input}")
    response = agent.invoke({"input": user_input})
    agent_response = response['output']
    query_handler.post_process_query(
        user_query=user_input,
        assistant_response=agent_response,
        session_id=session_id
    )
    print("Response: ", agent_response)
    await update.message.reply_text(agent_response)

# Main function
def main():
    # Build Telegram bot app
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run bot
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
