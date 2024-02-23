# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

import os
from math_folder.vec3 import Vec3

class ObjectParser:
    def __init__(self):
        self.name = None
        self.vertices = []
        self.texture_coords = []
        self.normals = []
        self.faces = []
        self.ambient = None
        self.diffuse = None
        self.specular = None
        self.shininess = None
        

    def parse_obj_file(self, file_path):

        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, file_path)

        with open(file_path, 'r') as file:
            for line in file:
                elements = line.split()

                if not elements:
                    continue  # Skip empty lines

                if elements[0] == 'o':
                    self.name = elements[1].strip()
                elif elements[0] == 'v':
                    vertex = list(map(float, elements[1:4]))
                    vertex.append(1)
                    self.vertices.append(vertex)
                
                elif elements[0] == 'vt':
                    tex_coord = list(map(float, elements[1:3]))
                    self.texture_coords.append(tex_coord)
                
                elif elements[0] == 'vn':
                    normal = list(map(float, elements[1:4]))
                    self.normals.append(normal)
                elif elements[0] == 'f':
                    face = []
                    for elem in elements[1:]:
                        vertex_indices = [int(i)-1 if i != '' else None for i in elem.split('/')]
                        face.append(vertex_indices)
                    self.faces.append(face)
    
    def parse_mtl_file(self, file_path):
        
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, file_path)
        
        with open(file_path, 'r') as file:
            
            for line in file:
                elements = line.split()
                
                if not elements:
                    continue
                
                if elements[0] == 'Ka':
                    self.ambient = Vec3(float(elements[1]),float(elements[2]),float(elements[3]),1)
                elif elements[0] == 'Kd':
                    self.diffuse = Vec3(float(elements[1]),float(elements[2]),float(elements[3]),1)
                elif elements[0] == 'Ks':
                    self.specular = Vec3(float(elements[1]),float(elements[2]),float(elements[3]),1)
                elif elements[0] == 'Ns':
                    self.shininess = float(elements[1])
    
    
    def reset(self):
        self.name = None
        self.vertices = []
        self.texture_coords = []
        self.normals = []
        self.faces = [] 

    def print_info(self):
        print(f"Object Name: {self.name}")
        print("\nVertices:")
        print(type(self.vertices))
        for vertex in self.vertices:
            print(f"  {vertex}")

        print("\nTexture Coordinates:")
        for tex_coord in self.texture_coords:
            print(f"  {tex_coord}")

        print("\nNormals:")
        for normal in self.normals:
            print(f"  {normal}")

        print("\nFaces:")
        for face in self.faces:
            print("  ", end="")
            for vertex_indices in face:
                print(f"({vertex_indices[0]}, {vertex_indices[1]}, {vertex_indices[2]})", end=" ")
            print()        

        print("\nUV")
        for tex in self.texture_coords:
            print(tex)