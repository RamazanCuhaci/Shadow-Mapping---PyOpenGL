# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

class Scene:
    def __init__(self,mainCamera):
        self.objects = [] 
        self.mainCamera = mainCamera
        self.active_object_ID = 0
        self.spotLights = []
        self.blinn = True

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        self.objects.remove(obj)

    def set_camera(self, camera):
        self.camera = camera

    def get_camera(self):
        return self.camera

    def set_active_object(self, id):
        
        if id >= len(self.objects) or id < 0:
            print("Object ID is out of range")
            return
        else:
            self.active_object_ID = id
            self.mainCamera.m_lookAt = self.objects[self.active_object_ID].position
            self.mainCamera.UpdateViewMatrix()

    def get_active_object(self):
        return self.objects[self.active_object_ID]

   
    def add_spot_light(self,light):
        self.spotLights.append(light)

    
    def isSpotLightOn(self,lightID):
        if self.spotLights[lightID].on: 
            return "ON" 
        else: 
            return "OFF"
        
    def isSpotLightShadowOn(self,lightID):
        if self.spotLights[lightID].shadowOn: 
            return "ON" 
        else: 
            return "OFF"
        
    def isSpotLightAnimationOn(self,lightID):
        if self.spotLights[lightID].animation: 
            return "ON" 
        else: 
            return "OFF"
        
    def isBlinnOn(self):
        if self.blinn: 
            return "ON" 
        else: 
            return "OFF"