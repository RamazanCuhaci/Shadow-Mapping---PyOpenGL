# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

from math_folder.mat3 import Mat3
from math_folder.vec3 import Vec3

class Camera:

    def __init__(self,eye,lookAt,upVector):
        
        self.m_eye = eye
        self.m_lookAt = lookAt
        self.m_upVector = upVector

        self.initialEye = eye
        self.initialLookAt = lookAt
        self.initialUpVector = upVector

        self.camNear = 1.0
        self.camFar = 100.0
        self.camAspect = 1.0
        self.camFov = 60.0
        self.UpdateViewMatrix()
    
    def UpdateViewMatrix(self):
        
        self.m_viewMatrix = Mat3.getViewMatrix(self.m_eye,self.m_lookAt,self.m_upVector)
        

    def SetCameraView(self,eye,lookAt,upVector):
        
        self.m_eye = eye
        self.m_lookAt = lookAt
        self.m_upVector = upVector
        self.UpdateViewMatrix()
    
    def ResetViewMatrix(self):
        self.camNear = 1.0
        self.camFar = 100.0
        self.camAspect = 1.0
        self.camFov = 60.0
        self.m_eye = self.initialEye
        self.m_upVector = self.initialUpVector
        self.UpdateViewMatrix()

    def GetXaxis(self):
        xAxis = Vec3(self.m_viewMatrix[0][0], self.m_viewMatrix[1][0], self.m_viewMatrix[2][0],0)
        return (xAxis*-1)

    def GetZaxis(self):
        zAxis =Vec3(self.m_viewMatrix[0][2], self.m_viewMatrix[1][2], self.m_viewMatrix[2][2],0)
        return (zAxis)