from utilities import DataKind, DataProcessor
import random



class DataKind(Enum):
    ASSIGNMENT_SUBMISSIONS = 1
    PERSONAL_INFORMATION = 2
    INTERACTION_DATA = 3
    OTHER = 4
    
    def __str__(self):
        if self == DataKind.OTHER:
            return "the collection, ownership or sharing of data"
        return self.name.title().replace("_", " ")
    


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
    ## Modelling the assignment submission system for CS19 for now
    student_understanding = cs19_understanding()
    
    
    target_level = student_understanding[data_kind][data_processor]
    weights = { GOOD_UNDERSTANDING : 0.1, BAD_UNDERSTANDING : 0.1, MIXED_UNDERSTANDING : 0.1}
    weights[target_level] = 0.8

    levels = list(weights.keys())
    level_weights = list(weights.values())
    return random.choices(levels, weights = level_weights)[0]

    

BAD_UNDERSTANDING = 1 ## Level 1 if its an area where students do not know what is going on.
MIXED_UNDERSTANDING = 2 ## Level 2 if its an area where student understanding is mixed, or the scenario is a little complicated.
GOOD_UNDERSTANDING = 3 ## Level 3 if it is an area where students have a good understanding of the topic.

def cs19_understanding():
    target_levels = []    
    target_levels[DataKind.ASSIGNMENT_SUBMISSIONS][ DataProcessor.OTHER_STUDENTS] = MIXED_UNDERSTANDING
    target_levels[DataKind.ASSIGNMENT_SUBMISSIONS][ DataProcessor.COURSE_INSTRUCTOR] = GOOD_UNDERSTANDING
    target_levels[DataKind.ASSIGNMENT_SUBMISSIONS][ DataProcessor.COURSE_TAS] = GOOD_UNDERSTANDING
    target_levels[DataKind.ASSIGNMENT_SUBMISSIONS][ DataProcessor.EDUCATION_RESEARCHERS] = BAD_UNDERSTANDING
    target_levels[DataKind.ASSIGNMENT_SUBMISSIONS][ DataProcessor.THIRD_PARTY_CORPORATIONS] = BAD_UNDERSTANDING
    target_levels[DataKind.PERSONAL_INFORMATION][ DataProcessor.OTHER_STUDENTS] = GOOD_UNDERSTANDING ## THis one is complicated
    target_levels[DataKind.PERSONAL_INFORMATION][ DataProcessor.COURSE_INSTRUCTOR] = GOOD_UNDERSTANDING
    target_levels[DataKind.PERSONAL_INFORMATION][ DataProcessor.COURSE_TAS] = BAD_UNDERSTANDING
    target_levels[DataKind.PERSONAL_INFORMATION][ DataProcessor.EDUCATION_RESEARCHERS] = GOOD_UNDERSTANDING
    target_levels[DataKind.PERSONAL_INFORMATION][ DataProcessor.THIRD_PARTY_CORPORATIONS] = BAD_UNDERSTANDING
    target_levels[DataKind.INTERACTION_DATA][ DataProcessor.OTHER_STUDENTS] = GOOD_UNDERSTANDING
    target_levels[DataKind.INTERACTION_DATA][ DataProcessor.COURSE_INSTRUCTOR] = BAD_UNDERSTANDING
    target_levels[DataKind.INTERACTION_DATA][ DataProcessor.COURSE_TAS] = GOOD_UNDERSTANDING
    target_levels[DataKind.INTERACTION_DATA][ DataProcessor.EDUCATION_RESEARCHERS] = GOOD_UNDERSTANDING
    target_levels[DataKind.INTERACTION_DATA][ DataProcessor.THIRD_PARTY_CORPORATIONS] = MIXED_UNDERSTANDING

    ## These are not well defined, to add some interestingness to the questions.
    target_levels[DataKind.OTHER][ DataProcessor.OTHER_STUDENTS] = random.randint(1,3)
    target_levels[DataKind.OTHER][ DataProcessor.COURSE_INSTRUCTOR] = random.randint(1,3)
    target_levels[DataKind.OTHER][ DataProcessor.COURSE_TAS] = random.randint(1,3)
    target_levels[DataKind.OTHER][ DataProcessor.EDUCATION_RESEARCHERS] = random.randint(1,3)
    target_levels[DataKind.OTHER][ DataProcessor.THIRD_PARTY_CORPORATIONS] = random.randint(1,3)

    
    return target_levels
