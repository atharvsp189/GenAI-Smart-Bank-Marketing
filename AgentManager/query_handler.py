import os
from datetime import datetime
from AgentManager.FinanceAgent import finance_agent
from AgentManager.log import logger
from AgentManager import history_handler
from AgentManager import get_lm_handler
from langchain_core.messages import SystemMessage
from AgentManager.FinanceAgent import prompts
# from nemoguardrails import LLMRails, RailsConfig

# base_dir = os.path.dirname(__file__)
# print("Base Dir: ", base_dir)
# config_path = os.path.join(base_dir, "rails")
# print("Config Path: ", config_path)

# lm = get_lm_handler()
# llm = lm.get_base_llm()

# config = RailsConfig.from_path(config_path)
# rails_app = LLMRails(config, llm=llm)


class QueryHandler:
    def __init__(self):
        pass

    def process_query(self, user_input: str, session_id: str):
        try:
            logger.info(f"Processing query for session_id {session_id}: {user_input}")

            if not session_id:
                session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                logger.info(f"Generated new session_id: {session_id}")
            
            if not user_input.strip():
                return {'response': 'Please provide a valid query'}
            

            agent = finance_agent.create_finance_agent()
            logger.info("Finance Agent Created")
            
            # if guardrails_result.output: # guardrailing input
            # user_input += f"Input Guardrails output: {guardrails_result}"
            agent_response = agent.run(user_input)
            # response = agent.invoke(
            #     {"messages": [prompts.finance_agent_template, ("user", user_input)]},
            #     config={"configurable": {"thread_id": session_id}}
            # )
            # else: # If Guardrails blocked it, return guardrails message
                # agent_response = guardrails_result.responses[0].get("content", "Blocked by safety filters.")
            
            # final_result = rails_app.generate(prompt=agent_response) # guardrailing output
            
            return agent_response
        
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")

    def post_process_query(self, user_query: str, assistant_response: str, session_id: str):
        try:
            history_handler.add_message(session_id, "user", user_query)
            history_handler.add_message(session_id, "assistant", assistant_response)
            logger.info(f"Post processing query for session: {session_id}")
            history_handler.get_formatted_history(session_id)
            return "Success"
        except Exception as e:
            logger.error(f"Error in post_process_query: {str(e)}", exc_info=True)
            history_handler.add_message(session_id, "system", f"Error in post_process_query: {str(e)}")
            return "Error"