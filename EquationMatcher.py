# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 09:55:10 2020

@author: shbharad
"""
import os
import requests
import json
from lxml import etree
import matplotlib.pyplot as plt
import base64
import io

def mathml2latex_yarosh(equation):
    """ MathML to LaTeX conversion with XSLT from Vasil Yaroshevich """
    xslt_file = os.path.join('mathconverter', 'xsl_yarosh', 'mmltex.xsl')
    dom = etree.fromstring(equation)
    xslt = etree.parse(xslt_file)
    transform = etree.XSLT(xslt)
    newdom = transform(dom)
    return newdom

#Ink Analysis service URL
INK_TO_MATH_URL = 'https://cii-ppe.azure-api.net/Ink/AnalysisMath/?api-version=beta'
SUBSCRIPTION_KEY = '7294f5ba13be41ae9704dd944f31ba33'

class EquationMatcher:
    def __init__(self):
        pass
    
    def get_mathml_from_strokes(self, paths = []):
        i = 0
        strokes = []
        for path in paths:
            str_point_list = [str(point) for point in path]
            stroke = {"id":i, "points":",".join(str_point_list)}
            strokes.append(stroke)
            i+=1
        payload = {"language":"en-US", "version":1,"unit":"mm", "strokes":strokes}
        headers = {"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY, 'Content-Type': 'application/json'}
        mathResponse = requests.put(INK_TO_MATH_URL, data = json.dumps(payload), headers = headers)
        response_json = json.loads(mathResponse.content)
        recognitionUnit = response_json["recognitionUnits"][0]
        recognizedMath = recognitionUnit["recognizedMath"]
        return recognizedMath
    
    def get_base64_image_from_mathml(self, mathml = ''):
        tex = mathml2latex_yarosh(mathml)
        fig, ax = plt.subplots()
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.text(0, 0.6, tex, fontsize = 50)                                  
        
        io_bytes = io.BytesIO()
        plt.savefig(io_bytes,  format='png')
        io_bytes.seek(0)
        img_string = base64.b64encode(io_bytes.read())
        return 'data:image/png;base64,' + img_string.decode('ascii')

if __name__=='__main__':
    matcher = EquationMatcher()
    paths = [[38, 97, 43, 97, 52, 102, 57, 104, 58, 104, 60, 105, 60, 107, 61, 108, 62, 111, 65, 114, 66, 119, 67, 122, 67, 123, 67, 125, 67, 126, 67, 127, 67, 128, 64, 129, 63, 129, 62, 130, 61, 131, 59, 131, 57, 131, 54, 131, 51, 131, 48, 131, 47, 131, 46, 131]]
    mathml = matcher.get_mathml_from_strokes(paths)
    img = matcher.get_base64_image_from_mathml(mathml)