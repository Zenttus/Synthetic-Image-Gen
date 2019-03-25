# TODO Documentation standards
# TODO Fix readme
# TODO FUTURE more labeling modes
# TODO Make background black
# TODO FUTURE implemente reflections

import os, sys
# TODO: Fix this annoying thing
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from ImageStudio.configuration import Configuration
from ImageStudio.director import Director
import bpy

# CONF FOR BOUYS
# conf = Configuration()
# conf.add_settings('D:\\roboboat training data')
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\Buoy 950410 Red.obj', 'tsmbred', [0.4572, 0.4572, 1.2446])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\Buoy 46104 White.obj', 'tsmbwhite', [0.4572, 0.4572, 1.2446])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\Buoy 950400 Green.obj', 'tsmbgreen', [0.4572, 0.4572, 1.2446])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\pr.obj', 'polybr', [0.639, 0.639, 0.639])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\pb.obj', 'polybb', [0.639, 0.639, 0.639])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\pg.obj', 'polybg', [0.639, 0.639, 0.639])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\py.obj', 'polyby', [0.639, 0.639, 0.639])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\pn.obj', 'polybn', [0.639, 0.639, 0.639])
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\dock.obj', 'dock')
# conf.add_backgrounds_from_directory('D:\\backgrounds_sig\\*', ['tsmbred', 'tsmbwhite', 'tsmbgreen', 'polybr', 'polybb', 'polybg', 'polyby', 'polybn', 'dock'], 2.0, [0.1, 1.0], [10, 10, 10], 5, [[0, 5], [-10, 10], [2, 10]], [1, 1, 1])

# CONF FOR DRONE
conf = Configuration()
conf.add_settings('D:\\drone traininge data')
conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\zero.jpeg', 'zero')
conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\uno.jpeg', 'one')
conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\dos.jpeg', 'two')
conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\tres.jpeg', 'three')
conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\cuatro.jpeg', 'four')
conf.add_backgrounds_from_directory('D:\\drone_backgrounds\\*', ['zero', 'one', 'two', 'three', 'four'], 10.0, [10.0, 20.0], [10, 10, 10], 2, [[0, 5], [-10, 10], [2, 10]], [1, 1, 1])

# CONF FOR SUB
# conf = Configuration()
# conf.add_settings('D:\\image_results')
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\Gate.obj', 'gate')
# conf.add_actor('D:\\GitProjects\\Synthetic-Image-Gen\\models\\Bouy.obj', 'bouy')
# conf.add_backgrounds_from_directory('D:\\background_img_underwater\\2018-07-31_07_49_55.310060_x264 (3-22-2019 12-22-05 PM)\\*', ['gate', 'bouy'], 1.0, [0.001, 2.0], [180,180,180], 2, [[0, 5], [-10, 10], [2, 10]], [1, 1, 1])
conf.save_conf_to_file()

# This is where everything runs
director = Director()
director.action()