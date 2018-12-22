

class Scenario:

    def __init__(self, directory_path, file_name):
        # Load New Image
        bpy.ops.import_image.to_plane(files=[{"name": file_name}], location=(0, 0, 0),
                                      directory=directory_path, shader='SHADELESS', relative=False)
        self.img = bpy.context.object
        self.img.location = (0, 0, 0)
        self.pos = self.img.data.vertices[0].co[0]

    # TODO def change_background(self):
    #   if old_img is not None:
    #        old_img.select = True
    #        bpy.ops.object.delete(use_global=False)
    # TODO implement masks

    # TODO def update_light(self):
    # TODO def take_image(self):