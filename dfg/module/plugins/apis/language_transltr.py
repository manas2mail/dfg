# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.oauth2 import service_account
from google.cloud import translate
import google.auth
import six

credentials = service_account.Credentials.from_service_account_file(r"D:\WebServer\webapp\module\data\API Project-3a3c7feb3e12.json")
client = translate.Client(credentials=credentials)

def translate_text(target, text):
    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')    
    result = client.translate(text, target_language=target)

    tTxt=format(result['translatedText'])
    lng=format(result['detectedSourceLanguage'])

    return tTxt, lng

tTxt, lng=translate_text("en","任意のコードを実行することが可能です。また")
print(tTxt)    


#
#
#def extract_entities(text, access_token=None):
#
#    url = 'https://language.googleapis.com/v1beta1/documents:analyzeEntities?key={}'.format('AIzaSyBOsF8iV_3gfR--4U2kkM0gDHo0WvhPSxI')
#    header = {'Content-Type': 'application/json'}
#    body = {
#        "document": {
#            "type": "PLAIN_TEXT",
#            "language": "EN",
#            "content": text
#        },
#        "encodingType": "UTF8"
#    }
#    response = requests.post(url, headers=header, json=body).json()
#    return response