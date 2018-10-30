#TODO check valididity of zrange(zrange being the distance from image)
def posObjRnd(object, zrange, relativeSize, imageX):
     zPos = random.uniform(0,zrange)
     yPos = random.uniform((-1)*((camera.location[2]-zPos)/camera.location[2])/2,((camera.location[2]-zPos)/camera.location[2])/2)
     xPos = random.uniform(imageX*((camera.location[2]-zPos)/camera.location[2]),abs(imageX)*((camera.location[2]-zPos)/camera.location[2]))
     print(zPos)
     print(yPos)
     print(xPos)
     bpy.ops.mesh.primitive_uv_sphere_add(location = (xPos, yPos, zPos), size=0.1)
