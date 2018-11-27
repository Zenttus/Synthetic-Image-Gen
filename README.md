# Synthetic Data Gen
 Synthetic Data Gen(SDG) is a group of python scripts that uses Blender to generate images. With the goal to generate images of objects that there's no enough data available to train vision models. The code has implemented anti biasing techniques like random positioning and different light conditions.
 This project is still on its initial stages, a lot of work is still to be done and there's a lot of room to improvement.

# Setting Up
 1. Install Blender
 2. Python module installation in blender
    1. lxml
 3. Download Repo
# Running Demo
* "C:\Program Files\Blender Foundation\Blender\blender.exe" --background --python datagen.py
# How to see results
Tool for looking at pics and labels. (https://github.com/tzutalin/labelImg)
# Custom data?
* Open the config.json, edit the lines that have the path of the object to your own. Then change the path of the background images to your own too. This folder should have the images that you selected as background. You can also change the number of images per background image, add multiple objects and also disable rotation.
# Now what? TRAIN!!!
* Darkflow(tested on) https://github.com/thtrieu/darkflow
* Darknet (need testing) https://pjreddie.com/darknet/
# Future Work
 * Clean the repo
 * Connect DB
 * Clean up
 * More bias mitigation techniques
 * Output for more vision algorithms
