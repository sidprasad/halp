import gptinterface
from utilities import *
import random



### TODO:
# [] provide question level alongside question
# [] Algorithm to determine question level





def get_random_topic():
    data_kind = random.choice(list(DataKind))
    data_processor = random.choice(list(DataProcessor))
    return (data_kind, data_processor)

# https://www.fortbendisd.com/cms/lib/TX01917858/Centricity/Domain/2615/Costas_3_Levels_of_Thinking.pdf
def get_costas_level_prompt(level):
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
            [QUESTION] should not have an obvious right or wrong answer.
            '''
    return "[QUESTION] should be focused on the privacy policy, and encourage thought about what information is collected, who it is shared with or what it is used for."


def get_level(data_kind, data_processor):

    # PErhaps we should bias questions --> TOWARDS <-- these levels for these question types.
    ## Level 1 if its an area where students do not know what is going on.
    ## Level 2 if its an area where student opinion is mixed. These questions require students to expand what they already know by using facts, details, or clues.
    ## Level 3 if it is an area where students have a good understanding of the topic. These questions require students to reflect on their thinking and be able to respond with a
    # personal opinion that is supported by facts. The student makes a value judgment or wonders about something. There is no right or wrong answer.

    return random.randint(1, 3)

class QuestionGenerator:
    def gen_question(self, policy_url):
        system_prompt = self.get_system_prompt(policy_url=policy_url)
        user_prompt = self.get_user_prompt()
        raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)
        ## Re-engineer to return question level, and potential answer.
        return try_parse_json_question(raw_str)

        
    def get_relation_string(self, data_kind, data_processor):
        return "[QUESTION] should focus on {dk} and how/if it is shared with {dp}.".format(dp = data_processor, dk = data_kind)


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

    # TODO: Improve        
    def get_user_prompt(self):

        (data_kind, data_processor) = get_random_topic()
        level = get_level(data_kind, data_processor)
        rel_prompt = self.get_relation_string(data_kind, data_processor)
        level_prompt = get_costas_level_prompt(level)

        # Generate prompt
        p = "Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY]" + rel_prompt + level_prompt
        return p
