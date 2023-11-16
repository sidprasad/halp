import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
import json
from enum import Enum


nltk.download('punkt')
nltk.download('stopwords')


def rough_num_words(s):
    return s.count(" ") + 1

# Retrieves hardcoded policy
def get_hardcoded_policy():
    return '''Gradescope collects the following types of data and shares them with the corresponding entities:
- Personal information: This may include names, email addresses, and other identifying details provided by users. It is shared with Gradescope's internal team, employees, and authorized service providers who need access to the information to perform their duties and improve the service. For example, the internal team may use personal information to verify user identities, provide customer support, and communicate important updates. Authorized service providers may include hosting providers, data storage providers, and analytics platforms who assist Gradescope in delivering and improving the service.
- Usage data: This includes information about how users interact with the platform, such as the courses they enroll in, assignments they submit, and grades they receive. It is shared with Gradescope's internal team, employees, and authorized service providers who analyze the data to enhance the platform's features and functionality. This analysis helps Gradescope understand user preferences, identify areas for improvement, and make data-driven decisions to provide a better user experience. The internal team may also use usage data to monitor system performance, troubleshoot issues, and ensure the proper functioning of the platform.

Gradescope takes appropriate measures to safeguard the collected data and respects user privacy in accordance with its privacy policy. These measures include implementing technical and organizational security measures to protect against unauthorized access, maintaining strict data confidentiality obligations for employees and service providers, and regularly monitoring and updating security practices to align with industry standards. It is important for users to review and understand the privacy policy to be aware of their rights and choices regarding their data.
Gradescope does not sell or share personal information with third parties for marketing purposes. The collected data is used solely for the purposes stated in the privacy policy and to provide and improve the Gradescope service. Users can trust that their data is handled with care and in compliance with applicable laws and regulations.'''





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

    # Check if the request was successful
    if response.status_code == 200:
        return response.text
        # Parse the HTML content of the page using BeautifulSoup

    else:
        print("Failed to retrieve the webpage. Status code:", response.status_code)
        return ""
    


def try_parse_json_answer(json_string):
    try:
        return json.loads(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {'Answer' : "Something went wrong", 'Confidence' : 0}



def try_parse_json_question(json_string):
    try:
        return json.loads(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {'Question' : "Something went wrong" }


def try_parse_json_answercheck(json_string):
    try:
        return json.loads(json_string)
    except Exception as e:
        print(json_string)
        print(e)
        return {
                'Correct' : False,
                'Explanation' : "Something went wrong",
            }
    

