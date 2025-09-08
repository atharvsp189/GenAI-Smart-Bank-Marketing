from langchain.agents import initialize_agent, Tool
from AgentManager.FinanceAgent.finance_resources import knwlg, usr_info

class ToolHandler:
    
    def __init__(self):
        self.knowledge_tool = Tool(
            name="Knowledge",
            func=knwlg.search_past_resolutions,
            description="Use this to answer questions from the document database"
        )
        self.user_info_tool = Tool(
            name="UserInfoTool",
            func=usr_info.get_user_info,
            description="Use this to fetch information about the user"
        )