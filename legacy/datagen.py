import bpy
from legacy import toolbox

#Prepare enviorment
scene, camera, lamp = toolbox.prepareScene(resX, resY)
jpgList = toolbox.loadImages(pathToBackgroundImages)


object = [None] * maxNumOfObjects
currentImg = None

for imgName in jpgList:
    imagePos, currentImg = toolbox.changeImage(camera, imgName, currentImg, pathToBackgroundImages)
    for n in range(numOfPics):
        object = toolbox.posObjRnd(object, scene, camera, 1, 1, imagePos, pathToObject, rotation=rotate, alpha=alp)
        lamp = toolbox.updateLamp(lamp, scene, camera)

        bpy.data.scenes['Scene'].render.filepath = pathToResults + '\\' + str(imgName[:-4]) + str(n) + '.jpg' # TODO find best format.
        bpy.ops.render.render( write_still=True )
        #toolbox.generateLabelTextFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)
        toolbox.generateLabelXmlFile(object, scene, camera, pathToResults, str(imgName[:-4]) + str(n), resX, resY, label)

print("Pictures Printed: " + str(len(jpgList)*numOfPics) + "\nResolution: " + str(resX) + " x " + str(resY) + "\nTime: " + str(tock-tick))
