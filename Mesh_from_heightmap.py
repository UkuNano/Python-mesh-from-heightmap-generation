from PIL import Image
import random

def mapX(value):
    return (float(value)/vertX) * sizeX

def mapZ(value):
    return (float(value)/vertZ) * sizeZ

def map_height(value):
    return (float(value)/255) * maxheight

# CONFIGURATION VALUES
# Size in vertices
vertX = 50 + 1
vertZ = 50 + 1

# Size in units
sizeX = 1
sizeZ = 1

smooth_shading = False

# Max height in units
maxheight = 1.0

randomness = 0

grid_texture_coordinates = False
texture = True # Will the mesh have any texture

# Use \\ instead of \ in paths like C:\\ to aviod escaped characters like \n
heightmap = Image.open(r"")
texture_path = ""
mtl_file_path = ""
mesh_file_path = ""
# END OF CONFIGURATION VALUES

hm_width, hm_height = heightmap.size

hole_verts = [] # Vertices at transparent spots

if texture == True:
    mtl_file = open(mtl_file_path, "w")
    mtl_file.write("newmtl texture\nKa 1.0 1.0 1.0\nKd 1.0 1.0 1.0\nKs 0.0 0.0 0.0\nNs 10.0\nd 1.0\nillum 2\nmap_Kd " + texture_path)
    mtl_file.close()
    
    file = open(mesh_file_path, "w")
    file.write("# Comment\nmtllib " + mtl_file_path + "\n")
else:
    file = open(mesh_file_path, "w")
    file.write("# Comment\n")

file = open(mesh_file_path, "a")

# Create the vertices
print("Creating vertices...")

for x in range(vertX):
    for z in range(vertZ):
        pixel_val = heightmap.getpixel((x/float(vertX) * hm_width, z/float(vertZ) * hm_height))
        alpha_val = pixel_val[-1]
        
        if alpha_val == 0:
            hole_verts.append((x - 1) * vertZ + z)
        
        if type(pixel_val) != int:
            pixel_val = pixel_val[0]
        
        height = pixel_val + random.randint(0, randomness)
        height = map_height(height)
        
        file.write("v " + str(mapX(x)) + " " + str(height) + " " + str(mapZ(z)) + "\n")

if texture == True:
    print("Creating texture coordinates...")
    
    if grid_texture_coordinates == False:
        for x in range(vertX): # Texture coordinates
            for z in range(vertZ):
                file.write("vt " + str(x/float(vertX)) + " " + str(z/float(vertZ)) + "\n")
    else:
        file.write("vt 0.0 0.0\nvt 1.0 0.0\nvt 0.0 1.0\nvt 1.0 1.0\n")

# Enable/disable smooth shading
if smooth_shading == True:
    file.write("s on\n")
else:
    file.write("s off\n")

file.write("usemtl texture\n")

# Create the triangles
print("Creating faces...")

for i in range(vertX * (vertZ - 1)):
    if i % vertZ != 0:
        if texture == True:
            if grid_texture_coordinates == False:
                if not (i in hole_verts) and not (i + 1 in hole_verts) and not (i + vertZ in hole_verts):
                    file.write("f " + str(i) + "/" + str(i) + " " + str(i + 1) + "/" + str(i + 1) + " " + str(i + vertZ) + "/" + str(i + vertZ) + "\n")

                if not (i + 1 in hole_verts) and not (i + vertZ in hole_verts) and not (i + vertZ + 1 in hole_verts):
                    file.write("f " + str(i + 1) + "/" + str(i + 1) + " " + str(i + vertZ + 1) + "/" + str(i + vertZ + 1) + " " + str(i + vertZ) + "/" + str(i + vertZ) + "\n")
            else:
                if not (i in hole_verts) and not (i + 1 in hole_verts) and not (i + vertZ in hole_verts):
                    file.write("f " + str(i) + "/1 " + str(i + 1) + "/2 " + str(i + vertZ) + "/3\n")

                if not (i + 1 in hole_verts) and not (i + vertZ in hole_verts) and not (i + vertZ + 1 in hole_verts):
                    file.write("f " + str(i + 1) + "/2 " + str(i + vertZ + 1) + "/4 " + str(i + vertZ) + "/3\n")
        else:
            if not (i in hole_verts) and not (i + 1 in hole_verts) and not (i + vertZ in hole_verts):
                file.write("f " + str(i) + " " + str(i + 1) + " " + str(i + vertZ) + "\n")

            if not (i + 1 in hole_verts) and not (i + vertZ in hole_verts) and not (i + vertZ + 1 in hole_verts):
                file.write("f " + str(i + 1) + " " + str(i + vertZ + 1) + " " + str(i + vertZ) + "\n")

file.close()
print("Done")

raw_input()
