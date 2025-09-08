
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from typing import Optional

from .tool_handler import ToolHandler
from AgentManager import history_handler
from AgentManager import get_lm_handler
from AgentManager.FinanceAgent.finance_resources import prompts

lm = get_lm_handler()

class FinanceAgentHandler:
    
    def __init__(self):
        self.tool_handler = ToolHandler()
        self.llm = lm.get_base_llm()
    
    def create_finance_agent(self):
        
        # memory = MemorySaver()
        
        # agent = create_react_agent(
        #     model=self.llm,
        #     tools=[
        #         self.tool_handler.knowledge_tool,
        #         self.tool_handler.user_info_tool
        #     ],
        #     checkpointer=memory
        # )

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Add a system-style first message
        memory.chat_memory.add_message(
            prompts.finance_agent_template
        )

        agent = initialize_agent(
            tools=[
                self.tool_handler.knowledge_tool,
                self.tool_handler.user_info_tool
            ],
            llm=self.llm,
            agent="chat-conversational-react-description",
            memory=memory,
            verbose=True
        )
        return agent