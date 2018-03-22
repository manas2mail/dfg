# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 22:15:38 2018

@author: 703106491
"""

# information-extraction.py

import re

import nltk

from nltk.corpus import stopwords

stop = stopwords.words('english')



string = """

Hey,



This week has been crazy. Attached is my report on IBM. Can you give it a quick read and provide some feedback.



Also, make sure you reach out to Claire (claire@xyz.com).



You're the best.





Cheers,


pin-
George W.
9836492392
212-555-1234

"""



def extract_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    return [re.sub(r'\D', '', number) for number in phone_numbers]



def extract_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)



def ie_preprocess(document):
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences



def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names


def fnExtractAll(string):
    numbers = extract_phone_numbers(string)
    emails = extract_email_addresses(string)
    names = extract_names(string)    
    
#    numbers =  ';'.join(extract_phone_numbers(string))
#    emails =';'.join(extract_email_addresses(string))
#    names =';'.join(extract_names(string) )    
    return numbers, emails, names



import pandas as pd
import numpy as np

if __name__ == '__main__':    
    numbers, emails, names= fnExtractAll(string)
    A1={'ORGANIZATION': 'BLUE SOLUTION Consulting GroupIL', 'PERSON': 'James Green Manager', 'LOCATION': '1010 Spring AveChicago'}    
#    B1 = "{'PHONE' : '" + numbers + "', 'E-mails' : '" + emails + "', '2nd option names' : '" + names + "'}"
    
    df1 = pd.DataFrame(list(A1.items()), columns=['Entity', 'Value'])    
    dic = dict( PHONE = numbers, EMAILS = emails, NAMES= names)
    df2 = pd.DataFrame(list(dic.items()), columns=['Entity', 'Value'])            

    df=df1.append(df2)
    
    print(df)


  
#    print(A)
#    print("------------------------------------------")
#    print(B1)
    
    
    
#    A = Counter(	)
##    B = Counter(strS)
#    A.update(B)
#    print(A)
    
    
#    numbers, emails, names= fnExtractAll(string)
#    
#    lng="ddfdf - "
#    
#    strS= "{{ph- "   + numbers + ";  emails- "  + emails + ";  2nd option names-" + names
#    lng+=strS
#    
##    lng = str(lng) 
#    print(lng)
    
#    print("numbers- ", numbers)
#    print("emails-  " , emails)
#    print("names-",names)
    
    
    
    
    
    
    
    
    