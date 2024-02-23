# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import*
import os

class ShaderGL:

    def __init__(self,vertexShader, fragmentShader):
        self.vertexShader = vertexShader
        self.fragmentShader = fragmentShader
        
        self.initProgram()
       
    
    def createProgram(self,shaderList):
        programID = glCreateProgram()

        for shader in shaderList:
            glAttachShader(programID, shader)

        glLinkProgram(programID)

        status = glGetProgramiv(programID, GL_LINK_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetProgramInfoLog(programID)
            print(b"Linker failure: \n" + strInfoLog)

        # important for cleanup
        for shaderID in shaderList:
            glDetachShader(programID, shaderID)

        return programID

    def initProgram(self):
        shaderList = []

        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        shaderList.append(self.createShader(GL_VERTEX_SHADER, self.openShader(os.path.join(script_directory, self.vertexShader))))
        shaderList.append(self.createShader(GL_FRAGMENT_SHADER, self.openShader(os.path.join(script_directory, self.fragmentShader))))

        self.programID = self.createProgram(shaderList)
        
        
        for shader in shaderList:
            glDeleteShader(shader)


    def createShader(self,shaderType, shaderCode):
        
        shaderID = glCreateShader(shaderType)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)
        glShaderSource(shaderID, shaderCode)
        glCompileShader(shaderID)

        status = None
        glGetShaderiv(shaderID, GL_COMPILE_STATUS, status)
        if status == GL_FALSE:

            strInfoLog = glGetShaderInfoLog(shaderID)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            print(b"Compilation failure for " + strShaderType + b" shader:\n" + strInfoLog)

        return shaderID

    def openShader(self,shaderFile):
        with open(shaderFile, 'r') as myfile:
            data = myfile.read()
        return data