from langchain.prompts import PromptTemplate
from .prompt_handler import prompts
from AgentManager import get_lm_handler
from .models import email_parser

lm = get_lm_handler()

class EmailWriter:
    def __init__(self):
        self.llm = lm.get_base_llm()

    def get_email_writer_prompt(self, product_to_market: str, customer_info: str, guideline: str):
        self.email_writer_template = PromptTemplate(
            input_variables=["product_to_market", "customer_info", "guideline"],
            template=prompts.get_email_writer_prompt_template(),
                partial_variables={"format_instructions": email_parser.get_format_instructions()},
        )
        self.email_writer_prompt = self.email_writer_template.format(
            product_to_market = product_to_market,
            customer_info = customer_info,
            guidelines = guideline
        )
        return self.email_writer_prompt

    def get_email_writer_template(self):
        self.email_writer_template = PromptTemplate(
            input_variables=["product_to_market", "customer_info", "guideline"],
            template=prompts.get_email_writer_prompt_template(),
                partial_variables={"format_instructions": email_parser.get_format_instructions()},
        )
        return self.email_writer_template
    
    def email_writer_chain(self):
        prompt_template = self.get_email_writer_template()
        llm = self.llm
        chain = prompt_template | llm | email_parser
        
        return chain
    
    def get_email_writer_result(self, product_to_market: str, customer_info: str, guideline: str):
        chain = self.email_writer_chain()
        response = chain.invoke({
            "product_to_market": product_to_market,
            "customer_info": customer_info,
            "guidelines": guideline}
        )
        
        return response