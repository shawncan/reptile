#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-
import cv2

fname = '5cc6ef12-0684-4f53-82b5-e816725cbe5a.jpg'

img = cv2.imread(fname)
# 画矩形框
cv2.rectangle(img, (212,317), (290,436), (0,255,0), 10)

