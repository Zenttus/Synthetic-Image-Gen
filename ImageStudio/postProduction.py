import numpy as np
from PIL import Image
import style
import os
import cv2
import glob
import sys
from random import randint
from shutil import copyfile
from keras.preprocessing.image import load_img, save_img, img_to_array

import subprocess
import xml.etree.ElementTree as xml

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from style import Styler

#TODO darknet output

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
    save_img(image, result)

def flip(image, flipver=True, fliphor=False):
    result = image
    if fliphor:
        result = result.transpose(Image.FLIP_LEFT_RIGHT)
    if flipver:
        result = result.transpose(Image.FLIP_TOP_BOTTOM)
    save_img(image, result)
    flip_label_file(image)

def ditexturize(images, styles, results_path):
    for i in images:
        count = 0
        for s in styles:
            styler = Styler()
            res = styler.change_style(i, s, results_path)
            del styler
            count += 1
            save_img("{0}{1}t{2}.png".format(results_path, os.path.splitext(i)[0].split("\\")[-1], count), res)
            duplicate_label_file("{0}.xml".format(os.path.splitext(i)[0]), "{0}{1}t{2}.xml".format(results_path, os.path.splitext(i)[0].split("\\")[-1], count), "{0}t{1}.xml".format(os.path.splitext(i)[0].split("\\")[-1], count), results_path)

def fast_ditexturize(path_to_script, model, src, des):
    process = subprocess.Popen("python " + path_to_script + " --checkpoint " + model + " --in-path " + src + " --out-path " + des, shell=True, stdout=subprocess.PIPE)
    process.wait()
    duplicate_label_file_fast(src, des, os.path.splitext(model)[0])


def duplicate_label_file(src, des, new_filename, new_path):
    # Open original file
    et = xml.ElementTree(file=src)
    root = et.getroot()

    for filename in root.iter("filename"):
        filename.text = new_filename
    for path in root.iter("path"):
        path.text = new_path
    et.write(des)


def duplicate_label_file_fast(src, dst, stl):
    for label in glob.iglob(os.path.join(src, "*.xml")):
        duplicate_label_file(label, "{0}{1}{2}.xml".format(dst, os.path.splitext(label)[0].split("\\")[-1],  os.path.splitext(stl)[0].split("\\")[-1]),  "{0}{1}.xml".format(os.path.splitext(label)[0].split("\\")[-1], stl), stl)
        org_name = dst+os.path.splitext(label)[0].split("\\")[-1]+".png"
        new_name = dst+os.path.splitext(label)[0].split("\\")[-1]+os.path.splitext(stl)[0].split("\\")[-1]+".png"
        os.rename(org_name, new_name)

#def flip_label_file(file):
    # TODO: it assumes that the file is xml.
# TODO: def data_preparer():
# TODO: def mulitcrop():
# TODO: def rotate():


src_dir = "D:\\drone-data\\"
dst_dir = "D:\\drone-data\\spiced\\"
path_to_script = "D:\\GitProjects\\fast-style-transfer\\evaluate.py"
style_dir = "D:\\GitProjects\\Synthetic-Image-Gen\\models"

for s in glob.iglob(os.path.join(style_dir, "*.ckpt")):
    print("Styling with {}".format(style_dir.split("\\")[-2]))
    fast_ditexturize(path_to_script, s, src_dir, dst_dir)

for image in glob.iglob(os.path.join(dst_dir, "*.png")):
   # if randint(0, 9) > 2:
       # flip(image)
    if randint(0, 9) > 2:
        add_noise(image)
    if randint(0, 9) > 2:
        add_noise(image, gauss=False, snp=True)


