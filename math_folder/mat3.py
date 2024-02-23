# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

import numpy as np
from math_folder.vec3 import Vec3

class Mat3:
    def __init__(self, data):
        self.data = data

    @classmethod
    def identity(cls):
        return cls(np.identity(4, dtype=np.float32))

    @classmethod
    def translation(cls, translation_vector):

        return cls(np.array([[1,0,0,translation_vector.x],
                            [0,1,0,translation_vector.y],
                            [0,0,1,translation_vector.z],
                            [0,0,0,1]],dtype=np.float32))
    
    @classmethod
    def rotation_x(cls, angle):
        if np.isclose(angle, 0.0, atol=1e-10):
            return cls.identity()
        else:
            c = np.cos(angle)
            s = np.sin(angle)
            mat = np.array([[1, 0, 0, 0],
                            [0, c, -s, 0],
                            [0, s, c, 0],
                            [0, 0, 0, 1]], dtype=np.float32)
            return cls(mat)

    @classmethod
    def rotation_y(cls, angle):
        if np.isclose(angle, 0.0, atol=1e-10):
            return cls.identity()
        else:
            c = np.cos(angle)
            s = np.sin(angle)
            mat = np.array([[c, 0, s, 0],
                            [0, 1, 0, 0],
                            [-s, 0, c, 0],
                            [0, 0, 0, 1]], dtype=np.float32)
            return cls(mat)

    @classmethod
    def rotation_z(cls, angle):
        if np.isclose(angle, 0.0, atol=1e-10):
            return cls.identity()
        elif np.isclose(angle, np.pi / 2, atol=1e-10):
            return cls(np.array([[0, -1, 0, 0],
                                [1, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]], dtype=np.float32))
        elif np.isclose(angle, -np.pi / 2, atol=1e-10):
            return cls(np.array([[0, 1, 0, 0],
                                [-1, 0, 0, 0],
                                [0, 0, 1, 0],
                                [0, 0, 0, 1]], dtype=np.float32))
        else:
            c = np.cos(angle)
            s = np.sin(angle)
            mat = np.array([[c, -s, 0, 0],
                            [s, c, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, 1]], dtype=np.float32)
            return cls(mat)
    
    def rotate(self, angle, axis):

        # Normalize the axis
        axis = axis.normalized()

        # Calculate components of the rotation matrix
        c = np.cos(angle)
        s = np.sin(angle)
        t = 1 - c
        x, y, z = axis.x, axis.y, axis.z

        # Build the rotation matrix
        rotation_matrix = np.array([
            [t * x**2 + c, t * x * y - s * z, t * x * z + s * y, 0],
            [t * x * y + s * z, t * y**2 + c, t * y * z - s * x, 0],
            [t * x * z - s * y, t * y * z + s * x, t * z**2 + c, 0],
            [0, 0, 0, 1]
        ])

        # Multiply the input matrix by the rotation matrix
        result_matrix = Mat3(rotation_matrix) * self
        return result_matrix
    
    @classmethod
    def scaling(cls, scale_vector):
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = scale_vector.data[0]
        mat[1, 1] = scale_vector.data[1]
        mat[2, 2] = scale_vector.data[2]
        return cls(mat)

    def transpose(self):
        return Mat3(self.data.T)

    def __mul__(self, other):
        if isinstance(other, Mat3):
            result_data = np.dot(self.data, other.data)
            return Mat3(result_data)
        elif(isinstance(other, Vec3)):
            columnMatrix = self.transpose()
            result_data = np.dot(columnMatrix.data,other.data)
            return Vec3(result_data[0],result_data[1],result_data[2],result_data[3])
        
    def inverse(self):
        inv_data = np.linalg.inv(self.data)
        return Mat3(inv_data)
    

    def getProjMatrix(near, far, aspect, fov):
        f = np.reciprocal(np.tan(np.divide(np.deg2rad(fov), 2.0)))
        base = near - far
        term_0_0 = np.divide(f, aspect)
        term_2_2 = np.divide(far + near, base)
        term_2_3 = np.divide(np.multiply(np.multiply(2, near), far), base)

        # https://en.wikibooks.org/wiki/GLSL_Programming/Vertex_Transformations
        return  np.array([	term_0_0, 0.0, 0.0, 0.0,
                                0.0, f, 0.0, 0.0,
                                0.0, 0.0, term_2_2, -1,
                                0.0, 0.0, term_2_3, 0.0], dtype='float32')

    def getViewMatrix(camPosition,targetPosition,camUpAxis):

        camZAxis = (targetPosition-camPosition).normalized()
        camXAxis = (camZAxis.cross(camUpAxis)).normalized()
        camYAxis = camXAxis.cross(camZAxis)

        rotMat = np.array([	camXAxis.x, camYAxis.x, (camZAxis.x)*-1, 0.0,
                                camXAxis.y, camYAxis.y, (camZAxis.y)*-1, 0.0,
                                camXAxis.z, camYAxis.z, (camZAxis.z)*-1, 0.0,
                                0.0, 0.0, 0.0, 1.0], dtype='float32').reshape(4,4)

        traMat = np.array([	1.0, 0.0, 0.0, 0.0,
                                0.0, 1.0, 0.0, 0.0,
                                0.0, 0.0, 1.0, 0.0,
                                (camPosition.x)*-1, (camPosition.y)*-1, (camPosition.z)*-1, 1.0], dtype='float32').reshape(4,4)

        

        return traMat.dot(rotMat)

    def getModelMatrix(objectPosition):
        return np.array([	1.0, 0.0, 0.0, 0.0,
                                0.0, 1.0, 0.0, 0.0,
                                0.0, 0.0, 1.0, 0.0,
                                objectPosition.x, objectPosition.y, objectPosition.z, 1.0], dtype='float32')

 