import bpy

class Actor:

    def __init__(self, id, path, label, size):
        # Loading model
        bpy.ops.import_scene.autodesk_3ds(filepath=path, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl")
        for obj in bpy.data.objects:  # Deselect all objects
            obj.select = False
        self.model = bpy.data.objects['Box001']
        # Hiding model
        self.hide()

        self.id = id
        self.label = label
        self.size_x = size[0]
        self.size_y = size[1]

    def hide(self):
        self.model.location = (0, 0, -20)  # TODO : Make this properly. This is not the best way, fix this(imagine an object that is that big)

    # TODO def set_size(self):
    # TODO def rotate(self):
    # TODO def move(self):
    # TODO def clone(self):
    # TODO def delete(self):
    # TODO implement max num of actors