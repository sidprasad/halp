

from questiongen import QuestionGenerator
from answercheck import GPTAnswerChecker
from transformers import pipeline

from sentence_transformers import SentenceTransformer, util


class DialogicPrompter:
    qgen = QuestionGenerator()
    gptacheck = GPTAnswerChecker()
    t5_semantic_similarity = pipeline("text2text-generation", model="t5-base", tokenizer="t5-base")
    semantic_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')



    def gen_question(self, policy_url):
        return self.qgen.gen_question(policy_url = policy_url)
    
    def check_answer(self, policy_url, question, answer, candidate_answer):
        
        #t5a = T5AnswerChecker().check_answer(question = question, policy_url = policy_url, student_answer = answer)



        ### Get the 
        
        ans = self.gptacheck.check_answer(policy_url = policy_url, question = question, answer = answer)
        conf_measure = self.get_measurement_of_feedback(candidate_answer, ans['Explanation'])

        ### TODO: Fix
        ans['Confidence'] = conf_measure
        return ans

    


    def get_measurement_of_feedback(self, t1, t2):
        
        # Embedding for generated and provided answers
        generated_embedding = self.semantic_model.encode(t1, convert_to_tensor=True)
        provided_embedding = self.semantic_model.encode(t2, convert_to_tensor=True)

        # Calculate cosine similarity
        cosine_similarity = util.pytorch_cos_sim(generated_embedding, provided_embedding)

        # Check if the answers are similar
        return cosine_similarity.item()