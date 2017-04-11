import src.exceptions as exceptions


# TODO cached array of values for faster get() access? instead of average constant always constant
class BoxContainer():
    def __init__(self, width, height):
        self._width=width
        self._height=height
        self._cont={}

    def insert(self, x, y, val):
        if x>=self._width or y>=self._height:
            raise exceptions.OutOfRangeError("Inserting out of range into a box container")

        if not x in self._cont:
            self._cont[x]={}
        self._cont[x][y]=val

    def clear(self):
        self._cont={}

    def get(self, x, y):
        if not x in self._cont or not y in self._cont[x]:
            return None
        return self._cont[x][y]

    # TODO maybe better to remove straight off??
    def remove(self, x, y):
        if x in self._cont and y in self._cont[x]:
            self._cont[x][y]=None

    def __iter__(self):
        for x in self._cont:
            for y in self._cont[x]:
                if not self._cont[x][y]==None:
                    yield x,y,self._cont[x][y]
