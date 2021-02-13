#!/usr/bin/env python
from icecube import icetray
from icecube.load_pybindings import load_pybindings
load_pybindings(__name__, __path__)

try:
    import icecube.tableio
    import converters
except ImportError:
    pass

del load_pybindings

import modules
import segments

del icetray
