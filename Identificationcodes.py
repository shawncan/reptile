#!/usr/local/Cellar/python3
# -*- coding: utf-8 -*-

import pytesseract
from PIL import Image

image = Image.open(r'/Users/wangjiacan/Desktop/code/code.png')
code = pytesseract.image_to_string(image)
print(code)
