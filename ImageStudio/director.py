import json
from legacy import toolbox


class Director:

    def __init__(self, conf_file='config.json'):

        with open(conf_file, 'r') as f:
            config = json.load(f)

        # Loading settings
        x_resolution = config['SETTINGS']['ResX']
        y_resolution = config['SETTINGS']['ResY']
        self.label_type = config['SETTINGS']['LabelType']
        self.results_path = config['SETTINGS']['PathToResults']

        self.scene, self.camera, self.camera = toolbox.prepare_scene(x_resolution, y_resolution)
        self.backgrounds = toolbox.load_backgrounds(config['SETTINGS']['PathToBackgrounds'])

        self.scene.cycles.device = 'GPU'  # Comment this if not using GPU # TODO implement this properly

    # TODO def render()
    # TODO def get_objects_coordinates(self):