import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
import json
import nltk
import re

try:
    nltk.data.find('punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('stopwords')
except LookupError:
    nltk.download('stopwords')

def rough_num_words(s):
    return s.count(" ") + 1


# VERY BASIC, from https://www.geeksforgeeks.org/python-text-summarizer/
def summarizer(text):
    
    # Tokenizing the text 
    stopWords = set(stopwords.words("english")) 
    words = word_tokenize(text) 
    
    # Creating a frequency table to keep the score of each word 
    
    freqTable = dict() 
    for word in words: 
        word = word.lower() 
        if word in stopWords: 
            continue
        if word in freqTable: 
            freqTable[word] += 1
        else: 
            freqTable[word] = 1
    
    # Creating a dictionary to keep the score of each sentence 
    sentences = sent_tokenize(text) 
    sentenceValue = dict() 
    
    for sentence in sentences: 
        for word, freq in freqTable.items(): 
            if word in sentence.lower(): 
                if sentence in sentenceValue: 
                    sentenceValue[sentence] += freq 
                else: 
                    sentenceValue[sentence] = freq 
    
    sumValues = 0
    for sentence in sentenceValue: 
        sumValues += sentenceValue[sentence] 
    
    # Average value of a sentence from the original text 
    
    average = int(sumValues / len(sentenceValue)) 
    
    # Storing sentences into our summary. 
    summary = '' 
    for sentence in sentences: 
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * average)): 
            summary += " " + sentence 
    return summary

        
def get_policy_from_web(url, summarize_if_needed = True):
    text_with_html = get_policy_from_web_html(url)
    soup = BeautifulSoup(text_with_html, 'html.parser')
    plaintext_policy = soup.get_text()

    # This is a hack I need to figure out!!
    c = 0
    while summarize_if_needed and rough_num_words(plaintext_policy) > 3000 and c < 3:
        c += 1
        plaintext_policy = summarizer(plaintext_policy)

    return plaintext_policy

    
def get_policy_from_web_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return ""

def try_parse_json_answer(json_string):
    try:
        return load_string(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {'Answer' : "Something went wrong", 'Confidence' : 0}

def try_parse_json_question(json_string):
    try:
        return load_string(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {'Question' : "Something went wrong" }


def try_parse_json_answercheck(json_string):
    try:
        return load_string(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {
                'Correct' : False,
                'AltAnswer' : "Something went wrong",
            }

def load_string(json_string):
    # Check if ",}" is present in the json_string
    if re.search(r',\s*}', json_string):
        json_string = re.sub(r',\s*}', '}', json_string)
    return json.loads(json_string)