import os as _os

from . import classify
from . import detect
from . import object_tracking
from .representation import Detection

del(cellar)
del(root)
del(representation)

with open(_os.path.abspath(_os.path.dirname(__file__))+'/__doc__','r') as _f:
    __doc__ = _f.read()
