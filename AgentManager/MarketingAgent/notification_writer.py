from langchain.prompts import PromptTemplate
from .prompt_handler import prompts
from AgentManager import get_lm_handler
from .models import notifi_parser

lm = get_lm_handler()

class NotifiWriter:
    def __init__(self):
        self.llm = lm.get_base_llm()

    def get_notifi_writer_prompt(self, product_to_market: str, customer_info: str, guideline: str):
        self.notifi_writer_template = PromptTemplate(
            input_variables=["product_to_market", "customer_info", "guideline"],
            template=prompts.get_notifi_writer_prompt_template(),
                partial_variables={"format_instructions": notifi_parser.get_format_instructions()},
        )
        self.notifi_writer_prompt = self.notifi_writer_template.format(
            product_to_market = product_to_market,
            customer_info = customer_info,
            guidelines = guideline
        )
        return self.notifi_writer_prompt

    def get_notifi_writer_template(self):
        self.notifi_writer_template = PromptTemplate(
            input_variables=["product_to_market", "customer_info", "guideline"],
            template=prompts.get_notifi_writer_prompt_template(),
                partial_variables={"format_instructions": notifi_parser.get_format_instructions()},
        )
        return self.notifi_writer_template
    
    def notifi_writer_chain(self):
        prompt_template = self.get_notifi_writer_template()
        llm = self.llm
        chain = prompt_template | llm | notifi_parser
        
        return chain
    
    def get_notifi_writer_result(self, product_to_market: str, customer_info: str, guideline: str):
        chain = self.notifi_writer_chain()
        response = chain.invoke({
            "product_to_market": product_to_market,
            "customer_info": customer_info,
            "guidelines": guideline}
        )
        
        return response