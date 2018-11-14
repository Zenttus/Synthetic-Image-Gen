import bpy
import os
import time
import sys
import json
import random
import toolbox

#TODO that the conf file has the backgroundImages info
#TODO script to set shits
#TODO Make background black
#TODO Make script to automate setting up
#TODO dinamic camera
#TODO label type
#TODO Write README
#TODO Make object a class

tick = time.time()

with open('config.json', 'r') as f:
    config = json.load(f)

# TODO clean this mess
pathToBackgroundImages = config['SETTINGS']['BackGroundImagesPath']
pathToObject = config['OBJECTS']['O1']['ObjectModelPath'] # TODO : Make it for more than one type of object
pathToResults = config['SETTINGS']['PathToResults']
numOfPics = config['SETTINGS']['PicturesPerBackgroudn']
resX = config['SETTINGS']['ResX']
resY = config['SETTINGS']['ResY']
label = config['OBJECTS']['O1']['Label']
rotate = config['OBJECTS']['O1']['Rotate']
maxNumOfObjects = config['OBJECTS']['O1']['MaxRepetition']
alp = config['OBJECTS']['O1']['Alpha']
usingGPU = config['SETTINGS']['GPU']
xmlLabels = config['SETTINGS']

#Prepare enviorment
scene, camera, lamp = toolbox.prepareScene(resX, resY)
jpgList = toolbox.loadImages(pathToBackgroundImages)

#GPU acceleration
if(usingGPU==1):
    scene.cycles.device = 'GPU'

object = [None] * maxNumOfObjects
currentImg = None

for imgName in jpgList:
    imagePos, currentImg = toolbox.changeImage(camera, imgName, currentImg, pathToBackgroundImages)
    for n in range(numOfPics):
        object = toolbox.posObjRnd(object, scene, camera, 1, 1, imagePos, pathToObject, rotation=rotate, alpha=alp)
        lamp = toolbox.updateLamp(lamp, scene, camera)

        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(imgName[:-4]) + str(n) + '.jpg' # TODO find best format.
        bpy.ops.render.render( write_still=True )
        toolbox.generateLabelTextFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)
        #toolbox.generateLabelFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)

tock = time.time()
print("Pictures Printed: " + str(len(jpgList)*numOfPics) + "\nResolution: " + str(resX) + " x " + str(resY) + "\nTime: " + str(tock-tick))
