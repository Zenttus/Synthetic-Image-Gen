import json


class Configuration:

    def __init__(self, path=None):
        if path is None:
            self.conf = dict()
        else:
            with open(path) as f: # TODO : catch exeptions
                self.conf = json.load(f)

    def add_settings(self, path_to_results="./results", res_x=640, res_y=480, label="xml"):
        self.conf['SETTINGS'] = {}
        self.conf['SETTINGS']['PathToResults'] = path_to_results
        self.conf['SETTINGS']['ResX'] = res_x
        self.conf['SETTINGS']['ResY'] = res_y
        self.conf['SETTINGS']['LabelType'] = label

    def add_object(self, path, label, size=[1.0, 1.0]):
        if "OBJECTS" not in self.conf:
            self.conf["OBJECTS"] = []

        obj = dict()
        obj["id"] = len(self.conf["OBJECTS"])
        obj["path"] = path
        obj["label"] = label
        obj["size"] = size

        self.conf["OBJECTS"].append(obj)

    def add_background(self, path, objects, image_size, size_ranges, rotation_ranges, max_objects, lamp_position_range, lampColor):
        if "BACKGROUNDS" not in self.conf:
            self.conf["BACKGROUNDS"] = []

        background = dict()
        background["id"] = len(self.conf["BACKGROUNDS"])
        background["path"] = path
        background["objects"] = objects
        background["size"] = image_size
        background["objectsSizeRanges"] = size_ranges
        background["rotations"] = rotation_ranges
        background["maxObjects"] = max_objects
        background["lampPositionRange"] = lamp_position_range
        background["lampColor"] = lampColor
        # TODO camera zoom

        self.conf["BACKGROUNDS"].append(background)

    # TODO def add_mask()

    def save_conf_to_file(self, path):
        json_string = json.dumps(self.conf)

        with open(path, 'w') as f:
            f.write(json_string)
