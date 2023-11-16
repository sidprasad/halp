

from questiongen import QuestionGenerator
from answercheck import GPTAnswerChecker
from transformers import pipeline

class DialogicPrompter:
    qgen = QuestionGenerator()
    gptacheck = GPTAnswerChecker()
    t5_semantic_similarity = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base")



    def gen_question(self, policy_url):
        return self.qgen.gen_question(policy_url = policy_url)
    
    def check_answer(self, policy_url, question, answer, candidate_answer):
        
        #t5a = T5AnswerChecker().check_answer(question = question, policy_url = policy_url, student_answer = answer)



        ### Get the 
        
        ans = self.gptacheck.check_answer(policy_url = policy_url, question = question, answer = answer)
        conf_measure = self.get_measurement_of_feedback(candidate_answer, ans['Explanation'])

        ### TODO: Fix
        ans['Confidence'] = conf_measure

    


    def get_measurement_of_feedback(self, a1, a2):
              
        # Combine sentences for input to T5
        input_text = f"check semantic similarity: '{a1}' and '{a2}'"

        # Generate output using T5
        output = self.t5_semantic_similarity(input_text, max_length=50, num_beams=4, length_penalty=2.0, early_stopping=True)

        ## Now we should be able to examine the output. If both answers are semantically similar, we may be more confident in the answer.

        # Extract the generated output
        generated_text = output[0]['generated_text']

