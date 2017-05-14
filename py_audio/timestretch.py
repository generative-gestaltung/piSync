import pyaudio
import wave
import time
import sys
import math
import random
from array import array
import numpy as np
import struct
from sampleslot import SampleSlot
from stretchsample import StretchSample


FRAME = 128

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)

s0 = SampleSlot(sys.argv[1])
s1 = StretchSample(sys.argv[1],8,FRAME,3)



# instantiate PyAudio (1)
p = pyaudio.PyAudio()

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    #data = s0.getFrame (frame_count) #data.readframes(frame_count)
    #data = s0.getFrameFFT (0) #data.readframes(frame_count)
    data = s1.getFrame()

    return (data, pyaudio.paContinue)

# open stream using callback (3)
stream = p.open(format=p.get_format_from_width(2),
                channels=1,
                rate=s0.rate,
                output=True,
                stream_callback=callback,
                frames_per_buffer=FRAME)

# start the stream (4)
stream.start_stream()

# wait for stream to finish (5)

ss = 0
s0.setSlices(16)
speed = 1
s1.setSpeed(2)
while stream.is_active():
    time.sleep(0.1)
    #s1.setPitch(speed)
    #speed = 0.03
    #s0.selectSlice(ss)
    #ss += 1
# stop stream (6)
stream.stop_stream()
stream.close()


# close PyAudio (7)
p.terminate()
