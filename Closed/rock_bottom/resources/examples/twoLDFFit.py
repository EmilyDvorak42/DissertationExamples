#!/usr/bin/env python

def main(inputFiles, outfile, n=None, outputLevel=2):
    import math
    import numpy

    from I3Tray import I3Tray
    from icecube import icetray, dataclasses, dataio, phys_services, rock_bottom, gulliver, lilliput

    icetray.set_log_level_for_unit('RockBottom', icetray.I3LogLevel(outputLevel))
    icetray.set_log_level_for_unit('I3TwoLDFSignalModel', icetray.I3LogLevel(outputLevel))
    icetray.set_log_level_for_unit('I3TopLeanFitter', icetray.I3LogLevel(outputLevel))
    icetray.set_log_level_for_unit('I3TopSeedService', icetray.I3LogLevel(outputLevel))

    gcdfile = [options.gcd]

    # Instantiate a tray
    tray = I3Tray()

    HLCPulses='OfflineIceTopSelectedHLC'
    SLCPulses='OfflineIceTopSelectedSLC'

    tray.AddService('I3GulliverMinuitFactory', 'Minuit',
                    MinuitPrintLevel = -2,
                    FlatnessCheck = True,
                    Algorithm = 'SIMPLEX',
                    MaxIterations = 2500,
                    MinuitStrategy = 2,
                    Tolerance = 0.01,
                    )

    tray.AddService('TwoLDFSignalModel', 'TwoLDFSignalModel',
                    TankResponseTablesDir = '/data/icet0/gonzalez/IceCubeSoftware/Sandbox/rock_bottom/resources/data/tank_response')

    tray.AddService('I3TopLDFLikelihoodFactory', 'TwoLDFLikelihood',
                    Model='TwoLDFSignalModel',
                    HLCPulses=HLCPulses,
                    SLCPulses=SLCPulses,
                    SaturatedPulses='',
                    IgnoreTanks=''
                    )

    tray.AddService('I3TopTrivialGulliverParametrizationFactory', 'TwoLDFParam',
                    Parameters=dataclasses.I3MapStringVectorDouble({'S_ref':(numpy.nan, numpy.nan, 2), 'rho_mu_ref':[1.], 'age':[0.8]})
                    )

    tray.AddService('I3TopSeedServiceFactory', 'TwoLDFSeed',
                    Seed = 'Laputop',
                    HLCPulses = HLCPulses,
                    SLCPulses = SLCPulses,
                    SignalModel='TwoLDFSignalModel',
                    )

    tray.AddModule( 'I3Reader', 'Reader', FilenameList = gcdfile + inputFiles)

    #def select(frame): return True
    #tray.AddSegment(select, 'selection')

    tray.AddModule('I3TopLeanFitter', 'TwoLDFLeanFitter',
                   Minimizer = 'Minuit',
                   Parametrization = 'TwoLDFParam',
                   LogLikelihood = 'TwoLDFLikelihood',
                   Seed = 'TwoLDFSeed')

    tray.AddModule('I3Writer', 'i3-writer',
                   Filename = outfile,
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


if __name__ == '__main__':
    import sys, os
    import os.path
    from optparse import OptionParser
    parser = OptionParser(usage='%s [options] {i3 file list}'%os.path.basename(sys.argv[0]))
    parser.add_option('-o', '--outputprefix', action='store', type='string', dest='output', help='Output file name', metavar='FILE')
    parser.add_option('-n', action='store', type='int', dest='n', help='number of frames to process', metavar='N')
    #parser.add_option('--verbosity', action='store', type='int', dest='log_level', help='integer log level', metavar='V')
    parser.add_option('--gcd', action='store', dest='gcd', help='GCD file', metavar='GCD_FILE', default='%s/GeoCalibDetectorStatus_IC86.55697_corrected_V2.i3.gz'%os.environ['I3_DATA'])
    parser.add_option('--debug', action='store_const', dest='log_level', help='Trace log-level', const=1, metavar='N', default=2)
    parser.add_option('--trace', action='store_const', dest='log_level', help='Trace log-level', const=0, metavar='N', default=2)


    (options, inputFiles) = parser.parse_args()

    ok = True
    if not os.path.exists(options.gcd):
        print '"%s"does not exist'%options.gcd
        ok = False
    if not os.path.isfile(options.gcd):
        print '"%s" is not a valid GCD file'%options.gcd
        ok = False

    if not options.output:
        print 'need to specify output file name!'
        ok = False
        
    if ok and len(inputFiles) > 0:
        main(inputFiles, outfile=options.output, n=options.n, outputLevel=options.log_level)
    else:
        parser.print_help()
