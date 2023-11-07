import gptinterface
from utilities import *
import json


class Assistant:


    def get_system_prompt(self, policy_url):

        plaintext_policy = get_policy_from_web(policy_url)
        PLAINTEXT_SYSTEM_PROMPT = ''' You are a tutor helping answer user questions about the privacy policy below:
            [PRIVACY POLICY]
            {p}


        '''.format(p = plaintext_policy)
        return PLAINTEXT_SYSTEM_PROMPT


    def get_user_prompt(self, question):
        return ''' 
            For this [PRIVACY POLICY], the student asked the following [QUESTION]:        
            [QUESTION] {q}

            Answer this question using only information from [PRIVACY POLICY]:
            {{
                'Answer' : [A short answer to the question],
                'Confidence' : [Your confidence in this decision on a scale of 0 to 1, with 0 being not confident and 1 being completely certain.]
            }}
        '''.format(q = question)
    
    def gen_answer(self, question, privacy_policy):
        system_prompt = self.get_system_prompt(policy_url=privacy_policy)
        user_prompt = self.get_user_prompt(question = question)
        raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)

        ## Make this robust
        return json.loads(raw_str)