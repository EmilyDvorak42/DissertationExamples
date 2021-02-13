#!/usr/bin/env python

import os,sys


from I3Tray import *
from icecube import icetray, dataclasses, dataio, phys_services, rock_bottom


from optparse import OptionParser
parser = OptionParser()
parser.add_option("-o", "--outputprefix", action="store", type="string", dest="output", help="Output file name", metavar="FILE")

(options, inputFiles) = parser.parse_args()

gcdfile = ["/Users/javierg/IceCubeData/GeoCalibDetectorStatus_IC79.55380_L2a.i3"]
outfile=options.output

# Instantiate a tray
tray = I3Tray()

tray.AddModule( 'I3Reader', 'Reader', FilenameList = gcdfile + inputFiles)

tray.AddModule("I3IceTopLTPFinder", "ltp-finder",
               SLCPulses = 'IceTopSelectedSLC',
               HLCPulses = 'IceTopSelectedHLC',
               Seed = 'IceTopLDFChi2',
               LDFType = rock_bottom.ldf.LogLog()
               )

tray.AddModule("I3Writer", "i3-writer",
               Filename = "%s.i3"%outfile,
               streams = [icetray.I3Frame.Physics]
   )



tray.AddModule("TrashCan","trashcan")

# Execute the Tray
tray.Execute()
tray.Finish()
