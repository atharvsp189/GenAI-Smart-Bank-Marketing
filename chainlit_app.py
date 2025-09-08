import uuid
import chainlit as cl
from AgentManager import get_query_handler
from AgentManager.FinanceAgent import finance_agent, prompts
from AgentManager.FinanceAgent import FinanceAgentHandler

query_handler = get_query_handler()


@cl.on_chat_start
async def start_chat():
    # Create a new session_id for the user
    session_id = str(uuid.uuid4())
    global agent 
    obj = FinanceAgentHandler()
    agent = obj.create_finance_agent()
    cl.user_session.set("session_id", session_id)
    await cl.Message(content="👋 Hello! How can I help you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    session_id = cl.user_session.get("session_id")
    try:
        # msg = cl.Message(content="", author="Assistant")
        # await msg.send()

        user_input = message.content

        # response = query_handler.process_query(
        #     user_input=message.content,
        #     session_id=session_id
        # )
        # response = agent.invoke(
        #         {"messages": [prompts.finance_agent_template, ("user", user_input)]},
        #         config={"configurable": {"thread_id": session_id}}
        # )

        response = agent.invoke({"input": user_input})
        agent_response = response['output']
        # agent_response = response['messages'][-1].content

        await cl.Message(content=agent_response).send()

        query_handler.post_process_query(
            user_query=user_input,
            assistant_response=agent_response,
            session_id=session_id
        )
    except Exception as e:
        await cl.Message(content=f"Error: {e}", author="Assistant").send()
