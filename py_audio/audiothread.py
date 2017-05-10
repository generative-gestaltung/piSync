#!/usr/bin/env python


from __future__ import print_function

import sys
import wave
import getopt
import alsaaudio
import math
import random
import threading
import func
import wavefile
from array import array 

from multiprocessing import Queue


class WaveFile:
      def __init__(self, filename):
          self.ready = False
          try:
              f = open (filename, "r")
              self.wavedata = f.read()
              self.len = len (self.wavedata)
              f.close()
              self.ready = True
              print ("load file "+self.len)

          except Exception:
              print (Exception)
          
      def get_sample (self, phase):
          if (self.ready):
              #ph = (phase*4)%self.len
              #b = bytearray ([self.wavedata[ph+1], self.wavedata[ph+0]])
              #return b[0]<<8 | b[1]
              return int(math.sin(phase*0.1)*32000+32000)

class CodeDummy:
    def _init(self):
        return 0

    def _calc(self, phase):
        return 0


class AudioThread (threading.Thread):

    def __init__(self, threadID, name, counter, wavepath):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.play = False
        self.queue = Queue()        
        self.obj0 = {}
        self.wavepath = wavepath
        self.c = CodeDummy()


    def run (self):    

        device = 'default'
        device = alsaaudio.PCM(device=device)


        device.setchannels (1)
        device.setrate(32000)
        device.setformat(alsaaudio.PCM_FORMAT_U16_BE)


        periodsize = 1000

        device.setperiodsize(periodsize)
        data = array("H") #bytearray (periodsize)
        phase = 0



        self.play = True

        while self.play:

            if (self.queue.empty()==False):
                self.process_queue()

            for i in range (0, periodsize):
	        
                d = (int(math.sin(phase*0.1)*127+127))
                #data.append (int(math.sin(phase*0.1)*127+127)) #self.c._calc(phase)>>8
	        #data[i*2+1] = 0#self.c._calc(phase)&0xff
                phase += 1

                device.write (buffer(d)) # (buffer(data))
       

    def process_queue (self):
        while (self.queue.empty()==False):
            cmd = self.queue.get(True)
            print(cmd)

            if (cmd["cmd"]=="STOP"):
                self.play = False

            if (cmd["cmd"]=="COMPILE"):
                self.obj0 = compile (cmd["code"], "o0", "exec");
                exec(self.obj0)
                self.c = Code()
                self.c._init()


    def stop (self):
        self.queue.put ({"cmd":"STOP"})
 
    def cmd (self, cmd):
        self.queue.put(cmd)
