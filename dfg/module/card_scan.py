# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 00:44:04 2017

@author: 703106491
"""

# -*- coding: utf-8 -*-
import argparse
import os
import sys
import goslate
sys.path.append('..')
gs = goslate.Goslate()

from module.plugins.apis.vision import detect_text
from module.plugins.apis.config_loader import loader
from module.plugins.apis.language import extract_required_entities
    
def fnMain(path):
    text=""    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))    
    text = detect_text(path, google_token['token'])  
    language_id = gs.detect(text)    
    txt=gs.translate(text, language_id)    
    return txt    

    
def fnMain1(text):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))    
    entities = extract_required_entities(text, google_token['token'])
    return entities   






#if __name__ == '__main__':
#    path=r"D:\WebServer\webapp\module\plugins\tests\data\example_en.png"
#    print(fnMain1('TraducciÃ³n de Actas y Documentos'))
#    
#    
#    


#import base64
#import requests
#
#
#def detect_text(image_file, access_token=None):
#
#    with open(image_file, 'rb') as image:
#        base64_image = base64.b64encode(image.read()).decode()
#
#    url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(access_token)
#    header = {'Content-Type': 'application/json'}
#    body = {
#        'requests': [{
#            'image': {
#                'content': base64_image,
#            },
#            'features': [{
#                'type': 'TEXT_DETECTION',
#                'maxResults': 1,
#            }]
#
#        }]
#    }
#    response = requests.post(url, headers=header, json=body).json()
#    text = response['responses'][0]['textAnnotations'][0]['description'] if len(response['responses'][0]) > 0 else ''
#    return text
