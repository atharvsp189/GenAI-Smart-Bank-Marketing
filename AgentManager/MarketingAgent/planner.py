from langchain.prompts import PromptTemplate
from .prompt_handler import prompts
from AgentManager import get_lm_handler

lm = get_lm_handler()

class Planner:
    def __init__(self):
        self.llm = lm.get_base_llm()

    def get_planner_prompt(self, target_audience):
        self.planner_template = PromptTemplate(
            input_variables=["target_audience"],
            template=prompts.get_planner_prompt_template()
        )
        self.planner_prompt = self.planner_template.format(
            target_audience=target_audience
        )
        return self.planner_prompt
    
    def get_planner_result(self, target_audience: str):
        prompt = self.get_planner_prompt(target_audience)
        response = self.llm.invoke(prompt)
        
        return response