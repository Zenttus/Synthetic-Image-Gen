import bpy
import os
import random

#TODO move functions to library and add cocumentation
#TODO check valididity of zrange(zrange being the distance from image)
def posObjRnd(object, zrange, relativeSize, imageX):
     zPos = random.uniform(0,zrange)
     yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
     xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
     print(zPos)
     print(yPos)
     print(xPos)
     bpy.ops.mesh.primitive_uv_sphere_add(location = (xPos, yPos, zPos), size=0.1)#TODO change this to load data

def cleanScene():
    for obj in bpy.context.scene.objects:
        obj.select = True
        bpy.ops.object.delete(use_global=False)

def loadImages():#TODO add args
    #TODO make it read from args
    #pathToBackgroundImages = sys.argv[1]
    pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen', 'backgroundImages')
    picList = os.listdir(pathToBackgroundImages)
    jpgList = [item for item in picList if item[-3:] == 'jpg']
    return picList

def changeImage(camera, img):
    bpy.ops.import_image.to_plane(files=[{"name":img}], location=(0,0,0), directory=pathToBackgroundImages,shader='SHADELESS', relative=False)
    temp = bpy.context.object
    temp.location = (0,0,0)
    camera.location = (0,0,abs(temp.data.vertices[0].co[0])*cameraConstant)
    return temp.data.vertices[0].co[0]



pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen', 'backgroundImages')#TODO remove this eventually
cameraConstant = 2.1892349261 #Based on the camera angle(if field of view changes this must also change)

cleanScene()

#Create Camera
bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
camera = bpy.context.object

#TODO add light source

jpgList = loadImages()

for img in jpgList:
    imagePos = changeImage(camera, img)
    posObjRnd(camera, 1, 1, imagePos)
