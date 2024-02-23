# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18,GLUT_BITMAP_HELVETICA_10
from OpenGL.GLU import *
from OpenGL.GL import*
import numpy as np
from math_folder.mat3 import Mat3

from math_folder.vec3 import Vec3
from models import *
from light import *
from material import *
from shadow import *



class View:

    def __init__(self,scene):
        self.scene = scene
        self.blinn = True
        self.initLightParamsAndMaterials()

    def drawText(self,x, y, color,font, text):
        
        # Reset ModelView matrix for text rendering
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Disable depth testing for text rendering
        glDisable(GL_DEPTH_TEST)

        # Set up 2D rendering for text
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, glutGet(GLUT_WINDOW_WIDTH), 0, glutGet(GLUT_WINDOW_HEIGHT))
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))

       
        # Enable depth testing for subsequent rendering (if needed)
        glEnable(GL_DEPTH_TEST)
        
        
        glColor3fv(color)
        glWindowPos2f(x, y)
        
        glutBitmapString(font, text.encode('ascii'))

    def display(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.renderDepthMap()


        for shape in self.scene.objects:
            
            programID = shape.shader.programID
            glUseProgram(programID)
            
            self.calculateLight(programID)
            
            viewMatrix = self.scene.mainCamera.m_viewMatrix
            projMatrix = Mat3.getProjMatrix(self.scene.mainCamera.camNear, self.scene.mainCamera.camFar,
                                            self.scene.mainCamera.camAspect, self.scene.mainCamera.camFov)
            
            self.draw(programID,shape,viewMatrix,projMatrix)
            

        glBindVertexArray(0)
        glUseProgram(0)

        self.drawInfo()

        # Swap buffers
        glutSwapBuffers()


    def calculateLight(self,programID):
        
        # For blinn's specular
        cameraPositionLocation = glGetUniformLocation(programID, "viewPos")
        glUniform3f(cameraPositionLocation, self.scene.mainCamera.m_eye.x, self.scene.mainCamera.m_eye.y, self.scene.mainCamera.m_eye.z)

        # Spotlights switch   
        useSpotLightLocationOne = glGetUniformLocation(programID, "useSpotLightOne")
        glUniform1i(useSpotLightLocationOne, self.scene.spotLights[0].on)
        useSpotLightLocationTwo = glGetUniformLocation(programID, "useSpotLightTwo")
        glUniform1i(useSpotLightLocationTwo, self.scene.spotLights[1].on)
        
        # Blinn's specular switch    
        useBlinnLocation = glGetUniformLocation(programID, "blinn")
        glUniform1i(useBlinnLocation, self.scene.blinn)
            
        # For SpotLight animation and shadow switch
        for i, spotLight in enumerate(self.scene.spotLights):
                glUniform3f(glGetUniformLocation(programID, f"spotLights[{i}].position"), spotLight.position.x, spotLight.position.y, spotLight.position.z)
                glUniform3f(glGetUniformLocation(programID, f"spotLights[{i}].direction"),self.scene.spotLights[i].direction.x, self.scene.spotLights[i].direction.y, self.scene.spotLights[i].direction.z)
                glUniformMatrix4fv(glGetUniformLocation(programID, f"spotLights[{i}].lightProj"), 1, GL_FALSE, self.scene.spotLights[i].getProjection())
                glUniformMatrix4fv(glGetUniformLocation(programID, f"spotLights[{i}].lightView"), 1, GL_FALSE, self.scene.spotLights[i].getView())
                glUniform1i(glGetUniformLocation(programID, f"spotLights[{i}].shadowOn"), self.scene.spotLights[i].shadowOn)
   
   
    def draw(self,programID,shape,viewMatrix,projMatrix):
        # For draw shape
        viewLocation = glGetUniformLocation(programID, "view")
        glUniformMatrix4fv(viewLocation, 1, GL_FALSE, viewMatrix)
        projLocation = glGetUniformLocation(programID, "proj")
        glUniformMatrix4fv(projLocation, 1, GL_FALSE, projMatrix)
            
        modelLocation = glGetUniformLocation(programID, "model")
            
        # OpenGL expects column-major order for matrices
        glUniformMatrix4fv(modelLocation, 1, GL_FALSE, shape.modelMatrix.data.T.flatten())
            
        glBindVertexArray(shape.VAO)
        glDrawArrays(GL_TRIANGLES, 0, shape.vertexSize)
            
    
    def renderDepthMap(self):
    
        for light in self.scene.spotLights:
            
            if light.shadowOn:
            
                depthMapProgramID = light.shadow.depthMapShader.programID
                
                glUseProgram(depthMapProgramID)

                viewMatrix = light.getView()
                projMatrix = light.getProjection()

                viewLocation = glGetUniformLocation(depthMapProgramID, "view")
                projLocation = glGetUniformLocation(depthMapProgramID, "proj")

                # set matrices for view and proj
                glUniformMatrix4fv(viewLocation, 1, GL_FALSE, viewMatrix)
                glUniformMatrix4fv(projLocation, 1, GL_FALSE, projMatrix)

                # setup viewport
                glClearColor(0.0, 0.0, 0.0, 0.0)
                glViewport(0, 0, light.shadow.depthMapRes, light.shadow.depthMapRes)
                glBindFramebuffer(GL_FRAMEBUFFER, light.shadow.depthMapBuffer )
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

                # cull front faces to improve peter panning!
                glEnable(GL_CULL_FACE)
                glCullFace(GL_FRONT)

                # render 
                for shape in self.scene.objects:
                    self.draw(depthMapProgramID, shape, viewMatrix, projMatrix)

                # unbind framebuffer
                glBindFramebuffer(GL_FRAMEBUFFER, 0 )
                glCullFace(GL_BACK) # reset to default
                glDisable(GL_CULL_FACE) # reset to default
        
         # reset program
        glViewport(0, 0, glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT))
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      
        
    def update(self):
        
        if self.scene.spotLights[0].animation:
            
            self.scene.spotLights[0].rotate(3.6)
            
        if self.scene.spotLights[1].animation:
            
            self.scene.spotLights[1].sinusoidalAnimation()

    def drawInfo(self):
        
         # Render text
        self.drawText(4, 50, (1, 1, 1), GLUT_BITMAP_HELVETICA_10,"Spot Light 1: "+
                                                                 "\nLight : " + self.scene.isSpotLightOn(0) + 
                                                                 "\nAnimation : " + self.scene.isSpotLightAnimationOn(0) +
                                                                "\nShadow : " + self.scene.isSpotLightShadowOn(0))
        
        
        self.drawText(100, 65, (1, 1, 1), GLUT_BITMAP_HELVETICA_10,"\nSpot Light 2 : " +
                                                                    "\nLight: "   + self.scene.isSpotLightOn(1) +
                                                                    "\nAnimation : " + self.scene.isSpotLightAnimationOn(1) +
                                                                    "\nShadow : " + self.scene.isSpotLightShadowOn(1))
        
        self.drawText(180, 65, (1, 1, 1), GLUT_BITMAP_HELVETICA_10,"\nBlinn's Specular: "+ self.scene.isBlinnOn())
        
        self.drawText(4,glutGet(GLUT_WINDOW_HEIGHT), (1, 1, 1), GLUT_BITMAP_HELVETICA_10,
                        "\nHit ESC key to quit."
                        + "\nAlt + Left Mouse Button: Rotation around center of the object"
                        + "\nAlt + Right Mouse Button: Zoom in and out"
                        + "\nF key to reset view"
                        + "\n1 key to on/off Spot Light 1's depth map"
                        + "\n2 key to on/off Spot Light 2's depth map"
                        + "\nQ key to on/off Spot Light 1"
                        + "\nW key to on/off Spot Light 2"
                        + "\nA key to on/off animation of Spot Light 1"
                        + "\nS key to on/off animation of Spot Light 2"
                        + "\nB key to on/off Blinn's specular") 
    
    def mouse(self,button, state, xPos, yPos):
    
        global alt_pressed, right_mouse_button_pressed, left_mouse_button_pressed, lastX, lastY
        
        alt_pressed = glutGetModifiers() == GLUT_ACTIVE_ALT
        right_mouse_button_pressed = (button == GLUT_RIGHT_BUTTON) and (state == GLUT_DOWN)
        left_mouse_button_pressed = (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN)
        lastX = xPos
        lastY= yPos
                        
    def motion(self,xPos, yPos):
        global alt_pressed, right_mouse_button_pressed, left_mouse_button_pressed, lastX ,lastY
        
        if alt_pressed:
            
            if right_mouse_button_pressed:
                deltaY = yPos - lastY
                
                if(deltaY < -1):
                    
                    self.scene.mainCamera.camFov -= 1
                    self.scene.mainCamera.UpdateViewMatrix()
                
                elif(deltaY > 1):
                    
                    self.scene.mainCamera.camFov += 1
                    self.scene.mainCamera.UpdateViewMatrix()
        
            elif left_mouse_button_pressed:

                position =self.scene.mainCamera.m_eye
                pivot = self.scene.mainCamera.m_lookAt
                deltaAngleX = ( 2* np.pi/glutGet(GLUT_WINDOW_WIDTH))
                deltaAngleY = (np.pi / glutGet(GLUT_WINDOW_HEIGHT))
        
                xAngle = (lastX-xPos) * deltaAngleX
                yAngle = (lastY-yPos) * deltaAngleY

                cosAngle = self.scene.mainCamera.GetZaxis().dot(self.scene.mainCamera.m_upVector)
                if(cosAngle * np.sign(yAngle)):
                    deltaAngleY = 0
                
                rotationMatrixX = Mat3.identity()
                rotationMatrixX = Mat3.rotate(rotationMatrixX,xAngle,self.scene.mainCamera.m_upVector)
            
                position = (rotationMatrixX * (position-pivot))+pivot
                
                rotationMatrixY = Mat3.identity()
                rotationMatrixY = Mat3.rotate(rotationMatrixY,yAngle,self.scene.mainCamera.GetXaxis())
                
                finalPosition = (rotationMatrixY * (position-pivot))+pivot
                
                self.scene.mainCamera.SetCameraView(finalPosition, self.scene.mainCamera.m_lookAt, self.scene.mainCamera.m_upVector)

            lastX = xPos
            lastY = yPos  

    def initLightParamsAndMaterials(self):
        for obj in self.scene.objects:
            
            programID = obj.shader.programID
            
            glUseProgram(programID)
            
            # SpotLight parameters
            
            for i, spotLight in enumerate(self.scene.spotLights):
                glUniform3f(glGetUniformLocation(programID, f"spotLights[{i}].position"), spotLight.position.x, spotLight.position.y, spotLight.position.z)
                glUniform3f(glGetUniformLocation(programID, f"spotLights[{i}].direction"), spotLight.direction.x, spotLight.direction.y, spotLight.direction.z)
                glUniform3f(glGetUniformLocation(programID, f"spotLights[{i}].color"), spotLight.color.x, spotLight.color.y, spotLight.color.z)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].intensity"), spotLight.intensity)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].constant"), spotLight.constant)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].linear"), spotLight.linear)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].quadratic"), spotLight.quadratic)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].cutOff"), spotLight.cutOff)
                glUniform1f(glGetUniformLocation(programID, f"spotLights[{i}].outerCutOff"), spotLight.outerCutOff)
                glUniformMatrix4fv(glGetUniformLocation(programID, f"spotLights[{i}].lightProj"), 1, GL_FALSE, spotLight.getProjection())
                glUniformMatrix4fv(glGetUniformLocation(programID, f"spotLights[{i}].lightView"), 1, GL_FALSE, spotLight.getView())
                glUniform1i(glGetUniformLocation(programID, f"depthMapTex{i+1}"), spotLight.shadow.depthMapTex)
                # now activate texture unit
                glActiveTexture(GL_TEXTURE0 + spotLight.shadow.depthMapTex)
                glBindTexture(GL_TEXTURE_2D, spotLight.shadow.depthMapTex)
            
            # Material properties
            glUniform1f(glGetUniformLocation(programID, "material.shininess"), obj.material.shininess)
            glUniform3f(glGetUniformLocation(programID, "material.ambient"), obj.material.ambient.x, obj.material.ambient.y, obj.material.ambient.z)
            glUniform3f(glGetUniformLocation(programID, "material.diffuse"), obj.material.diffuse.x, obj.material.diffuse.y, obj.material.diffuse.z)
            glUniform3f(glGetUniformLocation(programID, "material.specular"), obj.material.specular.x, obj.material.specular.y, obj.material.specular.z)
            
            
            
            # reset program
            glUseProgram(0)

    def keyboard(self,key, x, y):
        
        if ord(key) == 27: 
            glutLeaveMainLoop()
            return
        
        if key == b'f' or key == b'F':
            self.scene.mainCamera.ResetViewMatrix()

        if key == b'r' or key == b'R':
            self.scene.get_active_object().resetModelMatrix()


        if key == b'a' or key == b'A':
            self.scene.spotLights[0].animation = not self.scene.spotLights[0].animation
            
        if key == b's' or key == b'S':
            self.scene.spotLights[1].animation = not self.scene.spotLights[1].animation
            
        if key == b'1':
            self.scene.spotLights[0].shadowOn = not self.scene.spotLights[0].shadowOn

        if key == b'2':
            self.scene.spotLights[1].shadowOn = not self.scene.spotLights[1].shadowOn
            
        if key == b'q' or key == b'Q':
            self.scene.spotLights[0].on = not self.scene.spotLights[0].on
        
        if key == b'w' or key == b'W':
            self.scene.spotLights[1].on = not self.scene.spotLights[1].on
        
        if key == b'b':
            self.scene.blinn = not self.scene.blinn
        
        
    
    def object_selecting(self,key):
        self.scene.set_active_object(int(key)-1)

