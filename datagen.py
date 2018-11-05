import bpy
import os
import toolbox

pathToBackgroundImages = 'C:\\Users\\Owrn\\Documents\\gitRepos\\synthetic-data-gen-hub\\backgroundImages'
pathToObject = 'C:\\Users\\Owrn\\Documents\\gitRepos\\synthetic-data-gen-hub\\tenbal.3DS'
pathToResults = 'C:\\Users\\Owrn\\Documents\\gitRepos\\synthetic-data-gen-hub\\results'
numOfPics = 5
resX = 640
resY = 480
label = 'tennisBall'

#Prepare enviorment
scene, camera, lamp = toolbox.prepareScene(resX, resY)
jpgList = toolbox.loadImages(pathToBackgroundImages)


object = None
currentImg = None
for imgName in jpgList:
    imagePos, currentImg = toolbox.changeImage(camera, imgName, currentImg, pathToBackgroundImages)
    for n in range(numOfPics):

        object = toolbox.posObjRnd(object, camera, 1, 1, imagePos, pathToObject)
        lamp = toolbox.updateLamp(lamp, scene, object)

        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(imgName[:-4]) + str(n) + '.jpg'
        bpy.ops.render.render( write_still=True )

        toolbox.generateLabelFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)

#o.select = True
#bpy.ops.object.delete(use_global=False)
