# TODO Documentation standards
# TODO Fix readme
# TODO FUTURE more labeling modes
# TODO Make background black
# TODO Make it for more than one type of object (stl, 3ds, etc)
# TODO Test textures on object
# TODO FUTURE implemente reflections
# TODO test on other OSs
# TODO change to "panel"?

from ImageStudio.configuration import Configuration
from ImageStudio.director import Director
import bpy

# Configuration
#if len(sys.argv) > 1: #TODO fix this cuz if using python from blender extra parameters are required
#    conf = Configuration(sys.argv[1])
#else:  # TODO changer this to a more standard case, this is currently set for specific project

conf = Configuration()
conf.add_settings('C:\\Users\\Owrn\\Desktop\\Roboboat images\\backgrounds_sig\\results')
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\Buoy 950410 Red.obj', 'tsmbred', [0.4572, 0.4572, 1.2446])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\Buoy 46104 White.obj', 'tsmbwhite', [0.4572, 0.4572, 1.2446])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\Buoy 950400 Green.obj', 'tsmbgreen', [0.4572, 0.4572, 1.2446])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\pr.obj', 'polybr', [0.639, 0.639, 0.639])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\pb.obj', 'polybb', [0.639, 0.639, 0.639])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\pg.obj', 'polybg', [0.639, 0.639, 0.639])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\py.obj', 'polyby', [0.639, 0.639, 0.639])
conf.add_actor('C:\\Users\\Owrn\\Desktop\\Roboboat images\\models\\pn.obj', 'polybn', [0.639, 0.639, 0.639])


# TODO : platfrom
# TODO: if model is image, import as plane
conf.add_backgrounds_from_directory('C:\\Users\\Owrn\\Desktop\\Roboboat images\\backgrounds_sig\\*', ['tsmbred', 'tsmbwhite', 'tsmbgreen', 'polybr', 'polybb', 'polybg', 'polyby', 'polybn'], 2.0, [0.1, 1.0], [10, 10, 10], 10, [[0, 5], [-10, 10], [2, 10]], [1, 1, 1])

conf.save_conf_to_file()

# This is where everything runs
director = Director()
director.action()