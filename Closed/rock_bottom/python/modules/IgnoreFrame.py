from icecube.icetray import I3Module, I3ConditionalModule, I3Frame
from icecube import dataclasses
from icecube.dataclasses import I3RecoPulseSeriesMapMask, I3EventHeader, I3Particle



class IgnoreFrame(I3Module):
    """
    I3Module to drop frame objects.
    """
    def __init__(self, ctx):
        I3Module.__init__(self, ctx)
        self.AddParameter("Streams", "Will ignore a given event stream", [])
        self.AddParameter("SubStreams", "Will ignore a given sub-event stream", [])
        self.AddOutBox("OutBox")

    def Configure(self):
        self.substreams = self.GetParameter("SubStreams")
        self.streams = self.GetParameter("Streams")

    def Physics(self, frame):
        if not frame.Stop in self.streams and not frame['I3EventHeader'].sub_event_stream in self.substreams:
            self.PushFrame(frame)

    def DAQ(self, frame):
        if not frame.Stop in self.streams and not frame['I3EventHeader'].sub_event_stream in self.substreams:
            self.PushFrame(frame)

class WriteSeed(I3Module):
    """
    I3Module to write I3Particle from ShowerCOG and ShowerPlane seeds
    """
    def __init__(self, ctx):
        I3Module.__init__(self, ctx)
        self.AddParameter("ShowerCOG", "Input ShowerCOG name", "ShowerCOG")
        self.AddParameter("ShowerPlane", "Input ShowerPlane name", "ShowerPlane")
        self.AddParameter("OutputName", "Output I3Particle name")
        self.AddOutBox("OutBox")

    def Configure(self):
        self.cog = self.GetParameter("ShowerCOG")
        self.plane = self.GetParameter("ShowerPlane")
        self.outname = self.GetParameter("OutputName")

    def Physics(self, frame):
        cog = frame[self.cog]
        plane = frame[self.plane]
        part = I3Particle()
        part.dir = plane.dir
        part.pos = cog.pos
        part.time = cog.time
        part.shape = dataclasses.I3Particle.ParticleShape.InfiniteTrack
        part.fit_status = dataclasses.I3Particle.FitStatus.OK

        frame[self.outname] = part
    
        self.PushFrame(frame)
        
