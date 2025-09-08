from langchain.prompts import PromptTemplate
from .prompt_handler import prompts
from AgentManager import get_lm_handler

lm = get_lm_handler()

class Reflector:
    def __init__(self):
        self.llm = lm.get_base_llm()

    def get_reflector_prompt(self, suggestion: str, previous_strategy: str):
        self.reflect_template = PromptTemplate(
            input_variables=["target_audience"],
            template=prompts.get_relect_prompt_template()
        )
        self.reflector_prompt = self.reflect_template.format(
            suggestions = suggestion,
            previous_strategy=previous_strategy
        )
        return self.reflector_prompt
    
    def get_reflector_result(self, suggestion: str, previous_strategy: str):
        prompt = self.get_reflector_prompt(suggestion, previous_strategy)
        response = self.llm.invoke(prompt)
        
        return response