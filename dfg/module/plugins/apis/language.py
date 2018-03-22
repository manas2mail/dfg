# -*- coding: utf-8 -*-
import requests


def extract_entities(text, access_token=None):

    url = 'https://language.googleapis.com/v1beta1/documents:analyzeEntities?key={}'.format('AIzaSyBOsF8iV_3gfR--4U2kkM0gDHo0WvhPSxI')
    header = {'Content-Type': 'application/json'}
    body = {
        "document": {
            "type": "PLAIN_TEXT",
            "language": "EN",
            "content": text
        },
        "encodingType": "UTF8"
    }
    response = requests.post(url, headers=header, json=body).json()
    return response


def extract_required_entities(text, access_token=None):
    entities = extract_entities(text, 'AIzaSyBOsF8iV_3gfR--4U2kkM0gDHo0WvhPSxI')
    required_entities = {'ORGANIZATION': '', 'PERSON': '', 'LOCATION': ''}   #, 'PHONE': ''
    for entity in entities['entities']:
        t = entity['type']
        if t in required_entities:
            required_entities[t] += entity['name']

    return required_entities


#import os
#from apis.config_loader import loader
#import six
#    
#def fnMain1(text):
#    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))  
#    if isinstance(text, six.binary_type):
#        text = text.decode('utf-8') 
#    entities = extract_required_entities(text, google_token['token'])
#    return entities 
#
#text='PM Modis delicate balancing act of rolpolitical power contact phone:-+91-9836492392'
#print(fnMain1(text))