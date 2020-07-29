# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 08:52:15 2020

@author: shbharad
"""


import time 
import requests
from PIL import Image
import base64, re
import io
import numpy as np
# Display images within Jupyter

class TextMatcher:
    def __init__(self):
        self.url = "https://westus2.api.cognitive.microsoft.com/vision/v2.0/recognizeText" # Here, paste your full endpoint from the Azure portal
        self.key = "c21f4d7cc0ac4c7e94217ff0a1b17737"  # Here, paste your primary key
        self.maxNumRetries = 10
    
    def process_request(self, json, data, headers, params):
        retries = 0
        result = None
    
        while True:
            response = requests.request( 'post', self.url, json = json, data = data, headers = headers, params = params )
    
            if response.status_code == 429:
                if retries <= self.maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    print( 'Error: failed after retrying!' )
                    break
            elif response.status_code == 202:
                result = response.headers['Operation-Location']
            else:
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json() ) )
            break
            
        return result    
    
    def get_OCR_text_result(self, operationLocation, headers):
        retries = 0
        result = None
    
        while True:
            response = requests.request('get', operationLocation, json=None, data=None, headers=headers, params=None)
            if response.status_code == 429:
                print("Message: %s" % (response.json()))
                if retries <= self.maxNumRetries:
                    time.sleep(1)
                    retries += 1
                    continue
                else:
                    print('Error: failed after retrying!')
                    break
            elif response.status_code == 200:
                result = response.json()
            else:
                print("Error code: %d" % (response.status_code))
                print("Message: %s" % (response.json()))
            break
    
        return result
    
    def get_text_from_result(self, result):
        final = []
        lines = result['recognitionResult']['lines']
        for i in range(len(lines)):
            words = lines[i]['words']
            s = ''
            for j in range(len(words)):
                text = words[j]['text']
                s = s + text + ' '
            final.append(s)
        return final

    def match_text(self, data):
        params = {'mode' : 'Handwritten'}
        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = self.key
        headers['Content-Type'] = 'application/octet-stream'
        json = None
        operationLocation = self.process_request(json, data, headers, params)
    
        result = None
        if (operationLocation != None):
            headers = {}
            headers['Ocp-Apim-Subscription-Key'] = self.key
            while True:
                time.sleep(1)
                result = self.get_OCR_text_result(operationLocation, headers)
                if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                    break
        
        text = ['Nothing']
        if result is not None and result['status'] == 'Succeeded':
            text = self.get_text_from_result(result)
        return ''.join(text)

def read_transparent_png(image_4channel):
    alpha_channel = image_4channel[:,:,3]
    rgb_channels = image_4channel[:,:,:3]

    # White Background Image
    white_background_image = np.ones_like(rgb_channels, dtype=np.uint8) * 255

    # Alpha factor
    alpha_factor = alpha_channel[:,:,np.newaxis].astype(np.float32) / 255.0
    alpha_factor = np.concatenate((alpha_factor,alpha_factor,alpha_factor), axis=2)

    # Transparent Image Rendered on White Background
    base = rgb_channels.astype(np.float32) * alpha_factor
    white = white_background_image.astype(np.float32) * (1 - alpha_factor)
    final_image = base + white
    return final_image.astype(np.uint8)

if __name__ == '__main__':
    base64_image = "data:image/png;base64,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"
    base64_data = re.sub('^data:image/.+;base64,', '', base64_image)
    imgdata = base64.b64decode(base64_data)
    image = Image.open(io.BytesIO(imgdata))
    image = np.array(image)
    image = read_transparent_png(image)
    im = Image.fromarray(image)
    # imgByteArr = io.BytesIO()
    # image.save(imgByteArr, format='PNG')
    # data = imgByteArr.getvalue()
    # start_time = time.time()
    # matcher = TextMatcher()
    # text = matcher.match_text(data)
    # print(text)
    # print("--- %s seconds ---" % (time.time() - start_time))