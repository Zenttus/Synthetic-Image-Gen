import numpy as np
from PIL import Image
from ImageStudio import style
import os
import cv2
import glob, os

# Current directory
#current_dir = os.path.dirname(os.path.abspath(__file__))
#print(current_dir)
#current_dir = '/home/cc/results/'
# Percentage of images to be used for the test set
#percentage_test = 10;
# Create and/or truncate train.txt and test.txt
#file_train = open('train.txt', 'w')
#file_test = open('test.txt', 'w')
# Populate train.txt and test.txt
#counter = 1
#index_test = round(100 / percentage_test)
#for pathAndFilename in glob.iglob(os.path.join(current_dir, "*.jpg")):
#    title, ext = os.path.splitext(os.path.basename(pathAndFilename))
#    if counter == index_test:
#        counter = 1
#        file_test.write(current_dir + "/" + title + '.jpg' + "\n")
#    else:
#        file_train.write(current_dir + "/" + title + '.jpg' + "\n")
#        counter = counter + 1

# TODO: def aument_data():

def add_noise(image, gauss=True, mean=0, var=0.1, snp=False, svsp=0.5, amount=0.004, poisson=False, speckle=False):
    row, col, ch = image.shape
    result = image
    if poisson:
        vals = len(np.unique(result))
        vals = 2 ** np.ceil(np.log2(vals))
        result = np.random.poisson(result * vals) / float(vals)
    if gauss:
        sigma = var**0.5
        g = np.random.normal(mean, sigma, (row, col, ch))
        g = g.reshape(row, col, ch)
        result += g

    if snp:
        # Salt
        num_salt = np.ceil(amount * image.size * svsp)
        coords = [np.random.randint(0, i-1, int(num_salt))
                  for i in image.shape]
        result[coords] = 1
        # Pepper
        num_pepper = np.ceil(amount * image.size * (1. - svsp))
        coords = [np.random.randint(0, i - 1, int(num_pepper))
                  for i in image.shape]
        result[coords] = 0
    if speckle:
        g = np.random.randn(row, col, ch)
        g = g.reshape(row, col, ch)
        result = result + result * g
    return result

def flip(image, flipver=True, fliphor=False):
    result = image
    if fliphor:
        result = result.transpose(Image.FLIP_LEFT_RIGHT)
    if flipver:
        result = result.transpose(Image.FLIP_TOP_BOTTOM)
    return result

def ditexturize(images, styles):
    styler = style()
    for i in images:
        count = 0
        for s in styles:
            styler.change_style(i, s, i+count)
            count+=1
            # TODO duplicate yolo file



# TODO: def data_preparer():
# TODO: def mulitcrop():
# TODO: def rotate():
