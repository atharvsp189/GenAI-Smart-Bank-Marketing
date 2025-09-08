import os
import json
from langchain.schema import HumanMessage, AIMessage, BaseMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory

from AgentManager.log import logger
# from AgentManager.FinanceAgent import prompts

system_prompt = """You are a Finance Sales Chatbot for the Bank of Dholakpur. You act like a friendly, professional, and persuasive banking advisor

        Tone & Style:
        - Cheerful, approachable, and trustworthy
        - Always customer-first and helpful
        - Subtly persuasive, highlighting benefits & value

        Goal:

        - Understand the customer's needs through conversation
        - Provide accurate information about banking products
        - Recommend the most suitable product(s) to the customer
        - Encourage the customer to take the next step (sign up, apply, learn more)
        - when ask to provide the link to provide the link to the source

        Tools Available:

        1. knowledge_agent → Use to fetch accurate details about bank products.
        2. user_info → Use to get user's profile (age, income, existing products). Use this for personalization call it without any argument

        Instructions:

        - Always start by clarifying the customer's needs or intent.
        - Use knowledge_agent when you need product details.
        - Use user_info when you want to personalize recommendations.
        - When recommending products, explain in simple benefits (how it helps the customer).
        - End responses with a call to action (e.g., "Would you like me to show you how to apply?").
        - If the user is confused, guide them step by step.
        - Be proactive: if you notice a gap in their financial portfolio, suggest products that add value
        - keep the responses short and conversational
        - Do NOT answer the unrealated questions other than banking queries

        Example Behaviors:

        If user asks: "What's the best savings account?"
        → Use knowledge_agent for account details
        → Use user_info to check income/age, then suggest best fit
        → Reply cheerfully: "Since you're 25 and just starting your career, the XYZ Savings Account could be perfect — it gives higher interest and zero fees for young professionals!
        """


class ChatHistoryHandler:
    def __init__(self, storage_dir: str = "chat_histories"):
        self._chatbot_store = {}   # session_id -> ChatMessageHistory
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)

    def _get_file_path(self, session_id: str) -> str:
        """Return file path for storing session history."""
        return os.path.join(self.storage_dir, f"{session_id}.json")

    def _save_history(self, session_id: str, history: ChatMessageHistory):
        """Persist chat history to disk as JSON."""
        try:
            messages_data = []
            for msg in history.messages:
                role = (
                    "human" if isinstance(msg, HumanMessage)
                    else "ai" if isinstance(msg, AIMessage)
                    else "system"
                )
                messages_data.append({"role": role, "content": msg.content})

            with open(self._get_file_path(session_id), "w", encoding="utf-8") as f:
                json.dump(messages_data, f, ensure_ascii=False, indent=2)

            logger.info(f"Saved chat history for session {session_id}")
        except Exception as e:
            logger.error(f"Error saving chat history for {session_id}: {e}")

    def _load_history(self, session_id: str) -> ChatMessageHistory:
        """Load chat history from disk if available."""
        history = ChatMessageHistory()
        try:
            file_path = self._get_file_path(session_id)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    messages_data = json.load(f)

                for msg in messages_data:
                    if msg["role"] == "human":
                        history.add_message(HumanMessage(content=msg["content"]))
                    elif msg["role"] == "ai":
                        history.add_message(AIMessage(content=msg["content"]))
                    else:
                        history.add_message(BaseMessage(content=msg["content"]))

                logger.info(f"Loaded chat history for session {session_id}")
        except Exception as e:
            logger.error(f"Error loading chat history for {session_id}: {e}")
        return history

    def _get_or_create_history(self, session_id: str) -> ChatMessageHistory:
        if session_id not in self._chatbot_store:
            self._chatbot_store[session_id] = self._load_history(session_id)
            history = self._chatbot_store[session_id]
            # if not history.messages:
                # history.add_message(SystemMessage(content=system_prompt))
        return self._chatbot_store[session_id]

    def add_message(self, session_id: str, role: str, content: str) -> bool:
        """Add a new chatbot message to the history and persist it."""
        try:
            if not isinstance(session_id, str) or not session_id.strip():
                logger.error(f"Invalid session_id for adding chatbot message: {session_id}")
                return False

            history = self._get_or_create_history(session_id)

            if role.lower() in ["user", "human"]:
                history.add_message(HumanMessage(content=content))
            elif role.lower() in ["assistant", "ai", "bot"]:
                history.add_message(AIMessage(content=content))
            else:
                logger.warning(f"Unknown role {role}, storing as generic message.")
                history.add_message(BaseMessage(content=content))

            # Save updated history
            self._save_history(session_id, history)
            return True
        except Exception as e:
            logger.error(f"Error adding chatbot message for session {session_id}: {e}")
            return False

    def get_formatted_history(self, session_id: str) -> str:
        """Return formatted chatbot history as a string."""
        try:
            if not isinstance(session_id, str) or not session_id.strip():
                logger.error(f"Invalid session_id for formatting chatbot history: {session_id}")
                return "Invalid session ID."

            history = self._get_or_create_history(session_id)
            if not history or not history.messages:
                logger.info(f"No chatbot history available for session {session_id}")
                return "No chatbot history available."

            formatted_messages = []
            for msg in history.messages:
                role = "User" if isinstance(msg, HumanMessage) else "Assistant" if isinstance(msg, AIMessage) else "System"
                formatted_messages.append(f"{role}: {msg.content}")

            logger.info(f"Formatted chatbot history for session {session_id}: {len(formatted_messages)} messages")
            # for msg in formatted_messages:
            #     print(msg)
            # logger.info(formatted_messages)
            return "\n".join(formatted_messages)
        except Exception as e:
            logger.error(f"Error formatting chatbot history for session {session_id}: {e}")
            return "Error retrieving chatbot history."
