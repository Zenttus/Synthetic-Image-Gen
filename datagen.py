import bpy
import os
import random
    
#TODO check valididity of zrange(zrange being the distance from image)
def posObjRnd(object, zrange, relativeSize, imageX):
     zPos = random.uniform(0,zrange)
     yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
     xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
     print(zPos)
     print(yPos)
     print(xPos)
     bpy.ops.mesh.primitive_uv_sphere_add(location = (xPos, yPos, zPos), size=0.1)

#TODO fix the backgournd image path(make them arguments)
pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen', 'backgroundImages')
cameraConstant = 2.1892349261 #Based on the camera angle(if field of view changes this must also change).

#Clean up scene
for obj in bpy.context.scene.objects:
    obj.select = True
    bpy.ops.object.delete(use_global=False)

#Create Camera
bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
camera = bpy.context.object

#Get Images
fileList = os.listdir(pathToBackgroundImages)
jpgList = [item for item in fileList if item[-3:] == 'jpg']
#print(jpgList)


for img in jpgList:
    bpy.ops.import_image.to_plane(files=[{"name":img}], location=(0,0,0), directory=pathToBackgroundImages,shader='SHADELESS', relative=False)
    temp = bpy.context.object
    temp.location = (0,0,0)
    camera.location = (0,0,abs(temp.data.vertices[0].co[0])*cameraConstant)
    print(temp.data.vertices[0].co)
    posObjRnd(camera, 1, 1, temp.data.vertices[0].co[0]) 

     
    
    