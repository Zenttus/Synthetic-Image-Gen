import bpy
from bpy_extras.object_utils import world_to_camera_view
import os
import random
from lxml import etree

# TODO: Documentation
# TODO: Oganize order
# TODO: Make parameters name better
# TODO: Different label modes for different algorithms

# TODO: Incorporate scale and origin, different types of file, random rotation
def posObjRnd(object, scene, camera, zrange, relativeSize, imageX, filePath, alpha=0.5, rotation=1):

    if(object[0]==None):
        bpy.ops.import_scene.autodesk_3ds(filepath=filePath, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")
        deselectAll()
        object[0] = bpy.data.objects['Box001']
        object[0].scale = (.001, .001, .001)
        for o in range(len(object)):
            object[o] = object[0].copy()
            object[o].data = object[0].data.copy()
            scene.objects.link(object[o])
            zPos = random.uniform(0,zrange)
            yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
            xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
            object[o].location = (xPos, yPos, zPos)
            if(rotation==1):
                object[o].rotation_euler = (random.uniform(0,3.14),random.uniform(0,3.14),random.uniform(0,3.14))
        makeInvisible(bpy.data.objects['Box001'])
    else:
        for o in object:
            if(random.uniform(0,1)<alpha):
                makeInvisible(o)
                o.hide = True
            else:
                o.hide = False
                zPos = random.uniform(0,zrange)
                yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
                xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
                o.location = (xPos, yPos, zPos)
                if(rotation==1):
                    o.rotation_euler = (random.uniform(0,3.14),random.uniform(0,3.14),random.uniform(0,3.14))
    return object

def makeInvisible(ob):
    ob.location = (0,0,-20) # TODO : This is not the best way, fix this(imagine an object that is that big)


def copyObjects(arrayOfObjects, obj, scene):
    arrayOfObjects[0] = obj
    for n in range(1, len(arrayOfObjects)):
        arrayOfObjects[n] = arrayOfObjects[0].copy()
        arrayOfObjects[n] = arrayOfObjects[0].data.copy()
        scene.objects.link(arrayOfObjects[n])

def deselectAll():
    for obj in bpy.data.objects:
        obj.select = False

def prepareScene(resX, resY):
    #Clear all
    for obj in bpy.context.scene.objects:
        obj.select = True
        bpy.ops.object.delete(use_global=False)
    #Create Camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
    camera = bpy.context.object
    scene = bpy.context.scene
    scene.camera = bpy.context.object
    scene.render.resolution_x = resX
    scene.render.resolution_y = resY
    scene.render.resolution_percentage = 100
    #create light
    lamp = updateLamp(None, scene, camera)

    return scene, camera, lamp

def loadImages(backgroundImagesPath):
    picList = os.listdir(backgroundImagesPath)
    jpgList = [item for item in picList if item[-3:] == 'jpg']
    return picList

def changeImage(camera, newImgName, oldImg, pathToBackgroundImages):
    cameraConstant = 2.1892349261 #Based on the camera angle(if field of view changes this must also change)
    deselectAll()
    #Delete Old Image(if there's one)
    if(oldImg!=None):
        oldImg.select = True
        bpy.ops.object.delete(use_global=False)
    #loadNewImage
    bpy.ops.import_image.to_plane(files=[{"name":newImgName}], location=(0,0,0), directory=pathToBackgroundImages,shader='SHADELESS', relative=False)
    newImg = bpy.context.object
    newImg.location = (0,0,0)
    imgPos = newImg.data.vertices[0].co[0]
    camera.location = (0,0,abs(imgPos)*cameraConstant)
    return imgPos, newImg

# TODO: make it more random(color intensity)
def updateLamp(lamp, scene, img):
    #Create lamp if it doesnt exist.
    if(lamp==None):
        lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
        lamp = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
        scene.objects.link(lamp)
    xPos = random.uniform(img.location[0] - 2, img.location[0] + 2)
    yPos = random.uniform(img.location[1] - 2, img.location[1] + 2)
    zPos = random.uniform(img.location[2] + 1, img.location[2] + 2)

    lamp.location = (xPos, yPos, zPos)
    lamp.select = True
    scene.objects.active = lamp

    #Randomize Color 
    r = random.uniform(.5,1)
    g = random.uniform(.5,1)
    b = random.uniform(.5,1)
    lamp.data.color = [r, g, b]

    return lamp

def generateLabelFile(object, scene, camera, pathToResults, img, resX, resY, Objectlabel):
    root = etree.Element("annotation")

    folder = etree.SubElement(root, "folder")
    folder.text = "results"
    fileName = etree.SubElement(root, "filename")
    fileName.text = str(img)
    path = etree.SubElement(root, "path")
    path.text = pathToResults
    source = etree.SubElement(root, "source")
    database = etree.SubElement(source, "database")
    database.text = "Unknown"

    size = etree.SubElement(root, "size")
    width = etree.SubElement(size, "width")
    width.text = str(resX)
    height = etree.SubElement(size, "height")
    height.text = str(resY)
    depth = etree.SubElement(size, "depth")
    depth.text = "3"
    segmented = etree.SubElement(root, "segmented")
    segmented.text = "0"

    for o in object:
        if(o.hide == True):
            continue
        xmaxV, xminV, yminV, ymaxV = getObjCords(scene, o, camera, resX, resY)

        obj = etree.SubElement(root, "object")
        label = etree.SubElement(obj, "name")
        label.text = Objectlabel
        pose = etree.SubElement(obj, "pose")
        pose.text = "Unspecified"
        truncated = etree.SubElement(obj, "truncated")
        truncated.text = "0"
        difficult = etree.SubElement(obj, "difficult")
        difficult.text = "0"
        bndBox = etree.SubElement(obj, "bndbox")
        xmin = etree.SubElement(bndBox, "xmin")
        xmin.text = str(xminV)
        ymin = etree.SubElement(bndBox, "ymin")
        ymin.text = str(yminV)
        xmax = etree.SubElement(bndBox, "xmax")
        xmax.text = str(xmaxV)
        ymax = etree.SubElement(bndBox, "ymax")
        ymax.text = str(ymaxV)

    file = open(pathToResults + '\\' + img + '.xml', 'w')
    file.write(str(etree.tostring(root, pretty_print=True)).replace("\\n","")[2:-1])
    file.close()

# TODO: Research of something to be done with the distance parameter?
def getObjCords(scene, obj, camera, resX, resY):
    mw = obj.matrix_world

    verts = (mw * vert.co for vert in obj.data.vertices)
    cords2d = [world_to_camera_view(scene, camera, coord) for coord in verts]

    xmax = round(cords2d[0][0]*resX)
    xmin = round(cords2d[0][0]*resX)
    ymax = round(cords2d[0][1]*resY)
    ymin = round(cords2d[0][1]*resY)

    for x, y, d in cords2d:
        if(xmax<x*resX):
            xmax = round(x * resX)
        if(xmin>x*resX):
            xmin = round(x * resX)
        if(ymax<y*resY):
            ymax = round(y * resY)
        if(ymin>y*resY):
            ymin = round(y * resY)

    if(xmin<0):
        xmin = 0
    if(ymin<0):
        ymin = 0

    if(xmax>resX):
        xmax = resX
    if(ymax>resY):
        ymax = resY

    ymax = resY - ymax
    ymin = resY - ymin

    return xmax, xmin, ymin, ymax
