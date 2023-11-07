import gptinterface
from utilities import *


class DialogicPrompter:


    # Add constructor

    def get_costas_level_prompt(self, level):
        if level == 1:
            return ""
        elif level == 2:
            return ""
        elif level == 3:
            return ""
        return ""

    def gen_question(self, context, level):
        return ""

    def check_answer(self, q, a, pp):
        system_prompt = self.get_system_prompt(policy_url=pp)
        user_prompt = self.get_user_prompt(question = q, answer = a)


        ## TODO: THis needs to be fixed :)
        return gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)

    # Will abstract out to various connectors
    def get_system_prompt(self, policy_url):

        plaintext_policy = get_policy_from_web(policy_url)

       

        PLAINTEXT_SYSTEM_PROMPT = ''' You are a tutor helping determine whether users correctly understand the privacy policy below:
            [PRIVACY POLICY]
            {p}

            For this policy, the student was asked a [QUESTION] and responded with an [ANSWER]. 
            Determine whether [ANSWER] answers [QUESTION], whether it was correct or incorrect.
            {{
                'Relevant' : [True if [ANSWER] answers [QUESTION], False otherwise],
                'Correct' : [True if the answer is correct, False if incorrect],
                'Explanation' : [A 2 sentence explanation of why the answer was correct or incorrect],
                'Confidence' : [Your confidence in this decision on a scale of 0 to 1, with 0 being not confident and 1 being completely certain.]
            }}

        '''.format(p = plaintext_policy)
        return PLAINTEXT_SYSTEM_PROMPT

        
    def get_user_prompt(self, question, answer):
        return ''' 

            The student was asked the following question:
            
            [QUESTION] {q}

            and gave the following answer:
            [ANSWER] {a}
        '''.format(q = question, a = answer)