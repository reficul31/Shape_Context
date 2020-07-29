# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:50:06 2020

@author: shbharad
"""
import numpy as np
import base64, re
import json

from io import BytesIO
from PIL import Image
from Matcher import Matcher
from TextMatcher import TextMatcher
from EquationMatcher import EquationMatcher
from Doodler import Doodler
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

equation = EquationMatcher()
text = TextMatcher()
matcher = Matcher()
doodler = Doodler()
app = Flask(__name__)
CORS(app)
api = Api(app)


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

class SymbolMatcher(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('image', type=str, help='Base64 string image', required=True)
        
        args = parser.parse_args()
        codec = args['image']
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        image = Image.open(image_data)
        image = np.array(image)
        image = read_transparent_png(image)
        prune_match = matcher.prune_match(image)
        indices_to_check = matcher.collapse_similar_shapes(prune_match, 6)
        match = matcher.match(np.array(image), indices_to_check)
        matched_paths = doodler.get_image_paths(match[:, 0].tolist(), 10)
        return jsonify(matched_paths)
    
    def get(self):
        return {'Hello': 'Hello World'}

class TextMatcher(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('image', type=str, help='Base64 string image', required=True)
        
        args = parser.parse_args()
        codec = args['image']
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        image = Image.open(image_data)
        image = np.array(image)
        image = read_transparent_png(image)
        image = Image.fromarray(image)
        image_byte = BytesIO()
        image.save(image_byte, format='PNG')
        data = image_byte.getvalue()
        matched_text = text.match_text(data)
        return jsonify({'text': matched_text})
    
    def get(self):
        return {'Hello': 'Hello World'}

class EquationMatcher(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('strokes', type=str, help='Equation strokes', required=True)
        
        args = parser.parse_args()
        strokes = json.loads(args['strokes'])
        mathml = equation.get_mathml_from_strokes(strokes)
        image = equation.get_base64_image_from_mathml(mathml)
        return jsonify({'equation': image})
    
    def get(self):
        return {'Hello': 'Hello World'}

api.add_resource(SymbolMatcher, '/')
api.add_resource(TextMatcher, '/text')
api.add_resource(EquationMatcher, '/equation')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
