# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 09:50:06 2020

@author: shbharad
"""

import numpy as np
import base64, re

from io import BytesIO
from PIL import Image
from Matcher import Matcher
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse

matcher = Matcher()
app = Flask(__name__)
api = Api(app)

class SymbolMatcher(Resource):
    def post(self):
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('symbol', type=str, help='Base64 string image', required=True)
        
        args = parser.parse_args()
        codec = args['symbol']
        base64_data = re.sub('^data:image/.+;base64,', '', codec)
        byte_data = base64.b64decode(base64_data)
        image_data = BytesIO(byte_data)
        image = Image.open(image_data)
        
        prune_match = matcher.prune_match(np.array(image))
        indices_to_check = matcher.find_indices_to_check(prune_match, 10)
        match = matcher.match(np.array(image), indices_to_check)
        return jsonify(match[:, 0].tolist())
    
    def get(self):
        return {'Hello': 'Hello World'}

api.add_resource(SymbolMatcher, '/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)