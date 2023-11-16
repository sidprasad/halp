import gptinterface
from utilities import *


class GPTAnswerChecker:


    def check_answer(self, question, answer, policy_url):
        system_prompt = self.get_system_prompt(policy_url=policy_url)
        user_prompt = self.get_user_prompt(question = question, answer = answer)
        raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)
        return try_parse_json_answercheck(raw_str)

    # Will abstract out to various connectors
    def get_system_prompt(self, policy_url):

        plaintext_policy = get_policy_from_web(policy_url)

        PLAINTEXT_SYSTEM_PROMPT = '''You are dealing with the [PRIVACY POLICY] below:
            [PRIVACY POLICY]
            {p}

            I was asked a [QUESTION] about [PRIVACY POLICY] and responded with an [ANSWER]. 
            Is [ANSWER] a correct answer to [QUESTION]?
            Also answer [QUESTION] with an [ALTERNATIVE ANSWER].
        '''.format(p = plaintext_policy)
        return PLAINTEXT_SYSTEM_PROMPT

        
    def get_user_prompt(self, question, answer):
        return '''            
            [QUESTION] {q}
            [ANSWER] {a}

            Format your response as follows:
            {{
                "Correct" : [true if [ANSWER] is correct, false if incorrect],
                "AltAnswer" : [ALTERNATIVE ANSWER]
            }}
        '''.format(q = question, a = answer)