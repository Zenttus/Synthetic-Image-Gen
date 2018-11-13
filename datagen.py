import bpy
import os
import sys
import toolbox
import json
import random

#TODO that the conf file has the backgroundImages info

with open('config.json', 'r') as f:
    config = json.load(f)

# TODO clean this mess
pathToBackgroundImages = config['SETTINGS']['BackGroundImagesPath']
pathToObject = config['OBJECTS']['O1']['ObjectModelPath']
pathToResults = config['SETTINGS']['PathToResults']
numOfPics = config['SETTINGS']['PicturesPerBackgroudn']
resX = config['SETTINGS']['ResX']
resY = config['SETTINGS']['ResY']
label = config['OBJECTS']['O1']['Label']
rotate = config['OBJECTS']['O1']['Rotate']
maxNumOfObjects = config['OBJECTS']['O1']['MaxRepetition']

#Prepare enviorment
scene, camera, lamp = toolbox.prepareScene(resX, resY)
jpgList = toolbox.loadImages(pathToBackgroundImages)

object = [None] * maxNumOfObjects
currentImg = None

for imgName in jpgList:
    imagePos, currentImg = toolbox.changeImage(camera, imgName, currentImg, pathToBackgroundImages)
    for n in range(numOfPics):
        object = toolbox.posObjRnd(object, scene, camera, 1, 1, imagePos, pathToObject, rotation=rotate)
        lamp = toolbox.updateLamp(lamp, scene, camera)

        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(imgName[:-4]) + str(n) + '.png' # TODO find best format.
        bpy.ops.render.render( write_still=True )
\
        toolbox.generateLabelFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)
