from AgentManager.log import logger


class UserInfo:
    def __init__(self):
        pass

    def get_user_info(self, query: str = "NULL"):
        logger.info("user info agent is called")
        return {
            "age": 34,
            "gender": "Female",
            "marital_status": "Married",
            "children": 2,
            "occupation": "IT Project Manager",
            "annual_income": 1450000,
            "loan_status": {
                "active": "yes",
                "type": "Home Loan",
                "balance": 4500000
            },
            "credit_card": {
                "has_card": "yes",
                "type": "Premium"
            },
            "savings_balance": 320000,
            "investment_products": ["Mutual Funds", "Fixed Deposit"],
            "preferred_communication_channel": ["Mobile App", "Email"],
            "location": "Bengaluru, India"
        }