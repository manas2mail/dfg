# -*- coding: utf-8 -*-
#import goslate
import os
import sys
#gs = goslate.Goslate()
sys.path.append('..')


from module.plugins.apis.vision import detect_text
from module.plugins.apis.config_loader import loader
from module.plugins.apis.language import extract_required_entities

from google.oauth2 import service_account
from google.cloud import translate
import six

credentials = service_account.Credentials.from_service_account_file(r"D:\dfg\dfg\module\data\API Project-3a3c7feb3e12.json")
client = translate.Client(credentials=credentials)

def translate_text(target, text):
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')    
    result = client.translate(text, target_language=target)

    tTxt=format(result['translatedText'])
    lng=format(result['detectedSourceLanguage'])
#    LANGUAGES
    return tTxt, lng

    
def fnMain(path):
    text=""    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))    
    text = detect_text(path, google_token['token'])  
#    language_id = gs.detect(text)    
    tTxt,lng=translate_text("en", text)  
    return tTxt,lng    

    
def fnMain1(text):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))  
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8') 
    entities = extract_required_entities(text, google_token['token'])
    return entities   

def LTT_Main(path):
    text=""    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    google_token = loader(os.path.join(BASE_DIR, 'config/google.yaml'))    
    text = detect_text(path, google_token['token'])  
#    language_id = gs.detect(text)    
    tTxt,lng=translate_text("en", text)  
    return tTxt,lng  





#
#if __name__ == '__main__':
#    path=r"D:\dfg\dfg\module\plugins\tests\data\example_en.png"
#    print(fnMain1('TraducciÃ³n de Actas y Documentos'))
#    
#    
#    
#    
    
