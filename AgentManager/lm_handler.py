
import os
import yaml
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI

from AgentManager.log import logger

base_dir = os.path.dirname(os.path.dirname(__file__))
config_path = os.path.join(base_dir, "AgentManager" ,"config.yaml")

# Load YAML config
with open(config_path, "r") as file:
    config = yaml.safe_load(file)



class LMHandler:
    def __init__(self):
        return

    def get_base_llm(self):
        llm = ChatGoogleGenerativeAI(
            model=config["lm"]["base_model"]["model"],  # or "gemini-1.5-pro" depending on access
            temperature=config["lm"]["base_model"]["temperature"],
            api_key=config["lm"]["base_model"]["api_key"]
        )
        logger.info(f"Initialized {config['lm']['base_model']['model']} as Base LLM")
        return llm

# if __name__ == "__main__":
#     lm = LLMHandler()
#     llm = lm.get_base_llm()
#     print("Hello World")
#     query = "why the sky is blue?"
#     response = llm.invoke(query)
#     print("Response: ", response)