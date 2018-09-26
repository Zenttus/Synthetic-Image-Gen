import bpy
import os

pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Desktop', 'backgroundImages')
cameraConstant = 2.1892349261

#Clean up scene
for obj in bpy.context.scene.objects:
    obj.select = True
    bpy.ops.object.delete(use_global=False)
    
bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
camera = bpy.context.object

fileList = os.listdir(pathToBackgroundImages)
jpgList = [item for item in fileList if item[-3:] == 'jpg']
#print(jpgList)



for img in jpgList:
    bpy.ops.import_image.to_plane(files=[{"name":img}], location=(0,0,0), directory=pathToBackgroundImages,shader='SHADELESS', relative=False)
    temp = bpy.context.object
    temp.location = (0,0,0)
    camera.location = (0,0,abs(temp.data.vertices[0].co[0])*cameraConstant)