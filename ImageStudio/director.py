import json
import random
from ImageStudio.panel import Panel
from ImageStudio.actor import Actor
from lxml import etree
from bpy_extras.object_utils import world_to_camera_view
import os
import bpy


class Director:

    def __init__(self, conf_file='config.json'):

        with open(conf_file, 'r') as f:
            config = json.load(f)

        # Loading settings
        self.settings = config['SETTINGS']
        self.panels_conf = config["PANELS"]
        self.actors_conf = config["ACTORS"]

        # Loading scene
        self.scene, self.camera = prepare_scene(self.settings['ResX'], self.settings['ResY'])
        self.current_panel = None
        self.light = None
        self.actors = {}

        self.scene.cycles.device = 'GPU'

    def update_light(self):
        # Create light
        if self.light is None:
            lamp_data = bpy.data.lamps.new(name="New Lamp", type='POINT')
            self.light = bpy.data.objects.new(name="New Lamp", object_data=lamp_data)
            self.scene.objects.link(self.light)

        # TODO use conf file parameters to position light
        x_pos = random.uniform(self.current_panel.img.location[0] - 2, self.current_panel.img.location[0] + 2)
        y_pos = random.uniform(self.current_panel.img.location[1] - 2, self.current_panel.img.location[1] + 2)
        z_pos = random.uniform(self.current_panel.img.location[2] + 1, self.current_panel.img.location[2] + 2)
        self.light.location = (x_pos, y_pos, z_pos)
        self.light.select = True
        self.scene.objects.active = self.light

        # TODO: Position the lamp and color it based on backgroundImage.
        # Randomize Color
        r = random.uniform(.8, 1)
        g = random.uniform(.8, 1)
        b = random.uniform(.8, 1)
        self.light.data.color = [r, g, b]

    def update_actors(self):
        # Taking out the actors from the scene
        for type in self.actors:
            for actor in self.actors[type]:
                if not actor.hiden:
                    actor.hide()

        # Adding actors to scene
        labels = self.current_panel.conf['objects']
        max_number_of_actors = int(self.current_panel.conf['maxObjects'])
        for label in labels:
            if label not in self.actors:
                self.actors[label] = []
                for n in range(max_number_of_actors):
                    self.actors[label].append(Actor(self.actors_conf[label]['id'], self.actors_conf[label]['path'], label, self.actors_conf[label]['size']))

        # Positioning actors
        actors_in_set = 0
        for type in self.actors:
            if type in labels:
                if random.random() > 0.5:
                    for actor in self.actors[type]:
                        if random.random() > 0.5 or actors_in_set > max_number_of_actors:  # TODO make this random more random
                            actor.hide()
                        else:
                            actor.pose(self.current_panel, 1, self.camera)
                            actors_in_set += 1
                            actor.hiden = False

    def action(self):
        for panel in self.panels_conf:
            if self.current_panel is None:
                self.current_panel = Panel(panel['path'], panel)
            else:
                self.current_panel.change_background(panel['path'], panel)
            for take in range(self.settings['imagesPerBackground']):
                self.current_panel.update_camera(self.camera)
                self.update_light()
                self.update_actors()
                self.generate_pic(take)

    def generate_pic(self, n):
        path_to_results = self.settings['PathToResults']
        bpy.data.scenes['Scene'].render.filepath = path_to_results + '\\' + os.path.basename(self.current_panel.conf['path'])[:-4] + str(
            n) + '.jpg'
        bpy.ops.render.render(write_still=True)
        self.generate_label_xml_file(path_to_results, os.path.basename(self.current_panel.conf['path'])[:-4] + str(n),
                                self.settings['ResX'], self.settings['ResY'])  # TODO: Implement diferent label modes.

    def generate_label_xml_file(self, pathToResults, img, resX, resY):
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

        for type in self.actors:
            for actor in self.actors[type]:
                if actor.hiden:
                    continue
                print(actor.model)
                xmaxV, xminV, yminV, ymaxV = get_obj_cords(self.scene, actor.model, self.camera, resX, resY)

                obj = etree.SubElement(root, "object")
                label = etree.SubElement(obj, "name")
                label.text = actor.label
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
        file.write(str(etree.tostring(root, pretty_print=True)).replace("\\n", "")[2:-1])
        file.close()


def prepare_scene(res_x, res_y):
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

    return scene, camera


# LABELING FUNCTIONS



def generate_label_text_file(object, scene, camera, pathToResults, img, resX, resY, Objectlabel):
    '''
    Generate the .txt version of the label file.
    '''
    file = open(pathToResults + '\\' + img + '.txt', 'w')
    for o in object:
        if o.hide is True:
            continue
        xmaxV, xminV, yminV, ymaxV = get_obj_cords(scene, o, camera, resX, resY)
        s = str(Objectlabel) + ' ' + str(((xmaxV + xminV) / 2) / resX) + ' ' + str(
            ((ymaxV + yminV) / 2) / resY) + ' ' + str((xmaxV - xminV) / resX) + ' ' + str(
            abs(ymaxV - yminV) / resY) + '\n'
        file.write(s)

    file.close()


def get_obj_cords(scene, obj, camera, res_x, res_y):
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

    #Convert coordinate system
    ymax = res_y - ymax
    ymin = res_y - ymin

    return xmax, xmin, ymin, ymax

