import bpy
import random


class Actor:

    def __init__(self, id, path, label, size):
        # Loading model
        # bpy.ops.import_scene.autodesk_3ds(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")  # TODO multiple object types

        for obj in bpy.data.objects:  # Deselect all objects
            obj.select = False
        bpy.ops.import_mesh.stl(filepath=path)
        self.model = bpy.context.selected_objects[0]  # TODO is this the best way to do it?
        # Hiding model
        self.hiden = False
        self.hide()

        self.id = id
        self.label = label
        self.size_x = size[0]
        self.size_y = size[1]
        self.size_z = size[2]
        self.model.scale = (self.size_x, self.size_y, self.size_z)

    def hide(self):
        self.model.location = (0, 0, -20)  # TODO : Make this properly. This is not the best way, fix this(imagine an object that is that big)
        self.hiden = True

    def pose(self, background, z, cam):
        self.rotate(background.conf['rotations'])
        self.move(z, cam, background.pos)

    def rotate(self, rotations):
        self.model.rotation_euler = (random.uniform(-rotations[0], rotations[0])/180, random.uniform(-rotations[1], rotations[1])/180, random.uniform(-rotations[2], rotations[2])/180)

    def move(self, z_range, camera, image_x):
        zPos = random.uniform(0, z_range)
        yPos = random.uniform((-1) * ((camera.location[2] - zPos) / camera.location[2]) / 2,
                                ((camera.location[2] - zPos) / camera.location[2]) / 2)
        xPos = random.uniform(image_x * ((camera.location[2] - zPos) / camera.location[2]),
                                abs(image_x) * ((camera.location[2] - zPos) / camera.location[2]))
        self.model.location = (xPos, yPos, zPos)

    # TODO def clone(self):
    # TODO def delete(self):
    # TODO implement max num of actors