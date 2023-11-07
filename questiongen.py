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

        
    def get_user_prompt(self):
        return ''' You are a tutor helping determine whether users correctly understand the [PRIVACY POLICY]. Employing the Socratic method,
        ask a student a question about the [PRIVACY POLICY].
        '''
