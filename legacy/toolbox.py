import bpy
from bpy_extras.object_utils import world_to_camera_view
import os
import random
from lxml import etree


def prepare_scene(res_x, res_y):
    '''
    Initiacion of scene(creates camera and lamp)
    '''
    # Clear all
    for obj in bpy.context.scene.objects:
        obj.select = True
        bpy.ops.object.delete(use_global=False)
    # Create Camera
    bpy.ops.object.camera_add(view_align=True, enter_editmode=False, location=(0,0,0), rotation=(0,0,0))
    camera = bpy.context.object
    scene = bpy.context.scene
    scene.camera = bpy.context.object
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100
    # Create light
    lamp = update_lamp(None, scene, camera)

    return scene, camera, lamp


def update_lamp(lamp, scene, img):
    '''
    Randomizes lamp position, if it doesnt exist it creates a lamp.
    '''
    # Create lamp if it doesnt exist.
    if lamp is None:
        lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
        lamp = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
        scene.objects.link(lamp)

    x_pos = random.uniform(img.location[0] - 2, img.location[0] + 2)
    y_pos = random.uniform(img.location[1] - 2, img.location[1] + 2)
    z_pos = random.uniform(img.location[2] + 1, img.location[2] + 2)

    lamp.location = (x_pos, y_pos, z_pos)
    lamp.select = True
    scene.objects.active = lamp

    # TODO: Position the lamp and color it based on backgroundImage.
    # Randomize Color
    r = random.uniform(.5, 1)
    g = random.uniform(.5, 1)
    b = random.uniform(.5, 1)
    lamp.data.color = [r, g, b]

    return lamp


# TODO: make positioning of camera more accurate(so that there's no black bars)
def change_image(camera, new_img_name, old_img, path_to_background_images):
    '''
    Changes the background Image.
    '''
    camera_constant = 2.1892349261  # Based on the camera angle(if field of view changes this must also change)
    # TODO: get this constant via code.
    deselect_all()
    # Delete Old Image(if there's one)
    if old_img is not None:
        old_img.select = True
        bpy.ops.object.delete(use_global=False)
    # Load New Image
    bpy.ops.import_image.to_plane(files=[{"name": new_img_name}], location=(0, 0, 0), directory=path_to_background_images, shader='SHADELESS', relative=False)
    new_img = bpy.context.object
    new_img.location = (0, 0, 0)
    img_pos = new_img.data.vertices[0].co[0]

    camera.location = (0, 0, abs(img_pos)*camera_constant)
    return img_pos, new_img


# TODO: Incorporate scale and origin, different types of file
def pos_obj_rnd(object, scene, camera, z_range, relativeSize, imageX, filePath, alpha=0.5, rotation=1):

    if object[0] is None:
        bpy.ops.import_scene.autodesk_3ds(filepath=filePath, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")
        deselect_all()
        object[0] = bpy.data.objects['Box001']
        object[0].scale = (.001, .001, .001)  # TODO read this from file
        for o in range(len(object)):
            object[o] = object[0].copy()
            object[o].data = object[0].data.copy()
            scene.objects.link(object[o])

            z_pos = random.uniform(0, z_range)
            y_pos = random.uniform((-1)*((camera.location[2]-z_pos)/camera.location[2])/2, ((camera.location[2]-z_pos)/camera.location[2])/2)
            x_pos = random.uniform(imageX*((camera.location[2]-z_pos)/camera.location[2]), abs(imageX)*((camera.location[2]-z_pos)/camera.location[2]))
            object[o].location = (x_pos, y_pos, z_pos)
            if rotation is 1:  # TODO read this from conf file
                object[o].rotation_euler = (random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14))
        make_invisible(bpy.data.objects['Box001'])
    else:
        for o in object:
            if random.uniform(0, 1) < alpha:
                make_invisible(o)
                o.hide = True
            else:
                o.hide = False
                z_pos = random.uniform(0, z_range)
                y_pos = random.uniform((-1)*((camera.location[2]-z_pos)/camera.location[2])/2, ((camera.location[2]-z_pos)/camera.location[2])/2)
                x_pos = random.uniform(imageX*((camera.location[2]-z_pos)/camera.location[2]), abs(imageX)*((camera.location[2]-z_pos)/camera.location[2]))
                o.location = (x_pos, y_pos, z_pos)
                if rotation is 1:  # TODO read this from conf file
                    o.rotation_euler = (random.uniform(0, 3.14), random.uniform(0, 3.14), random.uniform(0, 3.14))
    return object


def make_invisible(ob):
    ob.location = (0, 0, -20)  # TODO : Make this properly. This is not the best way, fix this(imagine an object that is that big)


def copy_objects(array_of_objects, obj, scene):
    array_of_objects[0] = obj
    for n in range(1, len(array_of_objects)):
        array_of_objects[n] = array_of_objects[0].copy()
        array_of_objects[n] = array_of_objects[0].data.copy()
        scene.objects.link(array_of_objects[n])


def deselect_all():
    for obj in bpy.data.objects:
        obj.select = False


# TODO Update this to get them from the conf file.
def load_backgrounds(background_images_path):
    pic_list = os.listdir(background_images_path)
    jpg_list = [item for item in pic_list if item[-3:] == 'jpg']  # TODO: add other kinds of images
    return jpg_list


# TODO: Implement mode to save object distance
def get_obj_cords(scene, obj, camera, res_x, res_y):
    """
    Returns the coordinates that encloses an object in image.
    """

    # Get vertices
    mw = obj.matrix_world
    verts = (mw * vert.co for vert in obj.data.vertices)
    cords2d = [world_to_camera_view(scene, camera, coord) for coord in verts]

    xmax = round(cords2d[0][0] * res_x)
    xmin = round(cords2d[0][0] * res_x)
    ymax = round(cords2d[0][1] * res_y)
    ymin = round(cords2d[0][1] * res_y)

    # Calculate min and max of vertices.
    for x, y, d in cords2d:
        if xmax < x*res_x:
            xmax = round(x * res_x)
        if xmin > x*res_x:
            xmin = round(x * res_x)
        if ymax < y*res_y:
            ymax = round(y * res_y)
        if ymin > y*res_y:
            ymin = round(y * res_y)

    # If object has part out of image.
    if xmin < 0:
        xmin = 0
    if ymin < 0:
        ymin = 0
    if xmax > res_x:
        xmax = res_x
    if ymax > res_y:
        ymax = res_y

    #Convert coordinate system #TODO: make this a parameter, to have different coordinates modes.
    ymax = res_y - ymax
    ymin = res_y - ymin

    return xmax, xmin, ymin, ymax


# LABELING FUNCTIONS


def generate_label_xml_file(object, scene, camera, pathToResults, img, resX, resY, Objectlabel):
    '''
    Generate the .xml version of the label file.
    '''
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
        if o.hide is True:
            continue
        xmaxV, xminV, yminV, ymaxV = get_obj_cords(scene, o, camera, resX, resY)

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


def generate_label_text_file(object, scene, camera, pathToResults, img, resX, resY, Objectlabel):
    '''
    Generate the .txt version of the label file.
    '''
    file = open(pathToResults + '\\' + img + '.txt', 'w')
    for o in object:
        if o.hide is True:
            continue
        xmaxV, xminV, yminV, ymaxV = get_obj_cords(scene, o, camera, resX, resY)
        s = str(Objectlabel) + ' ' + str(((xmaxV+xminV)/2)/resX) + ' ' + str(((ymaxV+yminV)/2)/resY) + ' ' + str((xmaxV-xminV)/resX) + ' ' + str(abs(ymaxV-yminV)/resY) + '\n'
        file.write(s)

    file.close()
