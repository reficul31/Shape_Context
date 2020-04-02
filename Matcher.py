# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 21:16:45 2020

@author: shbharad
"""

import cv2
import csv
import numpy as np
import time
from ShapeContext import ShapeContext

pruning_points = 10
sc = ShapeContext()

class Matcher:
    def __init__(self):
        self.filenames = []
        with open('./filenames.csv') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                self.filenames.append(row[0][:-4])
        
        self.pruned = []
        with open('./pruned.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.pruned.append(row)
        
        self.descriptors = []
        with open('./descriptors.csv') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                self.descriptors.append(row)
    
    def prune_match(self, image):
        pruned_image_points = sc.get_points_from_img(image, pruning_points)
        pruned_image_descriptor = sc.compute(pruned_image_points)
        
        pruned_cost = []
        for prune in self.pruned:
            n_prune = np.array(prune)
            n_prune = n_prune.astype(float)
            n_prune = n_prune.reshape(pruned_image_descriptor.shape)
            res_cost, indices = sc.diff(pruned_image_descriptor, n_prune)
            pruned_cost.append(res_cost)
        
        final = []
        for i in range(0, len(self.filenames)):
            final.append([self.filenames[i], pruned_cost[i]])
        
        final = np.array(final)
        sorted_array = final[np.argsort(np.array(final[:, 1]).astype(float))]
        return sorted_array
    
    def find_indices_to_check(self, sorted_array, top = 5):
        indices_to_check = []
        check_filenames = sorted_array[:top][:, 0]
        for filename in check_filenames:
            indices_to_check.append(self.filenames.index(filename))
        return indices_to_check
    
    def match(self, image, indices_to_check = []):
        image_points = sc.get_points_from_img(image)
        image_descriptor = sc.compute(image_points)
        
        if len(indices_to_check) == 0:
            cost = []
            for descriptor in self.descriptors:
                n_descriptor = np.array(descriptor)
                n_descriptor = n_descriptor.astype(float)
                n_descriptor = n_descriptor.reshape(image_descriptor.shape)
                res_cost, indices = sc.diff(image_descriptor, n_descriptor)
                cost.append(res_cost)
            
            final = []
            for i in range(0, len(self.filenames)):
                final.append([self.filenames[i], cost[i]])
            
            final = np.array(final)
            sorted_array = final[np.argsort(final[:, 1])]
            return sorted_array    
        else:
            final = []
            for i in indices_to_check:
                n_descriptor = np.array(self.descriptors[i])
                n_descriptor = n_descriptor.astype(float)
                n_descriptor = n_descriptor.reshape(image_descriptor.shape)
                res_cost, indices = sc.diff(image_descriptor, n_descriptor)
                final.append([self.filenames[i], res_cost])
            
            final = np.array(final)
            sorted_array = final[np.argsort(np.array(final[:, 1]).astype(float))]
            return sorted_array

if __name__ == '__main__':
    start_time = time.time()
    matcher = Matcher()
    image_path = './betatest.png'
    image = cv2.imread(image_path, 0)
    
    prune_match = matcher.prune_match(image)
    indices_to_check = matcher.find_indices_to_check(prune_match, 10)
    match = matcher.match(image, indices_to_check)
    
    print(match[:, 0])
    print("--- %s seconds ---" % (time.time() - start_time))
