import bpy
import os
import random
from lxml import etree

#TODO move functions to library and add documentation
def posObjRnd(object, zrange, relativeSize, imageX):
    #TODO object has a origin vector and scale factor
    zPos = random.uniform(0,zrange)
    yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
    xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
    print(zPos)
    print(yPos)j
    print(xPos)

    if(object==None):
        bpy.ops.import_scene.autodesk_3ds(filepath="C:\\Users\\Owrn\\Documents\\gitRepos\\synthetic-data-gen-hub\\tenbal.3DS", axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl",)
        for obj in bpy.data.objects:
            obj.select = False
        object = bpy.data.objects['Box001']
        object.scale = (.001, .001, .001)#TODO make as arg

    object.location = (xPos, yPos, zPos)
#    bpy.ops.mesh.primitive_uv_sphere_add(location = (xPos, yPos, zPos), size=0.1)#TODO change this to load data
    return object

def prepareScene():
    for obj in bpy.context.scene.objects:
        obj.select = True
        bpy.ops.object.delete(use_global=False)
    #Create Camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
    camera = bpy.context.object
    scene = bpy.context.scene
    scene.camera = bpy.context.object
    #TODO make resolution a parameter
    scene.render.resolution_x = 640
    scene.render.resolution_y = 480

    return scene, camera

def loadImages():#TODO add args
    #TODO make it read from args
    #pathToBackgroundImages = sys.argv[1]
    pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen-hub', 'backgroundImages')
    picList = os.listdir(pathToBackgroundImages)
    jpgList = [item for item in picList if item[-3:] == 'jpg']
    return picList

def changeImage(camera, img, tempImg):
    if(tempImg!=None):
        for obj in bpy.data.objects:
            obj.select = False
        tempImg.select = True
        bpy.ops.object.delete(use_global=False)
    bpy.ops.import_image.to_plane(files=[{"name":img}], location=(0,0,0), directory=pathToBackgroundImages,shader='SHADELESS', relative=False)
    temp = bpy.context.object
    temp.location = (0,0,0)
    camera.location = (0,0,abs(temp.data.vertices[0].co[0])*cameraConstant)
    return temp.data.vertices[0].co[0], temp

def generateLabelFile(object, camera, img, n):
    root = etree.Element("annotation")
    folder = etree.SubElement(root, "folder")
    folder.text = ""
    fileName = etree.SubElement(root, "filename")
    fileName.text = str(img)
    path = etree.SubElement(root, "path")
    path.text = ""
    size = etree.SubElement(root, "size")
    width = etree.SubElement(size, "width")
    width.text = ""
    height = etree.SubElement(size, "height")
    height.text = ""
    depth = etree.SubElement(size, "depth")
    depth.text = "3"
    segmented = etree.SubElement(root, "segmented")
    segmented.text = "0"

    obj = etree.SubElement(root, "object")
    label = etree.SubElement(obj, "name")
    label.text = ""
    pose = etree.SubElement(obj, "pose")
    pose.text = "Unspecified"
    truncated = etree.SubElement(obj, "truncated")
    truncated.text = "0"
    difficult = etree.SubElement(obj, "difficult")
    difficult.text = "0"
    bndBox = etree.SubElement(obj, "bndbox")
    xmin = etree.SubElement(bndBox, "xmin")
    xmin.text = ""
    ymin = etree.SubElement(bndBox, "ymin")
    ymin.text = ""
    xmax = etree.SubElement(bndBox, "xmax")
    xmax.text = ""
    ymax = etree.SubElement(bndBox, "ymax")
    ymax.text = ""
    file = open(os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen-hub', 'backgroundImages', 'test.xml'), 'w')
    file.write(str(etree.tostring(root, pretty_print=True)).replace("\\n","")[2:])
    file.close()

def updateLamp(lamp, scene, img):
    if(lamp==None):
        lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
        lamp = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
        scene.objects.link(lamp)
    #TODO make light color random
    xPos = random.uniform(img.location[0] - 2, img.location[0] + 2)
    yPos = random.uniform(img.location[1] - 2, img.location[1] + 2)
    zPos = random.uniform(img.location[2] + 1, img.location[2] + 2)

    lamp.location = (xPos, yPos, zPos)
    lamp.select = True
    scene.objects.active = lamp
    return lamp

pathToBackgroundImages = os.path.join('C:\\', 'Users', 'Owrn', 'Documents', 'gitRepos', 'synthetic-data-gen-hub', 'backgroundImages')
cameraConstant = 2.1892349261 #Based on the camera angle(if field of view changes this must also change)
numOfPics = 5

scene, camera = prepareScene()
lamp = updateLamp(None, scene, camera)
jpgList = loadImages()

#TODO automate black horizon
#TODO yolo trainig output
#TOFO add random rotation
o = None
tempImg = None
for img in jpgList:
    imagePos, tempImg = changeImage(camera, img, tempImg)
    for n in range(numOfPics):
        o = posObjRnd(o, 1, 1, imagePos)
        lamp = updateLamp(lamp, scene, o)
        bpy.data.scenes['Scene'].render.filepath = 'C:\\Users\\Owrn\\Documents\\gitRepos\\synthetic-data-gen-hub\\image' + str(img) + str(n) + '.jpg'
        bpy.ops.render.render( write_still=True )
        generateLabelFile(o, camera, img, n)

o.select = True
bpy.ops.object.delete(use_global=False)
