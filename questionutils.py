
import random
from enum import Enum
import pandas as pd
import os


BAD_UNDERSTANDING = 1 ## Level 1 if its an area where students do not know what is going on.
MIXED_UNDERSTANDING = 2 ## Level 2 if its an area where student understanding is mixed, or the scenario is a little complicated.
GOOD_UNDERSTANDING = 3 ## Level 3 if it is an area where students have a good understanding of the topic.

l1_words = ['collect', 'copy', 'define','describe', 'examine', 'find','group', 'identify', 'indicate','label', 'list', 'locate', 'match','name', 'omit', 'observe', 'point','provide', 'quote', 'read', 'recall','recite', 'recognize', 'repeat','reproduce', 'say', 'select', 'sort','spell', 'state', 'tabulate', 'tell','touch', 'underline', 'who','when', 'where', 'what','alter', 'associate','calculate', 'categorize','communicate', 'convert','distinguish', 'expand','explain', 'inform', 'name','alternatives', 'outline','paraphrase', 'rearrange','reconstruct', 'relate','restate','summarize', 'tell the','meaning of', 'translate','understand', 'verbalize','write']
l2_words = ["acquire", "adopt", "apply","assemble", "capitalize","construct", "consume","demonstrate","develop", "discuss","experiment","formulate","manipulate", "organize","relate", "report", "search","show", "solve novel","problems", "tell","consequences", "try","use", "utilize", "analyze", "arrange","break down","categorize", "classify","compare", "contrast","deduce", "determine","diagram", "differentiate","discuss causes", "dissect","distinguish", "give","reasons", "order","separate", "sequence","survey", "take apart","test for", "why"]
l3_words = ["appraise", "argue", "assess", "challenge", "choose", "conclude","criticize", "critique", "debate", "decide", "defend", "discriminate","discuss", "document", "draw conclusions", "editorialize", "evaluate","grade", "interpret", "judge", "justify", "prioritize", "rank", "rate","recommend", "reject", "support", "validate", "weigh", "alter", "build","combine", "compose", "construct", "create", "develop", "estimate","form", "generate", "hypothesize", "imagine", "improve", "infer","invent", "modify", "plan", "predict", "produce", "propose", "reorganize","rewrite", "revise", "simplify", "synthesize"]

class DataKind(Enum):
    ASSIGNMENT_SUBMISSIONS = 1
    PERSONAL_INFORMATION = 2
    INTERACTION_DATA = 3
    OTHER = 4
    
    def __str__(self):
        if self == DataKind.OTHER:
            return "the collection, ownership or sharing of data"
        return self.name.title().replace("_", " ")
    @staticmethod
    def from_str(s):
        if s == "the collection, ownership or sharing of data":
            return DataKind.OTHER
        return DataKind[s.upper().replace(" ", "_")]
    
class DataProcessor(Enum):
    OTHER_STUDENTS = 1
    COURSE_INSTRUCTOR = 2
    COURSE_TAS = 3
    EDUCATION_RESEARCHERS = 4
    THIRD_PARTY_CORPORATIONS = 5

    def __str__(self):
        if self == DataProcessor.THIRD_PARTY_CORPORATIONS:
            return "corporations (including the producer of this software)"
        return self.name.title().replace("_", " ")
    
    @staticmethod
    def from_str(s):
        if s == "corporations (including the producer of this software)":
            return DataProcessor.THIRD_PARTY_CORPORATIONS
        return DataProcessor[s.upper().replace(" ", "_")]

# Get the directory path of the current file
dirpath = os.path.dirname(os.path.abspath(__file__))
seed_path = os.path.join(dirpath, "csnseed.csv")


def get_seed_weights(seed_path):
    
    seed_weights = { dke : { dpe : random.random() for dpe in DataProcessor} for dke in DataKind}

    xs = pd.read_csv(seed_path, header=0, index_col=0).to_dict()

    for dk in xs.keys():
        for dp in xs[dk].keys():

            dke = DataKind.from_str(dk)
            dpe = DataProcessor.from_str(dp)

            seed_weights[dke][dpe] = float(xs[dk][dp])
    return seed_weights

# Probably want to update seed weights as we go.
seed_weights = get_seed_weights(seed_path)


def get_random_topic():
    data_kind = random.choice(list(DataKind))
    data_processor = random.choice(list(DataProcessor))
    return (data_kind, data_processor)

# https://www.fortbendisd.com/cms/lib/TX01917858/Centricity/Domain/2615/Costas_3_Levels_of_Thinking.pdf
def get_costas_level_prompt(level):
    if level == 1:
        return '''
            [QUESTION] should be answerable with yes, no, or specific information found in [POLICY].
            [QUESTION] should encorage students to define, define, describe, identify, list or name.
            [QUESTION] should have an obvious right or wrong answer.
            [QUESTION] should use one of the following words: {l1_words}'''.format(l1_words = ", ".join(l1_words))
    elif level == 2:
        return '''
            [QUESTION] should require students to expand what they already know by using facts or details in [POLICY].
            [QUESTION] should encorage students to analyze, compare, contrast, group, infer or sequence.
            Good responses to [QUESTION] should involve applying or analyzing existing knowledge.[QUESTION] should use one of the following words: {l2_words}'''.format(l2_words = ", ".join(l2_words))
    elif level == 3:
        return '''
            [QUESTION] should require students to reflect on their thinking and be able to respond with a personal opinion about [POLICY]. 
            [QUESTION] should encorage students to apply a principle, evaluate, hypothesize, imagine, judge, predict or speculate.
            [QUESTION] should not have an obvious right or wrong answer. [QUESTION] should use one of the following words: {l3_words}'''.format(l3_words = ", ".join(l3_words))
    return "[QUESTION] should be focused on the privacy policy, and encourage thought about what information is collected, who it is shared with or what it is used for."

def get_level(data_kind, data_processor):
    target_level = weight_to_understanding(seed_weights[data_kind][data_processor])
    weights = { GOOD_UNDERSTANDING : 0.1, BAD_UNDERSTANDING : 0.1, MIXED_UNDERSTANDING : 0.1}
    weights[target_level] = 0.8

    levels = list(weights.keys())
    level_weights = list(weights.values())
    return random.choices(levels, weights = level_weights)[0]

def weight_to_understanding(x):
    if x < 0.33:
        return BAD_UNDERSTANDING
    elif x >= 0.33 and x <= 0.66:
        return MIXED_UNDERSTANDING
    else:
        return GOOD_UNDERSTANDING

