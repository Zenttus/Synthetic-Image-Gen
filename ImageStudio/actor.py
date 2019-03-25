import bpy
import random
import os
import sys


class Actor:

    def __init__(self, id, path, label, size):
        # Deselect all objects
        for obj in bpy.data.objects:
            obj.select = False
        # Loading model
        if "stl" in os.path.splitext(path)[1]:
            bpy.ops.import_mesh.stl(filepath=path)
        elif "obj" in os.path.splitext(path)[1]:
            bpy.ops.import_scene.obj(filepath=path)
        elif "jp" in os.path.splitext(path)[1] or "png" in os.path.splitext(path)[1]: # imports object as plane if its a picture
            bpy.ops.import_image.to_plane(files=[{"name": os.path.basename(path)}], location=(0, 0, 0),
                                          directory=os.path.dirname(path), shader='SHADELESS', relative=False)
        else:
            print("ERROR: MODEL FILE FOR ACTOR NOT VALID")
            sys.exit()

        self.model = bpy.context.selected_objects[0]  # TODO is thitis the best way to do it?
        # Hiding model
        print(self.model)
        self.hiden = False
        self.hide()

        self.id = id
        self.label = label
        #TODO Correcting scaling
        self.size_x = size[0]
        self.size_y = size[1]
        self.size_z = size[2]
        self.model.scale = (self.size_x, self.size_y, self.size_z)

    def hide(self):
        self.model.location = (-200, -200, -200)  # TODO : Make this properly. This is not the best way, fix this(imagine an object that is that big)
        self.hiden = True

    def pose(self, background, z, cam):
        self.rotate(background.conf['rotations'])
        self.move(z, cam, background.pos)
        self.correct_size(background)

    def rotate(self, rotations):
        self.model.rotation_euler = (random.uniform(-rotations[0], rotations[0])/180, random.uniform(-rotations[1], rotations[1])/180, random.uniform(-rotations[2], rotations[2])/180)

    def move(self, z_range, camera, image_x):
        zPos = random.uniform(0, z_range)
        yPos = random.uniform((-1) * ((camera.location[2] - zPos) / camera.location[2]) / 2,
                                ((camera.location[2] - zPos) / camera.location[2]) / 2)
        xPos = random.uniform(image_x * ((camera.location[2] - zPos) / camera.location[2]),
                                abs(image_x) * ((camera.location[2] - zPos) / camera.location[2]))
        self.model.location = (xPos, yPos, zPos)

    def correct_size(self, panel):
            r = random.uniform(panel.conf["objectsSizeRanges"][0], panel.conf["objectsSizeRanges"][1])
            x = panel.img.dimensions[0] * self.size_x / r
            y = panel.img.dimensions[0] * self.size_y / r
            z = panel.img.dimensions[0] * self.size_z / r
            self.model.scale = (x, y, z) # TODO FIX this is temp
            print(self.model.scale)

    # TODO def clone(self):
    # TODO def delete(self):
    # TODO implement max num of actors