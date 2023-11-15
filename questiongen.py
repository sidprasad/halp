import gptinterface
from utilities import *
from questionutils import *



### TODO:
# [] provide question level alongside question




class QuestionGenerator:
    def gen_question(self, policy_url):
        system_prompt = self.get_system_prompt(policy_url=policy_url)
        user_prompt_data = self.get_user_prompt()
        user_prompt = user_prompt_data['prompt']

        raw_str = gptinterface.ask_gpt_chunked(system_prompt=system_prompt, user_prompt= user_prompt)
        
        ## Re-engineer to return question level, and potential answer.
        q = try_parse_json_question(raw_str)
        q['Level'] = user_prompt_data['level']
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
        p = "Employing the Socratic method, ask a student a [QUESTION] about the [PRIVACY POLICY]" + rel_prompt + level_prompt




        return { 'prompt' : p, 'level': level }
