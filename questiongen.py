import gptinterface
from utilities import *
from questionutils import *

class QuestionGenerator:




    def ensure_question_structure(self, q, level):

        q_lower = q.lower()
        if level == 1:
            return any([w in q_lower for w in l1_words])
        elif level == 2:
            return any([w in q_lower for w in l2_words])
        elif level == 3:
            return any([w in q_lower for w in l3_words])
        else:
            return True

            
            



    def gen_question(self, policy_url):
        system_prompt = self.get_system_prompt(policy_url=policy_url)
        user_prompt_data = self.get_user_prompt()
        user_prompt = user_prompt_data['prompt']

        q = None
        valid_question = False
        max_iter = 5

        while max_iter > 0 and (not valid_question):
            max_iter -= 1
            raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)
            q = try_parse_json_question(raw_str)
            valid_question = self.ensure_question_structure(q['Question'], user_prompt_data['level'])
            q['Level'] = user_prompt_data['level']

        if max_iter == 0:
            q = {'Question' : "Failed Question Gen, please try again.", 'Level' : -1}

        return q
        
    def get_relation_string(self, data_kind, data_processor):
        return "[QUESTION] should focus on {dk} and how/if it is shared with {dp}.".format(dp = data_processor, dk = data_kind)

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

        (data_kind, data_processor) = get_random_topic()
        level = get_level(data_kind, data_processor)
        rel_prompt = self.get_relation_string(data_kind, data_processor)
        level_prompt = get_costas_level_prompt(level)

        # Generate prompt
        p = "Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY]. " + rel_prompt + " " + level_prompt
        return { 'prompt' : p, 'level': level }
