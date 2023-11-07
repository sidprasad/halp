

from questiongen import QuestionGenerator
from answercheck import AnswerChecker

class DialogicPrompter:
    qgen = QuestionGenerator()
    acheck = AnswerChecker()

    def gen_question(self, policy_url):
        return self.qgen.gen_question(policy_url = policy_url)
    
    def check_answer(self, policy_url, question, answer):
        return self.acheck.check_answer(policy_url = policy_url, question = question, answer = answer)

