import src.exceptions as exceptions

class BoxContainer():
    """ Container that allows to store and access elements in two dimensional grid; the memory consumption is linear with the number of elements; average time complexity for access/removal is O(1)"""

    def __init__(self, width, height):
        """ width and height of the creating container,
        it's important just for bound testing;
        it doesn't affect the memory consumption """
        self._width=width
        self._height=height
        self._cont={}

    def insert(self, x, y, val):
        """ insert value on the given position,
            if the position is not empty, the value is overwritten """
        if x>=self._width or y>=self._height:
            raise exceptions.OutOfRangeError("Inserting out of range into a box container ({}, {})".format(x,y))

        if not x in self._cont:
            self._cont[x]={}
        self._cont[x][y]=val

    def clear(self):
        """ removes all elements in the container """
        self._cont={}

    def get(self, x, y):
        """ get an element, returns the actual value or None if there's no element on the given position"""
        if not x in self._cont or not y in self._cont[x]:
            return None
        return self._cont[x][y]

    def remove(self, x, y):
        """remove an element"""
        if x in self._cont and y in self._cont[x]:
            self._cont[x][y]=None

    def __iter__(self):
        """ this makes the container iterable
        try: for el in instance_of_container"""
        for x in self._cont:
            for y in self._cont[x]:
                if not self._cont[x][y]==None:
                    yield x,y,self._cont[x][y]
