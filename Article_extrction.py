import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob import TextBlob
import nltk
from nltk.corpus import cmudict


# Firstly we will extract the article from the text


# Input file reading 
input_df = pd.read_excel('F:\\internshup_blackcoffer\\Input (1).xlsx')

def extract_text_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.find('h1').get_text()
    paragraphs = soup.find_all('p')
    article_text = ' '.join([para.get_text() for para in paragraphs])
    return title, article_text

# we will iterate through url and extract the text 

for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    title, article_text = extract_text_from_url(url)
    with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
        file.write(title + '\n' + article_text)


# Downloading the nltk data 

nltk.download('punkt')
nltk.download('cmudict')


d = cmudict.dict()

def syllable_count(word):
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0] if word.lower() in d else 1

def analyze_text(article_text):
    blob = TextBlob(article_text)
    sentences = blob.sentences
    words = blob.words
    
# Variables
    
    positive_score = sum(1 for word in words if TextBlob(word).sentiment.polarity > 0)
    negative_score = sum(1 for word in words if TextBlob(word).sentiment.polarity < 0)
    polarity_score = blob.sentiment.polarity
    subjectivity_score = blob.sentiment.subjectivity
    avg_sentence_length = len(words) / len(sentences)
    complex_word_count = sum(1 for word in words if syllable_count(word) >= 3)
    percentage_complex_words = complex_word_count / len(words) * 100
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    avg_words_per_sentence = len(words) / len(sentences)
    word_count = len(words)
    syllables_per_word = sum(syllable_count(word) for word in words) / len(words)
    personal_pronouns = sum(1 for word in words if word.lower() in ["i", "we", "my", "ours", "us"])
    avg_word_length = sum(len(word) for word in words) / len(words)
    
    return [positive_score, negative_score, polarity_score, subjectivity_score, avg_sentence_length, 
            percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, word_count, 
            syllables_per_word, personal_pronouns, avg_word_length]

# Analyze the extracted text files

output_data = []
for index, row in input_df.iterrows():
    url_id = row['URL_ID']
    with open(f'{url_id}.txt', 'r', encoding='utf-8') as file:
        title = file.readline().strip()
        article_text = file.read().strip()
        analysis_results = analyze_text(article_text)
        output_data.append([url_id, row['URL'], title] + analysis_results)

# Save the output data

output_df = pd.DataFrame(output_data, columns=[
    'URL_ID', 'URL', 'Title', 'Positive Score', 'Negative Score', 'Polarity Score', 'Subjectivity Score',
    'Avg Sentence Length', 'Percentage Complex Words', 'Fog Index', 'Avg Words per Sentence', 
    'Complex Word Count', 'Word Count', 'Syllables per Word', 'Personal Pronouns', 'Avg Word Length'
])
output_df.to_excel('Output Data Structure.xlsx', index=False)









