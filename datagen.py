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


o = None
tempImg = None
for img in jpgList:
    imagePos, tempImg = toolbox.changeImage(camera, img, tempImg, pathToBackgroundImages)
    for n in range(numOfPics):
        o = toolbox.posObjRnd(o, camera, 1, 1, imagePos, pathToObject)
        lamp = toolbox.updateLamp(lamp, scene, o)
        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(img) + str(n) + '.jpg'
        bpy.ops.render.render( write_still=True )
        toolbox.generateLabelFile(o, camera, pathToResults, img, resX, resY, label)

o.select = True
bpy.ops.object.delete(use_global=False)
