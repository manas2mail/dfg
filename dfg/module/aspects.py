
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 27 22:17:43 2018

@author: 703106491
http://nlpforhackers.io/wordnet-sentence-similarity/
https://nycdatascience.com/blog/student-works/scraping-tripadvisor-airlines-customer-reviews/

"""
from time import time
start_time = time()


from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
from nltk import sent_tokenize
import _pickle as cPickle
import os.path as path 
import pandas as pd

def penn_to_wn(tag):
#    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None

def sentence_similarity(sentence1, sentence2):
#    """ compute the sentence similarity using Wordnet """
#     Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
    
    for syn1 in synsets1:
        arr_simi_score = []        
        for syn2 in synsets2:
            simi_score = syn1.wup_similarity(syn2)
            if simi_score is not None:
                arr_simi_score.append(simi_score)
                if(len(arr_simi_score) > 0):
                    best = max(arr_simi_score)   
                    if best > 0.99:
                        score += best
                        count += 1                
                
    # Average the values   
    if score> 0.1:  score /= (count+0.1)      
    return score


def fnStr2List(column,df):
    df1=df[column]
    df1 = df1.dropna()
    return column + ' '.join(word for word in df1)
    
def clean_document(document):
    """Cleans document by removing unnecessary punctuation. It also removes
    any extra periods and merges acronyms to prevent the tokenizer from
    splitting a false sentence
    """
    # and some punctuation
    document = document.replace('...', '')
    document = document.replace('.', '. ')

    # Remove extra whitespace
    document = ' '.join(document.split())
    return document


def sentence_similarity_main(focus_sentences,sentences,top_n):          
    focus_sentences=clean_document(focus_sentences)
    focus_sentences=sent_tokenize(focus_sentences)
       
    A=[]
    B=[]
#    C=[]  
    pd.options.html.border=0    
    for focus_sentence in focus_sentences:        
        if len(focus_sentence) > 5:
            similarity_scores = [(focus_sentence, sentence[:sentence.index(' ') + 1], sentence_similarity(focus_sentence, sentence)) for sentence in sentences if sentence_similarity(focus_sentence, sentence)> 0.89]
            sorted_by_second = sorted(similarity_scores, key=lambda x: x[-1], reverse=True) 
            for sent, aspct,score in sorted_by_second[:top_n]:        
                A.append(sent)
                B.append(aspct)
                      
    asptdf=pd.DataFrame(A,columns=['Sentence'])
    asptdf['Aspects']=B
#    asptdf['Score']=C  
    return asptdf  #sorted_by_second[:top_n]
   
def fnFilePath(filename):    
    cur_dir = path.dirname(__file__)
    cur_dir = path.abspath(cur_dir+ "/../")  
    parent_dir=path.join(cur_dir,r'module\data\act' )            
    filepath=path.join(parent_dir,filename )     
    
    return filepath
            

def fnGetData(hotel_loc): 
#    filepath=fnFilePath("hotel.csv")    
    filepath=fnFilePath(hotel_loc)    #Changed March 20 2018
    flrvw = pd.read_csv(filepath, encoding ="ISO-8859-1",index_col=False)      #nrows=899999,
    return flrvw


def fnGetModel(X):        
    # load it again
    filepath=fnFilePath("TfIDf.pkl")  
    with open(filepath, 'rb') as fid:
        TfIDf_vec = cPickle.load(fid)
    
    loaded_vec = TfIDf_vec
    tfidf_transformer =loaded_vec.transform(X)
    
 
    # load it again
    filepath=fnFilePath("LRg.pkl")  
    with open(filepath, 'rb') as fid:
        LRg_model = cPickle.load(fid)
    
  
    LRgPd=LRg_model.predict(tfidf_transformer)

    return LRgPd


def fnMain_ACT(hotel_loc):    
    filepath=fnFilePath("Aspect.csv")
    df = pd.read_csv(filepath)  #Aspect List    
    sentences=[fnStr2List(column,df)  for column in df]  
        
    flrvw=fnGetData(hotel_loc)      
    X = flrvw['Review'].astype('U') #raw text

    top_n=4
    asptdf = pd.DataFrame()
    
    print("Data upload")
    
    i=0
    for focus_sentences in X[:100]:    
        df1=sentence_similarity_main(focus_sentences,sentences,top_n)     
        asptdf=asptdf.append(df1, ignore_index=True)
        i+=1
        print(i)
        
        
    print("Data Aspect")
    
    # Predict Sentiment 
    X = asptdf['Sentence'].astype('U') #raw text
    LRgPd=fnGetModel(X)     #[list]
    
    #Combine
    asptdf['Polarity'] = LRgPd
    
#    df=asptdf[['Aspects','Polarity']]
    
    print("Data Classi")
    
    
    return asptdf


    

#asptdf=fnMain_ACT("Four Seasons Hotel.csv")    
#print(asptdf)   
#print("---processing time: %s seconds ---" % (time() - start_time)) 
# 
#    






















    
    
    
    
    
    
    
    