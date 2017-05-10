#!/usr/bin/env python

import time

from audiothread import AudioThread



if __name__ == '__main__':

    audioT = AudioThread (0, "audio", 0)
    audioT.start()

    time.sleep(1)
    audioT.cmd({"cmd":"COMPILE", "code":"val=math.sin(phase*0.03)"})

    time.sleep(1)
    audioT.cmd({"cmd":"STOP"})

        
    #play(device)
