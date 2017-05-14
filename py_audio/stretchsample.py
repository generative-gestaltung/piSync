import sys
from numpy import *
import scipy.io.wavfile
from scipy.ndimage.interpolation import shift
import wave
import sys
#import random

def load_wav(filename):
    try:
        wavedata=scipy.io.wavfile.read(filename)
        samplerate=int(wavedata[0])
        smp=wavedata[1]*(1.0/32768.0)
        if len(smp.shape)>1: #convert to mono
            smp=(smp[:,0]+smp[:,1])*1.5
        return (samplerate,smp)
    except:
        print ("Error loading wav: "+filename)
        return None



class StretchSample:

    def __init__ (self, fname, stretch, windowsize, nOverlays):

        self.nOverlays = nOverlays

        ret = load_wav (fname)
        self.samplerate = ret[0]
        self.smp = ret[1]
        #make sure that windowsize is even and larger than 16
        self.windowsize=int(windowsize * nOverlays)

        '''
        if windowsize<16:
            windowsize=16
        self.windowsize=int(windowsize/2)*2
        self.half_windowsize=int(windowsize/2)

        #correct the end of the smp
        self.end_size=int(self.samplerate*0.05)
        if self.end_size<16:
            self.end_size=16
        '''


        #self.smp[len(self.smp)-self.end_size:len(self.smp)]*=linspace(1,0,self.end_size)


        #compute the displacement inside the input file
        self.start_pos=0.0
        self.displace_pos=(self.windowsize*0.5)/stretch
        #print(displace_pos)

        #create Hann window
        self.window=0.5-cos(arange(self.windowsize,dtype='float')*2.0*pi/(self.windowsize-1))*0.5

        self.old_windowed_buf = [zeros(self.windowsize)]*self.nOverlays
        hinv_sqrt2=(1+sqrt(0.5))*0.5
        self.hinv_buf=hinv_sqrt2-(1.0-hinv_sqrt2)*cos(arange(self.windowsize/self.nOverlays,dtype='float')*2.0*pi/self.windowsize/self.nOverlays)


    def setSpeed (self, speed):
        self.displace_pos=(self.windowsize*0.5)/speed

    def setPitch (self, pitch):
        self.pitch = pitch

    def getFrame (self):

        #get the windowed buffer
        istart_pos=int(floor(self.start_pos))
        buf=self.smp[istart_pos:istart_pos+self.windowsize]

        if len(buf)<self.windowsize:
            buf=append(buf,zeros(self.windowsize-len(buf)))
        buf=buf*self.window

        #get the amplitudes of the frequency components and discard the phases
        #freqs=abs(fft.fft(buf))
        #_freqs = fft.fftfreq(self.windowsize)
        freqs=fft.fft(buf)


        #freqs = freqs[4:]# + freqs[:4]
        #freqs = shift(freqs,,cval=0)
        #print(type(freqs))

        #randomize the phases by multiplication with a random complex number with modulus=1
        #ph=random.uniform(0,2*pi,len(freqs))*1j

        #freqs=freqs*exp(ph)

        #freqs = freqs*exp(_freqs)

        #do the inverse FFT
        buf=fft.ifft(freqs)

        #window again the output buffer
        buf*=self.window

        #self.start_pos += self.windowsize






        #original

        #overlap-add the output
        #output=buf[0:self.half_windowsize]+self.old_windowed_buf[0][self.half_windowsize:self.windowsize]
        #self.old_windowed_buf[0]=buf

        ws = self.windowsize / self.nOverlays
        output = buf[0 : ws]

        for i in range (1,self.nOverlays):
            output += self.old_windowed_buf[i-1][ws*i:ws*(i+1)]

        for i in range (1,self.nOverlays):
            ind0 = self.nOverlays-i
            ind1 = self.nOverlays-i-1
            self.old_windowed_buf[ind0] = self.old_windowed_buf[ind1]
        self.old_windowed_buf[0] = buf

        #self.old_windowed_buf[0]=buf


        #remove the resulted amplitude modulation
        output*=self.hinv_buf

        #clamp the values to -1..1
        output[output>1.0]=1.0
        output[output<-1.0]=-1.0

        #write the output to wav file
        #outfile.writeframes(int16(output*32767.0).tostring())

        self.start_pos = (self.start_pos+90)#self.displace_pos) % len(self.smp)
        #if start_pos>=len(smp):
        #    print ("100 %")


        output = buf


        return int16(output*32767).tostring()
        #sys.stdout.write ("%d %% \r" % int(100.0*start_pos/len(smp)))
        #sys.stdout.flush()


#(samplerate,smp)=load_wav(sys.argv[1])
#paulstretch (samplerate, smp, 4, 512, "out.wav")
