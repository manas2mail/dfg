# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 12:41:49 2018

@author: 703106491
"""

from nltk.stem.wordnet import WordNetLemmatizer 
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import TweetTokenizer
from gensim import corpora, models
from nltk.corpus import stopwords
from collections import Counter
import pandas as pd
from os import path
import re, string
import nltk 


stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
stopwords=stopwords.words('english')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())


def process_tweet_text(tweet):
    if tweet.startswith('@null'):
        return "[Tweet not available]"
    tweet = re.sub(r'\$\w*','',tweet) # Remove tickers
    tweet = re.sub(r'https?:\/\/.*\/\w*','',tweet) # Remove hyperlinks
    tweet = re.sub(r'['+string.punctuation+']+', ' ',tweet) # Remove puncutations
    twtok = TweetTokenizer(strip_handles=True, reduce_len=True)
    tokens = twtok.tokenize(tweet)
    tokens = [i.lower() for i in tokens if i not in stopwords and len(i) > 2 and  
                                             i in english_vocab]
    return tokens

def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized


#print(dictionary)
def LDA_model(df,tweets_texts):
#    df,tweets_texts=getText(df)
    words = []   
    for tw in tweets_texts:
        words += process_tweet_text(tw)
    
#    wrds=' '.join(words)
    wrds=words
    
    cleaned_tweets = []
    for tw in tweets_texts:
        words = process_tweet_text(tw)
        cleaned_tweet = " ".join(w for w in words if len(w) > 2 and 
    w.isalpha()) #Form sentences of processed words
        cleaned_tweets.append(cleaned_tweet)
    df['CleanTweetText'] = cleaned_tweets

    texts = [text for text in cleaned_tweets if len(text) > 2]
    doc_clean = [clean(doc).split() for doc in texts]
    dictionary  = corpora.Dictionary(doc_clean)
    
    # Filter terms which occurs in less than 4 articles & more than 40% of the articles
    dictionary.filter_extremes(no_below=4, no_above=0.4)
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    
    ldamodel = models.ldamodel.LdaModel(doc_term_matrix, num_topics=10, id2word = dictionary, passes=50, iterations=500)
#    print(ldamodel)
  
#    ldamodel.save('lda.model')
    
    list=[]
    for topic in ldamodel.show_topics(num_topics=6, formatted=False, num_words=10):
        a="Topic {}: Words: ".format(topic[0])
#        print("Topic {}: Words: ".format(topic[0]))
        topicwords = [w for (w, val) in topic[1]]
        b=topicwords        
        list.append([str(a),str(b)])

    df1=pd.DataFrame(list,columns=['Topics','Words'])       
    return  wrds, df1      



def fnCreate_WordCloud(i,text):
    if len(text)>5:
        stopwords = set(STOPWORDS)
        stopwords.add("said")
        
        d = path.dirname(__file__)
        parent_dir = path.abspath(d + "/../")  
        d=path.join(parent_dir,r'nlp\static\images\img' )
    
        # lower max_font_size        
        wordcloud = WordCloud(background_color="white", max_font_size=45, stopwords=stopwords).generate(text)
    
        ## The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
    
        # store default colored image
        filename=  str(i) + '.png'
        image.save( path.join(d, filename), "PNG" )
    
    
def fnWord_Freq(words, top_n):  
    counts = Counter(words)
    my_list=pd.DataFrame(list(counts.items()), columns=['word', 'freq'])       
    return my_list.sort_values('freq',ascending=False)[:top_n]







#def fnChart_ACT(): 
#    pd.options.html.border=1
#        
##    df=fnMain_ACT()     
#    df =pd.read_csv('ACT.csv')   #, delimiter='\t', index_col=0)
#    
#        
#    df1= pd.DataFrame(df, columns = ['Aspects', 'Polarity'])      
#    df1['Polarity'] = np.where(df1['Polarity']>0, '+ve', '-ve')
#    df_grouped=df1.groupby(['Aspects','Polarity'])['Polarity'].count().reset_index(name='Count') #.reset_index() 
#    
#    
#    #------------------All Aspect Chart ------------------
#  
#    
#     #    ----New ---# We print percentages:  +ve --------   
#    dfp=df_grouped[df_grouped['Polarity']== "+ve"]
#    df2= pd.DataFrame(dfp, columns = ['Aspects', 'Count'])  
#     
#         
#    #    ----- -ve -----------    
#    dfn=df_grouped[df_grouped['Polarity']== "-ve"]
#    df2= pd.DataFrame(dfn, columns = ['Aspects', 'Count'])  
#   
#    
#   #    script1, div1=fnCreate_Stacked_Bar(df2) 
##    #------------------end All Aspect Chart ------------------
##    
##    
##    
##    #---------------- start All topics & Word Chart----------------    
#    texts= df["Sentence"].tolist()    
#    words, df_lda =LDA_model(df,texts)
#    
#    wrds=' '.join(words)
#    fnCreate_WordCloud(2,wrds)
#    htm="<img src=/static/images/img/2.png>"
#    
#    
#    df_wf=fnWord_Freq(words,10)
#
##    #----------------end All topics & Word Chart---------------- 
#
#
#    #--------------- +Ve charts --------------- 
#    dfp=df[df['Polarity']== 1]
#    textsp= dfp["Sentence"].tolist()    
#    wordsp, df_ldap =LDA_model(dfp,textsp)
#    
#    
#    wrdsp=' '.join(wordsp)
#    fnCreate_WordCloud(3,wrdsp)
#  
#    
#    df_wfp=fnWord_Freq(wordsp,10)
#   
#    #--------------- +Ve charts --------------- 
#    
#    
#    
#    #--------------- -Ve charts --------------- 
#    dfn=df[df['Polarity']== 0]
#    textsn= dfn["Sentence"].tolist()    
#    wordsn, df_ldan =LDA_model(dfn,textsn)
#    
#    
#    wrdsn=' '.join(wordsn)
#    fnCreate_WordCloud(4,wrdsn)
#
#    
#    df_wfn=fnWord_Freq(wordsn,10)
# 
#    #--------------- -Ve charts --------------- 
# 
#    
#    #--------------- Some Snapshot Data ---------------     
#    
#    df_smpl=df.loc[24:40]
#    df_smpl= pd.DataFrame(df_smpl, columns = ['Sentence', 'Aspects', 'Polarity']) 
#    


#def getText(df):
#    tweets_texts = df["Review"].tolist()
#    return tweets_texts
   

#def fnFilePath(filename):    
#    cur_dir = path.dirname(__file__)
#    cur_dir = path.abspath(cur_dir+ "/../")  
#    parent_dir=path.join(cur_dir,r'module\data\act' )            
#    filepath=path.join(parent_dir,filename )     
#    
#    return filepath
#
#
#def fnGetData(): 
#    filepath=fnFilePath("hotel.csv")
#    flrvw = pd.read_csv(filepath, encoding ="ISO-8859-1",index_col=False)      #nrows=899999,
#    return flrvw
#    
 
    





#df=fnGetData()
#
#texts= df["Review"].tolist()
#
#words, df1 =LDA_model(df,texts)
#print(df1)
#
#df2=fnWord_Freq(words,20)
#print(df2)
#
#wrds=' '.join(words)
#fnCreate_WordCloud(1,wrds)




































