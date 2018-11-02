#importing libraries
import bs4 as bs
from bs4 import BeautifulSoup
import urllib.request
import re
import nltk
import heapq
from nltk import sent_tokenize
#nltk.download('stopwords')
#nltk.download('punkt')


# Getting the data
source = urllib.request.urlopen('https://en.wikipedia.org/wiki/Wings_of_Fire').read()

# Getting the html page
soup = BeautifulSoup(source, 'lxml')

# Getting the text out of the <p> tag in html document
text = ""
for paragraph in soup.find_all('p'):
    text += paragraph.text
    
# Preprocessing the text
text = re.sub(r"\[[0-9]*\]"," ",text)
text = re.sub(r"\s+"," " ,text)
clean_text = text.lower()
clean_text = re.sub(r'\W' , ' ', clean_text)
clean_text = re.sub(r'\d' , ' ', clean_text)
clean_text = re.sub(r'\s+', ' ', clean_text)

# Forming sentences from the article
sentences = nltk.sent_tokenize(text)

# list of stop words
stop_words = nltk.corpus.stopwords.words('english')

# Basic Histogram
word2count = {}
for word in nltk.word_tokenize(clean_text):
    if word not in stop_words:
        if word not in word2count.keys():
            word2count[word] = 1
        else:
            word2count[word] += 1
            
# Weighted histogram
for key in word2count.keys():
    word2count[key] = word2count[key]/max(word2count.values())


# Finding out scores for the different sentences
sent2score = {}
for sentence in sentences:
    for word in nltk.word_tokenize(sentence.lower()):
        if word in word2count.keys():
            if len(sentence.split(' '))<30:
                if sentence not in sent2score.keys():
                    sent2score[sentence] = word2count[word]
                else:
                    sent2score[sentence] += word2count[word]
                    
                    
# Printing the summary
best_sentences = heapq.nlargest(5,sent2score,key=sent2score.get)                 
print('_____________________________')
for sentence in best_sentences:
    print(sentence)

