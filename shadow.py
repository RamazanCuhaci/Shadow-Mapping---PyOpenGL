# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024


from OpenGL.GL import *
from shaders.shaderGL import ShaderGL

class Shadow:
    
    def __init__(self):
        self.depthMapTex = None
        self.depthMapBuffer = None
        self.depthMapRes = 2048
        self.depthMapShader = ShaderGL("depthMapVertexShader.glsl","depthMapFragmentShader.glsl")
        self.initDepthMapBuffer()
        
        
    def initDepthMapBuffer(self):
        self.depthMapTex = glGenTextures(1)
        glActiveTexture(GL_TEXTURE0 + self.depthMapTex)
        glBindTexture(GL_TEXTURE_2D, self.depthMapTex)
        glTexImage2D( 	GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,
                        self.depthMapRes, self.depthMapRes, 0,
                        GL_DEPTH_COMPONENT, GL_FLOAT, None )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        # set border color to 1 which means no shadow since it is the max depth value
        glTexParameterfv( GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0] )

        # create a framebuffer
        self.depthMapBuffer = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapBuffer)
        # bind texture to framebuffers depth attachment
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depthMapTex, 0)

        # tell OpenGL we dont need color buffer as otherwise framebuffer would be incomplete
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE) # to avoid problems with some GPUS supporting only OpenGL3.x

        # unbind buffers for cleanup
        glBindTexture(GL_TEXTURE_2D, 0)  # unbind texture
        glActiveTexture(GL_TEXTURE0)  # set active TU to 0 again

        glBindFramebuffer(GL_FRAMEBUFFER, 0)  # unbind framebuffer
        
    