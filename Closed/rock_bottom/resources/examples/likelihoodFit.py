#!/usr/bin/env python

def main(inputFiles, outfile, n=None, outputLevel=2):
    import math
    import numpy

    from I3Tray import I3Tray
    from icecube import icetray, dataclasses, dataio, phys_services, rock_bottom, gulliver, lilliput

    from icecube.rock_bottom import processing as rb_processing

    icetray.set_log_level_for_unit('RockBottom', icetray.I3LogLevel(outputLevel))
    icetray.set_log_level_for_unit('I3TopNKG', icetray.I3LogLevel(outputLevel))
    icetray.set_log_level_for_unit('I3LaputopSignalModel', icetray.I3LogLevel(outputLevel))

    gcdfile = ["/Users/javierg/IceCubeData/GeoCalibDetectorStatus_IC79.55380_L2a.i3"]
    #gcdfile = ["/data/icet0/gonzalez/IceCubeData/GeoCalibDetectorStatus_IC79.55380_L2a.i3"]

    # Instantiate a tray
    tray = I3Tray()

    nkg = rock_bottom.ldf.NKG()
    #laputop_ltp = rock_bottom.functions.ERF(x_0=math.log10(0.1657), sigma=0.35)
    #rock_bottom_ltp = rock_bottom.functions.ERF(x_0=math.log10(0.22), sigma=0.14)
    laputop_ltp = 0
    rock_bottom_ltp = 0
    laputop_saturation = rock_bottom.functions.LaputopSaturationProbability()
    tray.AddService('SingleLDFSignalModel', "Single_NKGLDF",
                    LDF=nkg,
                    LTP=laputop_ltp,
                    Saturation=laputop_saturation,
                    )

    tray.AddService('LaputopSignalModel', "Laputop_NKGLDF",
                    LDF=nkg,
                    LTP=laputop_ltp,
                    Saturation=laputop_saturation,
                    )

    tray.AddService("I3GulliverMinuitFactory", "Minuit",
                    MinuitPrintLevel = -2,
                    FlatnessCheck = True,
                    Algorithm = "SIMPLEX",
                    MaxIterations = 2500,
                    MinuitStrategy = 2,
                    Tolerance = 0.01,
                    )


    tray.AddModule( 'I3Reader', 'Reader', FilenameList = gcdfile + inputFiles)

    tray.AddSegment(rb_processing.SelectInIce, 'InIceSelection')

    tray.AddSegment(rb_processing.CalibrateSLCs, 'CalibrateSLCs', SLCVEMPulses='IceTopSLCVEMPulses')

    #tray.AddSegment(rb_processing.SelectPulses, 'SelectPulses',
    #                Seed="MPEFitMuE")

    tray.AddModule(lambda frame: 'IceTopSelectedHLC' in frame and len(frame['IceTopSelectedHLC']) >= 8, 'select_icetop')

    tray.AddSegment(rb_processing.MaxLikelihood, "NKG",
                    #Parameters={'S_ref':(numpy.nan, numpy.nan, 2),
                    #            "beta":(numpy.nan, numpy.nan, 2),
                    #            "Moliere":(numpy.nan, numpy.nan, 100.)},
                    Parameters={'S_ref':(numpy.nan, numpy.nan, 2), 'x':[1000], 'y':[1000]},
                    #Parameters={'S_ref':(numpy.nan, numpy.nan, 2),"beta":(numpy.nan, numpy.nan, 2), 'x':[1000]},
                    Seed = "MPEFitMuE",
                    Model="Laputop_NKGLDF",
                    HLCPulses="IceTopSelectedHLC",
                    LDF="NKG_LDF")

    #tray.AddSegment(rb_processing.RedoOfflineIceTopReco, "OfflineIceTopReco", Pulses='IceTopSelectedHLC')

    tray.AddModule("I3Writer", "i3-writer",
                   Filename = "%s.i3"%outfile,
                   DropOrphanStreams = [ icetray.I3Frame.DAQ ],
                   streams = [icetray.I3Frame.DAQ, icetray.I3Frame.Physics]
                   )


    tray.AddModule( 'TrashCan' , 'Done' )


    # Execute the Tray
    if n is None:
        tray.Execute()
    else:
        tray.Execute(n)
    tray.Finish()


if __name__ == "__main__":
    import sys
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage='%s [options] {i3 file list}'%os.path.basename(sys.argv[0]))
    parser.add_option("-o", "--outputprefix", action="store", type="string", dest="output", help="Output file name", metavar="FILE")
    parser.add_option("-n", action="store", type="int", dest="n", help="number of frames to process", metavar="N")
    #parser.add_option('--verbosity', action="store", type="int", dest="log_level", help="integer log level", metavar="V")
    parser.add_option("--debug", action="store_const", dest="log_level", help="Trace log-level", const=1, metavar="N", default=2)
    parser.add_option("--trace", action="store_const", dest="log_level", help="Trace log-level", const=0, metavar="N", default=2)


    (options, inputFiles) = parser.parse_args()

    if len(inputFiles) > 0:
        main(inputFiles, outfile=options.output, n=options.n, outputLevel=options.log_level)
