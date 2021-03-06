# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:22:57 2017

@author: 703106491
http://www.johnwittenauer.net/language-exploration-using-vector-space-models/

"""
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from textblob import TextBlob as tb
import urllib.request
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import numpy as np
import ExtractMsg
import nltk
import glob
import re
from newspaper import Article
from os import path

stop = stopwords.words('english')
# Noun Part of Speech Tags used by NLTK
# More can be found here
# http://www.winwaed.com/blog/2011/11/08/part-of-speech-tags/
NOUNS = ['NN', 'NNS', 'NNP', 'NNPS']

def clean_document(document):
    """Cleans document by removing unnecessary punctuation. It also removes
    any extra periods and merges acronyms to prevent the tokenizer from
    splitting a false sentence
    """
    # Remove all characters outside of Alpha Numeric
    # and some punctuation
    document = re.sub('[^A-Za-z .-]+', ' ', document)
    document = document.replace('-', '')
    document = document.replace('...', '')
    document = document.replace('Mr.', 'Mr').replace('Mrs.', 'Mrs')

    # Remove Ancronymns M.I.T. -> MIT
    # to help with sentence tokenizing
    document = merge_acronyms(document)

    # Remove extra whitespace
    document = ' '.join(document.split())
    return document

def remove_stop_words(document):
    """Returns document without stop words"""
    document = ' '.join([i for i in document.split() if i not in stop])
    return document

def merge_acronyms(s):
    """Merges all acronyms in a given sentence. For example M.I.T -> MIT"""
    r = re.compile(r'(?:(?<=\.|\s)[A-Z]\.)+')
    acronyms = r.findall(s)
    for a in acronyms:
        s = s.replace(a, a.replace('.',''))
    return s

def link_text(url): 
    title=""
    txt=""
    article=Article(url)
    article.download()
    try:
        article.parse()
        article.nlp()
        txt=article.text  
        title=article.title 
#        smry=article.summary
    except :
        pass    
    return title,txt




def doc_list(): 
    bloblist = []
    d = path.dirname(__file__)
    parent_dir = path.abspath(d + "/../")  
    path1=path.join(parent_dir,r'module\db\New\*.msg' )
    files = glob.glob(path1)
    for file in files:          #files[:10]:
        msg = ExtractMsg.Message(file)
        txt=msg.body
        bloblist.append(tb(txt))
    return bloblist

def similarity_score(t, s):
    """Returns a similarity score for a given sentence.
    similarity score = the total number of tokens in a sentence that exits
                        within the title / total words in title
    """
    t = remove_stop_words(t.lower())
    s = remove_stop_words(s.lower())
    t_tokens, s_tokens = t.split(), s.split()
    similar = [w for w in s_tokens if w in t_tokens]
    score = (len(similar) * 0.1 ) / len(t_tokens)
    return score

    
def rank_sentences(doc, title, doc_matrix, feature_names, top_n=10):
    """Returns top_n sentences. Theses sentences are then used as summary
    of document.
    input
    ------------
    doc : a document as type str
    doc_matrix : a dense tf-idf matrix calculated with Scikits TfidfTransformer
    feature_names : a list of all features, the index is used to look up
                    tf-idf scores in the doc_matrix
    top_n : number of sentences to return
    """
    sents = nltk.sent_tokenize(doc)
    sentences = [nltk.word_tokenize(sent) for sent in sents]
    sentences = [[w for w in sent if nltk.pos_tag([w])[0][1] in NOUNS]
                  for sent in sentences]
    

    top_n=min(int(len(sentences)/1.5),22)  
    top_n=max(int(len(sentences)/1.5),6)  

    
    tfidf_sent = [[doc_matrix[feature_names.index(w.lower())]
                   for w in sent if w.lower() in feature_names]
                 for sent in sentences]

    # Calculate Sentence Values
    doc_val = sum(doc_matrix)
    sent_values = [sum(sent) / doc_val for sent in tfidf_sent]

    # Apply Similariy Score Weightings
    if len(title) > 0 : 
        similarity_scores = [similarity_score(title, sent) for sent in sents]        
        scored_sents = np.array(sent_values) + np.array(similarity_scores)    
        sent_values=scored_sents
    
    # Apply Position Weights
    ranked_sents = [sent*(i/len(sent_values))
                    for i, sent in enumerate(sent_values)]
    
    ranked_sents = [pair for pair in zip(range(len(sent_values)), sent_values)]
    ranked_sents = sorted(ranked_sents, key=lambda x: x[1] *-1)

    
    return ranked_sents[:top_n]


    
def fnMainModel(title, document):
    summary="No Data Found"
    # Load corpus data used to train the TF-IDF Transformer
    data = doc_list()
    
    # Load the document you wish to summarize
#    title, document = link_text(url)  
    
    cleaned_document = clean_document(document)
    doc = remove_stop_words(cleaned_document)

    cleaned_document = ' '.join(document.strip().split('\n'))
    
    if len(document) > 20:    
        # Merge corpus data and new document data
        data = [' '.join(document) for document in data]
        train_data = set(data + [doc])
        
        # Fit and Transform the term frequencies into a vector
        count_vect = CountVectorizer()
        count_vect = count_vect.fit(train_data)
        
        freq_term_matrix = count_vect.transform(train_data)
        feature_names = count_vect.get_feature_names()
        
        # Fit and Transform the TfidfTransformer
        tfidf = TfidfTransformer(norm="l2")
        tfidf.fit(freq_term_matrix)
        
        # Get the dense tf-idf matrix for the document
        story_freq_term_matrix = count_vect.transform([doc])
        story_tfidf_matrix = tfidf.transform(story_freq_term_matrix)
        story_dense = story_tfidf_matrix.todense()
        doc_matrix = story_dense.tolist()[0]
        
        # Get Top Ranking Sentences and join them as a summary
        top_sents = rank_sentences(document,title, doc_matrix, feature_names)
        summary = '.'.join([cleaned_document.split('.')[i]
                            for i in [pair[0] for pair in top_sents]])
        summary = ' '.join(summary.split())
#        print(summary)
#        summary = (sum([pair[1] for pair in top_sents]))
    return summary
    


# 
#if __name__ == '__main__':
##    
###    url='https://www.tradearabia.com/news/OGN_327225.html'
#    url='http://www.miningweekly.com/article/bluejay-focuses-on-starting-pituffik-operations-next-year-2017-04-21/searchString:ilmenite'  
#    title, document = link_text(url)  
##    
#    summary=fnMainModel(title, document)
#    print(summary)
#
##    summary=fnMainModel(url)

   
    
    
    
    