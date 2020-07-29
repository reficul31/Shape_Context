# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 20:43:25 2020

@author: shbharad
"""
import os
import base64

class Doodler:
    def __init__(self):
        pass
    
    def get_image_paths(self, sorted_array, top = 10):
        path='./static'
        files_paths = []
        files_list = []
        for r, d, f in os.walk(path):
            for file in f:
                files_list.append(file)
        for class_name in sorted_array:    
            for x in files_list:
                if class_name[:-1] in x:
                    files_paths.append(path+'/'+x)
        
        encoded_images = []
        for path in files_paths:
            with open(path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                base_64_string = encoded_string.decode('ascii')
                encoded_images.append('data:image/png;base64,' + base_64_string)
        return encoded_images[:top]

if __name__=='__main__':
    sorted_array = ['Guitar', 'Bat', 'House', 'Car']
    strings = Doodler().get_image_paths(sorted_array)