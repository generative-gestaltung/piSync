from Queue import Queue
import wave
import math
import numpy as np
import struct
from itertools import izip
import operator

flatten = lambda l: [item for sublist in l for item in sublist]

def getChannel (data, ch):

    pairs = zip(data[::2], data[1::2])
    ret = []
    ret.append(flatten(pairs[0::2]))
    ret.append(flatten(pairs[1::2]))

    return ''.join(ret[ch])


class SampleSlot :

    def __init__(self, filename):

        self.CMD_SELSLICE = 0
        self.CMD_NSLICES = 1

        wav = wave.open (filename, 'rb')
        self.len = wav.getnframes()
        self.data = getChannel (wav.readframes(self.len/2), 0)



        self.sampwidth = wav.getsampwidth()
        self.nchannels = wav.getnchannels()

        self.rate = wav.getframerate()

        self.queue = Queue()
        self.spec = 0
        self.specs = []

        self.fftsize = 128
        self.nFFT = self.len / self.fftsize
        self.analyze()

        wav.close()

        self.currentSlice = 0
        self.__setSlices(16)
        self.__selectSlice(0)
        self.index = self.start

        self.running = True
        self.p0 = 0
        self.p1 = 0

    def analyze (self):

        scale = [2/65535.0]*self.fftsize
        offset = [-1]*self.fftsize
        window = []

        for i in range (0, self.fftsize):
            v = math.sin(i*2*math.pi/self.fftsize-math.pi/2)*0.5+0.5
            window.append(v)

        self.ss = 0
        sz = self.fftsize*2
        nspecs = int(math.floor(self.len/sz))

        self.slices = []
        for i in range (0, nspecs):
            y = struct.unpack("%dH"%self.fftsize,self.data[i*sz:(i+1)*sz])
            y = map(operator.mul, scale, y)
            y = map(operator.add, offset, y)
            y = map(operator.mul, window, y)
            self.slices.append(y)

            Y = np.fft.fft(self.slices[i])
            self.specs.append(Y)

        #print(self.slices[0][0:10])



    def __selectSlice (self, slice):
        self.currentSlice = slice
        self.start = slice*self.sliceLen
        self.stop = (slice+1)*self.sliceLen
        self.index = self.start

    def selectSlice (self, slice):
        self.queue.put([self.CMD_SELSLICE, slice])

    def __setSlices (self, nSlices):
        self.nSlices = nSlices
        self.sliceLen = self.len / self.nSlices
        self.__selectSlice(self.currentSlice)

    def setSlices (self, nSlices):
        self.queue.put([self.CMD_NSLICES, nSlices])

    def getFrameFFT (self, frame_count):

        '''
        if (self.queue.empty() == False):
            cmd = self.queue.get()
            if (cmd[0]==self.CMD_SELSLICE):
                self.__selectSlice(cmd[1])
            elif (cmd[0]==self.CMD_NSLICES):
                self.__setSlices(cmd[1])

        self.p1 = self.p0 + 4*frame_count
        dat = self.data [self.p0:self.p1]
        self.p0 += 4*frame_count

        dat = np.fft.ifft(self.specs[self.spec])
        self.spec += 1
        print(self.spec)
        '''

        ind = int(math.floor(self.ss))
        t = self.ss-ind
        self.ss  = (self.ss+1)%(len(self.specs)-1)


        spec0 = self.specs[ind]
        spec1 = self.specs[ind+1]

        '''
        _spec0 = map(operator.mul,spec0,[t]*len(spec0))
        _spec1 = map(operator.mul,spec1,[1-t]*len(spec1))
        _spec = map(operator.add, _spec0, _spec1)
        '''

        _spec = []

        for i in range (0,128):
            v = (1-t)*spec0[i]+t*spec1[i]
            _spec.append (v)


        dat = np.fft.ifft (_spec)

        dat = map(operator.add, dat, [1]*len(dat))
        dat = map(operator.mul, dat, [32668]*len(dat))

        #print(dat[0:10])
        #dat = np.fft.ifft (spec0)

        return struct.pack ("%dH"%len(dat), *dat)



    def getFrame (self, frame_count):


        '''
        if (self.queue.empty() == False):
            cmd = self.queue.get()
            if (cmd[0]==self.CMD_SELSLICE):
                self.__selectSlice(cmd[1])
            elif (cmd[0]==self.CMD_NSLICES):
                self.__setSlices(cmd[1])

        '''
        self.p0 = self.index*2
        self.p1 = (self.index+frame_count)*2

        self.index += frame_count

        # stereo to mono
        return self.data[self.p0:self.p1]
