import gptinterface
from utilities import *


class QuestionGenerator:

    # https://www.fortbendisd.com/cms/lib/TX01917858/Centricity/Domain/2615/Costas_3_Levels_of_Thinking.pdf
    def get_costas_level_prompt(self, level):

        ## Level 1 if its an area where students do not know what is going on.
        if level == 1:
            return '''
                [QUESTION] should be answerable with yes, no, or specific information found in [POLICY].
                [QUESTION] should encorage students to define, define, describe, identify, list or name.
                '''
        ## Level 2 if its an area where student opinion is mixed. These questions require students to expand what they already know by using facts, details, or clues.
        elif level == 2:
            return '''
                [QUESTION] should require students to expand what they already know by using facts or details in [POLICY].
                [QUESTION] should encorage students to analyze, compare, contrast, group, infer or sequence.'''
        ## Level 3 if it is an area where students have a good understanding of the topic. These questions require students to reflect on their thinking and be able to respond with a
        # personal opinion that is supported by facts. The student makes a value judgment or wonders about something. There is no right or wrong answer.
        elif level == 3:
            return '''
                [QUESTION] should require students to reflect on their thinking and be able to respond with a personal opinion that is supported by facts in [POLICY]. 
                [QUESTION] should encorage students to apply a principle, evaluate, hypothesize,imagine, judge, predict or speculate.
                '''
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
        return ''' 
        Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY].
        [QUESTION] should be focused on the privacy policy, and encourage thought about
         what information is collected, who it is shared with or what it is used for.'''
