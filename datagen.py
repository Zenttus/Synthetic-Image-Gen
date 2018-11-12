import bpy
import os
import sys
import toolbox
import json
import random

#TODO multiple objects
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

object = [None]

for n in range(maxNumOfObjects-1):
    object.append(None)

currentImg = None

for imgName in jpgList:
    imagePos, currentImg = toolbox.changeImage(camera, imgName, currentImg, pathToBackgroundImages)
    for n in range(numOfPics):
        for ob in object:
            if(5 < random.uniform(0,10) or ob==None): #TODO : add this to conf
                ob = toolbox.posObjRnd(ob, camera, 1, 1, imagePos, pathToObject, rotate)
                lamp = toolbox.updateLamp(lamp, scene, ob)
            else:
                ob.delete(use_global=False)
                ob = None

        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(imgName[:-4]) + str(n) + '.png' # TODO find format.
        bpy.ops.render.render( write_still=True )

        #TODO fix this
        #toolbox.generateLabelFile(ob, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)
