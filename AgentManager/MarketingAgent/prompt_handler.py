class PromptHandler:
    def __init__(self):
        pass

    def get_planner_prompt_template(self):
        self.PLAN_PROMPT_TEPLATE = """
            You are the CMO of a reputed bank. \
                Your role is to guide a digital sales team whose job is to deliver personalized sales pitches to customers. \
                Provide clear, concise guidelines for the team, covering: tone of conversation, approach, key points to keep in mind, and best practices. \
                Present the response in short, actionable bullet points under 100 words.

                Traget Audience is:
                {target_audience}
        """
        return self.PLAN_PROMPT_TEPLATE

    def get_relect_prompt_template(self):
        self.REFLECT_PROMPT = """
        As the CMO of a reputed bank \
        you have previously provided guidelines to the digital sales team on delivering personalized sales pitches to customers covering tone, approach, and key points. \
        Now, the higher authorities have suggested changes to the marketing campaigns. \
        Based on these suggestions, redefine and update the sales guidelines for the team. \
        Include actionable, concise recommendations in bullet points, ensuring they align with the updated marketing strategy while maintaining personalization for customers. \
        Present the response in short, actionable bullet points under 100 words.

        -- Suggestions --
        {suggestions}

        -- Previous Strategy --
        {previous_strategy}
        """

        return self.REFLECT_PROMPT
    
    def get_notifi_writer_prompt_template(self):
        self.NOTIFI_WRITER_PROMPT = """You are a content writer for a reputed bank \
        specializing in creating engaging and persuasive content that sparks customer curiosity. \
        Your task is to write short Telegram messages or notifications that grab the customer's attention and act as a starting point to introduce them to a product. \
        Keep the messages concise, friendly, and curiosity-driven \
        provide just content no greetings
        provide output in a json format:
        
        -- Market this product to them 
        {product_to_market}
        
        -- Here is the brieft about customer
        {customer_info}
        
        -- Guideline
        {guidelines}
        """

        return self.NOTIFI_WRITER_PROMPT
    
    def get_email_writer_prompt_template(self):
        self.Email_WRITER = """You are a content writer for a reputed bank, specializing in creating engaging and persuasive content. \
            Your task is to write email campaigns targeted at young customers. \
            The emails should be concise, relatable, and designed to capture attention quickly. \
            Focus on: subject lines that spark curiosity, friendly yet professional tone, clear value for the customer, and encouraging them to take action \
            just provide the body of an email no greetings
            provide one email only as a json format
            subject, body
            
            -- user info
            {customer_info}

            -- product to market\
            {product_to_market}
            
            -- Guideline
            {guidelines}
            """
        
        return self.Email_WRITER


prompts = PromptHandler()