# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:48:55 2020

@author: shbharad
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt

simpleto = 40

def show_image_points(image):
    image = cv2.resize(image, (500, 500))
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    ret, thresh = cv2.threshold(image, 127, 255, 0)
    _, cnts, heir = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    points = np.array([[0, 0]])
    for cnt in cnts:
        if len(cnts) > 1:
            points = np.concatenate([points, np.array(cnt).reshape((-1, 2))], axis=0)
    
    indexes = [[n[0] != 0 and n[1] != 0 and n[0] != image.shape[1]-1 and n[1] != image.shape[0]-1 for n in points]]
    points = points[indexes]
    points = points.tolist()
    step = int(len(points) / simpleto)
    if step < 1:
        step = 1
    points = [points[i] for i in range(0, len(points), step)][:simpleto]
    if len(points) < simpleto:
        points = points + [[0, 0]] * (simpleto - len(points))
    
    points = np.array(points)
    plt.subplot(111),plt.imshow(image, cmap='gray')
    plt.scatter(x = points[:, 0], y = points[:, 1], c='r', s=40)
    plt.show()