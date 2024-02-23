# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

import numpy as np
from math_folder.vec3 import Vec3
from math_folder.mat3 import Mat3

class SpotLight:

    def __init__(self,position,lookUp,color,intensity,constant,linear,quadratic,cone,penumbra,shadow):
        self.position = position
        self.lookUp = lookUp
        self.direction = lookUp-position
        self.color = color
        self.intensity = intensity
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        self.cutOff = np.cos(np.radians(cone))
        self.outerCutOff = np.cos(np.radians(cone+penumbra))
        
        
        self.lightCamAspect = 1.0
        self.lightCamFov = 2 * (cone+penumbra)
        self.lightCamNear = 1.0
        self.lightCamFar = 100.0
        self.lightUpAxis = Vec3(0,1,0,0)
        self.shadow = shadow
    
        self.shadowOn = True
        self.animation = False
        
        self.angle = 0
        
        self.on = True

    def rotate(self,angle):
        x = self.position.x * np.cos(np.radians(angle)) + self.position.z * np.sin(np.radians(angle))
        z = self.position.z * np.cos(np.radians(angle)) - self.position.x * np.sin(np.radians(angle))
        
        self.position.x = x
        self.position.z = z

        self.direction = self.lookUp - self.position
        
        
    def sinusoidalAnimation(self):
        self.angle +=5
        self.position.z = 10 * np.sin(np.radians(self.angle))
        
    def getView(self):
        return Mat3.getViewMatrix(self.position,self.direction,self.lightUpAxis)
    
    def getProjection(self):
        return Mat3.getProjMatrix(self.lightCamNear,self.lightCamFar,self.lightCamAspect,self.lightCamFov)
        

class DirectionalLight:

    def __init__ (self,direction, color,intensity):
        self.direction = direction
        self.color = color
        self.intensity = intensity
        self.on = True

class PointLight:

    def __init__ (self,position, color,intensity,constant,linear,quadratic):
        self.position = position
        self.color = color
        self.intensity = intensity
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
        self.on = True


