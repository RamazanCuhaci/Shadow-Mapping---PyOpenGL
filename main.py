# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import*

from math_folder.vec3 import Vec3

from view import *
from models import *
from light import *
from material import *
from shadow import *


# Global variables
fps = 60
milliseconds_per_frame = int(1000 / fps)

mainView = None

def reshape(w, h):
    glViewport(0, 0, w, h)


def timer_callback(value):
    mainView.update()
    glutPostRedisplay()
    glutTimerFunc(milliseconds_per_frame, timer_callback, 0)

def initScene():
    global mainView
    camPosition = Vec3(-40,20,-20,1)
    camUpAxis = Vec3(0,1,0,0)
    camLookAtposition = Vec3(0,0,0,1)

    myCamera = Camera(camPosition,camLookAtposition,camUpAxis)

    mainScene = Scene(myCamera)
    
    parser = ObjectParser()
    
    textureList =["White.png"]
    objectList = ["Ground.obj","Ball1.obj","Ball2.obj","Tree.obj"]
    
    for shapeName in objectList:
        parser.parse_obj_file(shapeName)
        parser.parse_mtl_file(shapeName[:-4] + ".mtl")  # Assign the corresponding material name
        material = Material(parser.ambient, parser.diffuse, parser.specular, parser.shininess)

        shape = Object(parser.vertices, parser.texture_coords, parser.normals, parser.faces,
                       Vec3(0, 0, 0, 1), parser.name, "defaultVertex.glsl", "defaultFragment.glsl", textureList[0], material)
        mainScene.add_object(shape)
        parser.reset()
     
    
    # SpotLights will look at center of the object
    
    shadow1 = Shadow()
    shadow2 = Shadow()
    
    # For calculating attenuation
    constant = 1.0
    linear = 0.045
    quadratic = 0.0075
    
    spotLightOne = SpotLight(Vec3(0,10,-20,1),shape.position,Vec3(1,1,1,1),4,constant, linear,quadratic, 12.5, 17.5,shadow1)
    spotLightTwo = SpotLight(Vec3(-10,10,0,1),shape.position,Vec3(1,1,1,1),2, constant,linear, quadratic, 30, 17.5,shadow2)

    mainScene.set_active_object(0)  
    mainScene.add_spot_light(spotLightOne)
    mainScene.add_spot_light(spotLightTwo)

    mainView = View(mainScene)

# The main function
def main():
    global mainView
   
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    
    width = 800
    height = 600
    glutInitWindowSize (width, height)
    glutInitWindowPosition (300, 200)
    
    window = glutCreateWindow("CENG487 Multiple Lights with Blinn-Phong Shading")
    
    # Initialize the scene and the view
    initScene()
    
    # need to enable depth testing and depth funct for proper drawing
    glDepthFunc(GL_LEQUAL)
    glEnable(GL_DEPTH_TEST)
 
    glutDisplayFunc(mainView.display)
    glutIdleFunc(mainView.display)
    
    # 60 FPS
    glutTimerFunc(0, timer_callback, 0)
    
    glutReshapeFunc(reshape)
    glutKeyboardFunc(mainView.keyboard)
    glutMouseFunc(mainView.mouse)
    glutMotionFunc(mainView.motion)
    glutMainLoop();

if __name__ == '__main__':

    print("\nHit ESC key to quit."
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
    main()