import pandas as pd
import numpy as np
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import re, string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer  
from gensim import corpora, models
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity  
from wordcloud import WordCloud, STOPWORDS
from os import path

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()
stopwords=stopwords.words('english')
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    

def fnImpLDA():    
    url=r"D:\dfg\dfg\module\data\final.csv"   
    data= pd.read_csv(url)
    df= pd.DataFrame(data)
    
    tweets_texts = df["Text"].tolist()    
    return df, tweets_texts

def LDA_model():
    df, tweets_texts=fnImpLDA()
    words = []
    for tw in tweets_texts:
        words += process_tweet_text(tw)
    
    wrds=' '.join(words)
    
    cleaned_tweets = []
    for tw in tweets_texts:
        words = process_tweet_text(tw)
        cleaned_tweet = " ".join(w for w in words if len(w) > 2 and 
    w.isalpha()) #Form sentences of processed words
        cleaned_tweets.append(cleaned_tweet)
    df['CleanTweetText'] = cleaned_tweets

    texts = [text for text in cleaned_tweets if len(text) > 2]
    doc_clean = [clean(doc).split() for doc in texts]
    dict = corpora.Dictionary(doc_clean)
    doc_term_matrix = [dict.doc2bow(doc) for doc in doc_clean]
    
    ldamodel = models.ldamodel.LdaModel(doc_term_matrix, num_topics=6, id2word = dict, passes=5)
#    print(ldamodel)
#    c=""
    list=[]
    for topic in ldamodel.show_topics(num_topics=6, formatted=False, num_words=10):
        a="Topic {}: Words: ".format(topic[0])
#        print("Topic {}: Words: ".format(topic[0]))
        topicwords = [w for (w, val) in topic[1]]
        b=topicwords
        
        list.append([str(a),str(b)])
        
#        c+=  str(a) + '\n' + str(b) + '\n\n'       

    df1=pd.DataFrame(list,columns=['Topics','Words'])   
    
    return  wrds, df1      

   


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


def fnCreate_WordCloud(i,text):
    if len(text)>5:
        stopwords = set(STOPWORDS)
        stopwords.add("said")
        
        d = path.dirname(__file__)
        parent_dir = path.abspath(d + "/../")  
        d=path.join(parent_dir,r'nlp\static\images\img' )
    
    
        # lower max_font_size        
        wordcloud = WordCloud(background_color="white", max_font_size=40, stopwords=stopwords).generate(text)
        #change the color setting
#        wordcloud.recolor(color_func = grey_color_func)
    
        ## The pil way (if you don't have matplotlib)
        image = wordcloud.to_image()
    
        # store default colored image
        filename=  str(i) + '.png'
        image.save( path.join(d, filename), "PNG" )
        

#words, df =LDA_model()
#print(df)
#fnCreate_WordCloud(1,words)






























