# CENG 487 Assignment7 by
# Ramazan Cuhaci
# StudentId: 240201047
# Month Year: 01 / 2024

import math
import numpy as np

class Vec3:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.data = np.array([x, y, z, w], dtype=np.float32)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z, self.w)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z, self.w)

    def __mul__(self, scalar):
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar, self.w)

    def __truediv__(self, scalar):
        return Vec3(self.x / scalar, self.y / scalar, self.z / scalar, self.w)

    def length(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalized(self):
        length = self.length()
        if(length==0):
            return self
        else:
            return Vec3(self.x / length, self.y / length, self.z / length, self.w)


    def dot(self, other):
        return (self.x * other.x + self.y * other.y + self.z * other.z)*1.0

    def cross(self, other):
        return Vec3(self.y * other.z - self.z * other.y, self.z * other.x - self.x * other.z, self.x * other.y - self.y * other.x, self.w)*1.0

    def angle(self, other):
        cos_theta = self.dot(other) / (self.length() * other.length())
        return math.acos(cos_theta)

    def projection_to(self, basis):
        dot = self.dot(basis)
        basis_length = basis.length()
        return basis * (dot / (basis_length * basis_length))

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"
    

class Point(Vec3):
    def __init__(self, x, y, z, w=1.0, color=None):
        super().__init__(x, y, z, w)
        self.color = color

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.w))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z, self.w)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z, self.w)

    def __mul__(self, scalar):
        return Point(self.x * scalar, self.y * scalar, self.z * scalar, self.w)

    def __truediv__(self, scalar):
        return Point(self.x / scalar, self.y / scalar, self.z / scalar, self.w)
    
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    
