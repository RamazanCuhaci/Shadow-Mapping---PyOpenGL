# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

import numpy as np
from shaders.shaderGL import ShaderGL
from OpenGL.GL import *
from math_folder.mat3 import Mat3
from PIL import Image
import os

        
elementSize = np.dtype(np.float32).itemsize

class Object:
    def __init__(self,vertices,texture_coords,normals,faces,
                position, name, vertexShader, fragmentShader,texturePath,material,color=None, rotationY=0 ):
        
        self.vertices = vertices
        self.texture_coords = texture_coords
        self.normals = normals
        self.faces = faces
        self.material = material
        
        if color == None:
            self.colors = np.array([1, 1, 1, 1])
        else:
            self.colors = color
        self.vertexSize = 0

        self.position = position
        self.name = name
        self.rotationY = rotationY
        self.finalData = self.initVertexBufferData()
        
        self.texturePath = texturePath
        self.textureBlendRatio = 0.0
        self.shader = ShaderGL(vertexShader,fragmentShader)
        self.modelMatrix = Mat3.translation(self.position)
        self.VAO, self.VBO = self.initVertexBuffer()
        self.initTextures()


    def initVertexBufferData(self):
        
        finalVertexPositions = []
        finalVertexColors = []
        finalVertexUvs = []
        finalVertexNormals = []

        triangleFaces = []
        for face in self.faces:
            if(len(face)==4):
                triangleFaces.extend([[face[0],face[1],face[2],face[2],face[3],face[0]]])
                self.vertexSize += 6
            else:
                triangleFaces.extend([[face[0],face[1],face[2]]])
                self.vertexSize += 3

        self.faces = triangleFaces
        faceColors = np.tile(self.colors, (self.vertexSize,1))

        faceID = 0
        for face in self.faces:

            for vertex in face:
                finalVertexPositions.extend(self.vertices[vertex[0]])
                finalVertexColors.extend(faceColors[faceID])
                
            faceID +=1
            
            for uv in face:
                finalVertexUvs.extend(self.texture_coords[uv[1]])
            
            for normal in face:
                finalVertexNormals.extend(self.normals[normal[2]])

        return np.array(finalVertexPositions + finalVertexColors + finalVertexUvs + finalVertexNormals, dtype='float32')


    def initVertexBuffer(self):

       
        VAO= glGenVertexArrays(1)
        glBindVertexArray(VAO)

        VBO = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.finalData, GL_STATIC_DRAW)
            
        offset = 0
        # Specify the layout of the vertex data
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, elementSize*4, ctypes.c_void_p(offset))


        # Specify colors
        offset += elementSize * 4 * self.vertexSize
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 4, GL_FLOAT, GL_FALSE, elementSize*4, ctypes.c_void_p(offset))
        

        #Specify UV
        offset += elementSize * 4 * self.vertexSize
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, elementSize*2, ctypes.c_void_p(offset))


        # define normals which are passed in location 3 - they start after all positions, colors and uvs and has four floats per vertex
        offset += elementSize * 2 * self.vertexSize
        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, elementSize * 3, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(3)

        # Unbind VAO
        glBindVertexArray(0)
        
        return VAO,VBO

 
    def initTextures(self):
        glUseProgram(self.shader.programID)

        texID = self.loadTexture(self.texturePath)
        # set shader stuff
        texLocation = glGetUniformLocation(self.shader.programID, "tex1")
        glUniform1i(texLocation, texID)

        # now activate texture units
        glActiveTexture(GL_TEXTURE0 + texID)
        glBindTexture(GL_TEXTURE_2D, texID)

        # reset program
        glUseProgram(0)
    

    def loadTexture(self,texFilename):
	    
        script_directory = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_directory, texFilename)
        
        # load texture - flip int verticallt to convert from pillow to OpenGL orientation
        image = Image.open(file_path).transpose(Image.FLIP_TOP_BOTTOM)
       
        texID = glGenTextures(1)
        # bind to the new id for state
        glBindTexture(GL_TEXTURE_2D, texID)

        # set texture params
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        # copy texture data
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE,
                        np.frombuffer( image.tobytes(), dtype = np.uint8 ) )
        glGenerateMipmap(GL_TEXTURE_2D)

        return texID


    def rotateY(self):
        self.rotationMatrix = Mat3.rotation_y(np.radians(self.rotationY))
        self.modelMatrix = self.modelMatrix * self.rotationMatrix 
    
    def resetModelMatrix(self):
        self.modelMatrix = Mat3.translation(self.position)
        self.rotationX = 0
        self.rotationY = 0


   