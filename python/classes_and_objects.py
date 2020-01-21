class vector_class(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return vector_class(self.x * other, 
                                self.y * other,
                                self.z * other)
        elif isinstance(other, vector_class):
            return vector_class(self.x * other.x,
                                self.y * other.y,
                                self.z * other.z)

    def __repr__(self):
        return 'Vector < {x}:{y}:{z} >'.format(x=self.x, y=self.y, z=self.z)

v1 = vector_class(1, 2, 3)
v2 = vector_class(3, 2, 4)
v3 = v1 * v2
print v3.x, v3.y, v3.z

v4 = v1 * 5.2
print v4