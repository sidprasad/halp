import gptinterface
from utilities import *


class QuestionGenerator:


    def get_costas_level_prompt(self, level):
        if level == 1:
            return ""
        elif level == 2:
            return ""
        elif level == 3:
            return ""
        return ""

    def gen_question(self, policy_url):
        system_prompt = self.get_system_prompt(policy_url=policy_url)
        user_prompt = self.get_user_prompt()
        raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)
        return try_parse_json_question(raw_str)

        


    # Will abstract out to various connectors
    def get_system_prompt(self, policy_url):

        plaintext_policy = get_policy_from_web(policy_url)

    
        PLAINTEXT_SYSTEM_PROMPT = ''' You are a tutor helping users correctly understand the privacy policy below:
            [PRIVACY POLICY]
            {p}

            Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY].
            
            Format your response in JSON as follows:
            {{
                "Question" : The text of [QUESTION],
                "Authentic" : false if the answer is can be determined from [PRIVACY POLICY], true otherwise,
                "Answer" : A correct answer to [QUESTION],
            }}

        '''.format(p = plaintext_policy)
        return PLAINTEXT_SYSTEM_PROMPT

        
    def get_user_prompt(self):
        # This will be improved
        return ''' Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY].   '''
