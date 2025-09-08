from AgentManager.chat_history_handler import ChatHistoryHandler
history_handler = ChatHistoryHandler()

def get_query_handler():
    from AgentManager.query_handler import QueryHandler
    return QueryHandler()

def get_lm_handler():
    from AgentManager.lm_handler import LMHandler
    return LMHandler()

__all__ = [
    "history_handler",
    "get_query_handler",
    "get_lm_handler",
]