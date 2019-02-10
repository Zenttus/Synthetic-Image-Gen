import os
from random import random
import bpy
# TODO implement masks


class Panel:

    def __init__(self, img_path, conf):
        for obj in bpy.data.objects:
            obj.select = False
        # Load New Image
        bpy.ops.import_image.to_plane(files=[{"name": os.path.basename(img_path)}], location=(0, 0, 0),
                                      directory=os.path.dirname(img_path), shader='SHADELESS', relative=False)
        self.img = bpy.context.object
        self.img.location = (0, 0, 0)
        self.pos = self.img.data.vertices[0].co[0]
        self.conf = conf

    def change_background(self, img_path, new_conf):
        for obj in bpy.data.objects:
            obj.select = False
        self.img.select = True
        bpy.ops.object.delete(use_global=False)
        bpy.ops.import_image.to_plane(files=[{"name": os.path.basename(img_path)}], location=(0, 0, 0),
                                      directory=os.path.dirname(img_path), shader='SHADELESS', relative=False)
        self.img = bpy.context.object
        self.img.location = (0, 0, 0)
        self.pos = self.img.data.vertices[0].co[0]
        self.conf = new_conf

    def update_camera(self, camera):
        camera_constant = 2.1892349261  # Based on the camera angle(if field of view changes this must also change)
        # TODO: get this constant via code.
        camera.location = (0, 0, abs(self.pos) * camera_constant) #TODO: add randomness
