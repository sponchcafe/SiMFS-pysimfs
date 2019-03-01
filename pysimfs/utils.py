from collections import namedtuple
import os
import uuid

import numpy as np

########################################################################### 
def new_filename(name: str) -> str:
    ''' Create a rondomized filename based on a readable name

    Arguments
    name : file base name 

    Returns
    Absolute path with a basename of the form "name_<8 random chars>"
    '''

    uid = '_'.join((name, str(uuid.uuid1())[:8]))
    return os.path.abspath(uid)



class GridData():

    HEADER_SIZE = 9*8
    LinSpace_t = np.dtype([('min', 'f8'),('max', 'f8'),('n', 'i8')])
    Delta = namedtuple('Delta', ['x', 'y', 'z'])
    LinSpace = namedtuple('LinSpace', ['min', 'max', 'n'])
    GridSpace = namedtuple('GridSpace', ['x', 'y', 'z'])

    def __init__(self, filename, dtype='f8'):
        self.filename = filename
        self.dtype = dtype
        self._load()
        self.data = self._raw[GridData.HEADER_SIZE:].view(self.dtype)
        self.data = self.data.reshape(*(d.n for d in self.shape))

    def _load(self):
        self._raw = np.fromfile(self.filename, dtype='b')

    @property
    def shape(self):
        linspaces = self._raw[:GridData.HEADER_SIZE].view(GridData.LinSpace_t)
        return GridData.GridSpace(*(GridData.LinSpace(*d) for d in linspaces))

    @property
    def delta(self):
        return GridData.Delta(*( (d.max-d.min)/(d.n-1) for d in self.shape))
    
    def _ix(self, x):
       return self._index_of(x, self.shape.x)
       
    def _iy(self, y):
        return self._index_of(y, self.shape.y)
  
    def _iz(self, z):
        return self._index_of(z, self.shape.z)
 
    @staticmethod
    def _index_of(d: float, space: LinSpace) -> int:
        index = int((d-space.min)/((space.max-space.min)/space.n))
        if index >= space.n:
            return space.n-1
        if index < 0:
            return 0
        return index
